"""Stage 01 guard, the guarded transport, and the read-only Ads client, with fakes for PIA,
the IP-echo services and Google. Nothing here touches a real network or account."""
import json
from datetime import date

import httpx
import pytest

from allfix import store
from allfix.ads import gaql, importer
from allfix.ads.client import AdsApiError, AdsClient, AdsNotConfigured
from allfix.config import get_settings
from allfix.connectivity import guard as g
from allfix.connectivity.transport import EndpointNotAllowed, GuardedTransport

PROFILE = g.Profile(id=None, project_id="p1", ads_customer_id="123-456-7890", login_customer_id="111-222-3333",
                    required_country="US", required_region="Texas")


def fake_pia(state="Connected", pubip="203.0.113.7", region="us-texas"):
    calls = []

    def run(args):
        calls.append(args)
        return {"connectionstate": state, "pubip": pubip, "region": region}[args[1]]
    pia = g.Pia(path="piactl", runner=run)
    pia.calls = calls
    return pia


def echo_transport(ip="203.0.113.7", country="US", region="Texas", ip2=None, fail=()):
    def handler(req: httpx.Request):
        host = req.url.host
        if host in fail:
            raise httpx.ConnectError("down")
        if host == "ipinfo.io":
            return httpx.Response(200, json={"ip": ip, "country": country, "region": region})
        if host == "ipapi.co":
            return httpx.Response(200, json={"ip": ip2 or ip, "country_code": country, "region": region})
        if host == "api.ipify.org":
            return httpx.Response(200, json={"ip": ip})
        return httpx.Response(404)
    return httpx.MockTransport(handler)


def make_guard(**kw):
    pia = kw.pop("pia", None) or fake_pia()
    return g.RouteGuard(pia=pia, transport=echo_transport(**kw), cache_seconds=300)


async def test_verified_route_passes():
    v = await make_guard().verify(PROFILE)
    assert v.ok and v.public_ip == "203.0.113.7" and v.country == "US"
    names = {c.name: c.ok for c in v.checks}
    assert names["pia_connected"] and names["ip_echo"] and names["matches_pia"] and names["country"]


@pytest.mark.parametrize("kw,failing", [
    ({"pia": fake_pia(state="Disconnected")}, "pia_connected"),
    ({"country": "IL"}, "country"),
    ({"ip2": "198.51.100.9"}, "ip_echo"),
    ({"pia": fake_pia(pubip="198.51.100.1")}, "matches_pia"),
    ({"fail": ("ipinfo.io", "ipapi.co")}, "ip_echo"),
])
async def test_each_failure_blocks(kw, failing):
    v = await make_guard(**kw).verify(PROFILE)
    assert not v.ok
    assert any(c.name == failing and c.ok is False for c in v.checks)


async def test_missing_piactl_blocks():
    guard = g.RouteGuard(pia=g.Pia(path=None, runner=None), transport=echo_transport())
    guard.pia.path = None
    v = await guard.verify(PROFILE)
    assert not v.ok and "not found" in v.checks[0].detail


async def test_region_mismatch_is_advisory_only():
    v = await make_guard(region="California").verify(PROFILE)
    assert v.ok
    assert any(c.name == "region (advisory)" and c.ok is False for c in v.checks)


async def test_ensure_caches_full_check_but_rechecks_pia_every_time():
    pia = fake_pia()
    guard = make_guard(pia=pia)
    await guard.ensure(PROFILE)
    full = len(pia.calls)
    await guard.ensure(PROFILE)
    assert pia.calls[full:] == [["get", "connectionstate"]]     # only the cheap check on a cache hit


async def test_tunnel_drop_blocks_even_with_a_cached_pass():
    pia = fake_pia()
    guard = make_guard(pia=pia)
    await guard.ensure(PROFILE)
    pia._run = lambda args: "Disconnected"
    with pytest.raises(g.ConnectivityBlocked):
        await guard.ensure(PROFILE)
    guard2 = make_guard()
    await guard2.ensure(PROFILE)
    guard2._tunnel_down.set()                                   # what the PIA monitor does
    with pytest.raises(g.ConnectivityBlocked):
        await guard2.ensure(PROFILE)


class Recorder(httpx.AsyncBaseTransport):
    def __init__(self, handler):
        self.handler, self.requests = handler, []

    async def handle_async_request(self, request):
        self.requests.append(request)
        return self.handler(request)


async def test_guarded_transport_refuses_mutations_and_blocked_routes():
    inner = Recorder(lambda r: httpx.Response(200, json={}))
    ok_guard = make_guard()
    async with httpx.AsyncClient(transport=GuardedTransport(ok_guard, PROFILE, inner)) as c:
        with pytest.raises(EndpointNotAllowed):
            await c.post("https://googleads.googleapis.com/v25/customers/1234567890/campaigns:mutate", json={})
        with pytest.raises(EndpointNotAllowed):
            await c.get("https://example.com/")
        await c.get("https://googleads.googleapis.com/v25/customers:listAccessibleCustomers")
    assert len(inner.requests) == 1
    blocked = make_guard(pia=fake_pia(state="Disconnected"))
    inner2 = Recorder(lambda r: httpx.Response(200, json={}))
    async with httpx.AsyncClient(transport=GuardedTransport(blocked, PROFILE, inner2)) as c:
        with pytest.raises(g.ConnectivityBlocked):
            await c.post("https://oauth2.googleapis.com/token", data={})
    assert inner2.requests == []                                  # nothing left the machine


@pytest.fixture
def ads_settings(monkeypatch):
    s = get_settings()
    monkeypatch.setattr(s, "google_oauth_client_id", "cid")
    monkeypatch.setattr(s, "google_oauth_client_secret", "secret")
    monkeypatch.setattr(s, "ads_refresh_token", "rt")
    return s


def google(responses):
    def handler(req: httpx.Request):
        if req.url.host == "oauth2.googleapis.com":
            return httpx.Response(200, json={"access_token": "at", "expires_in": 3600})
        return responses(req)
    return Recorder(handler)


async def test_ads_client_refreshes_token_and_flattens_rows(ads_settings):
    def api(req):
        assert req.headers["authorization"] == "Bearer at" and req.headers["login-customer-id"] == "1112223333"
        assert req.url.path == "/v25/customers/1234567890/googleAds:searchStream"
        assert json.loads(req.content)["query"].endswith("LIMIT 200")
        return httpx.Response(200, json=[{"results": [{"campaign": {"name": "Brand"}, "metrics": {"costMicros": "5000000"}}]}])
    inner = google(api)
    async with AdsClient(PROFILE, guard=make_guard(), inner_transport=inner) as c:
        rows = await c.search("SELECT campaign.name, metrics.cost_micros FROM campaign")
    assert rows == [{"campaign.name": "Brand", "metrics.costMicros": "5000000"}]
    assert [r.url.host for r in inner.requests] == ["oauth2.googleapis.com", "googleads.googleapis.com"]


async def test_ads_errors_are_readable(ads_settings):
    inner = google(lambda r: httpx.Response(403, json=[{"error": {"message": "The caller does not have permission",
                                                                  "details": [{"errors": [{"message": "Customer not enabled"}]}]}}]))
    async with AdsClient(PROFILE, guard=make_guard(), inner_transport=inner) as c:
        with pytest.raises(AdsApiError) as e:
            await c.search("SELECT customer.id FROM customer")
    assert "permission" in str(e.value) and "Customer not enabled" in str(e.value)


def test_ads_client_explains_missing_setup(monkeypatch):
    monkeypatch.setattr(get_settings(), "ads_refresh_token", None)
    with pytest.raises(AdsNotConfigured) as e:
        AdsClient(PROFILE, guard=make_guard())
    assert "ads-login" in str(e.value)


@pytest.mark.parametrize("q,ok", [
    ("SELECT campaign.name FROM campaign", True),
    ("select metrics.clicks from search_term_view where segments.date during LAST_30_DAYS limit 5000", True),
    ("SELECT x FROM campaign; DROP", False),
    ("UPDATE campaign SET x", False),
    ("SELECT x FROM user_list", False),
])
def test_gaql_allowlist(q, ok):
    if ok:
        out = gaql.validate(q)
        assert "LIMIT" in out.upper() and int(out.rsplit(" ", 1)[1]) <= gaql.MAX_LIMIT
    else:
        with pytest.raises(gaql.GaqlError):
            gaql.validate(q)


async def test_import_stores_snapshot_and_summary(database, ads_settings):
    p = await store.create_project({"name": "Acct"})

    def api(req):
        q = json.loads(req.content)["query"]
        if "FROM customer" in q and "segments.date" not in q:
            res = [{"customer": {"descriptiveName": "Acme", "currencyCode": "USD", "autoTaggingEnabled": True}}]
        elif "FROM campaign" in q:
            res = [{"campaign": {"name": "Search - Core"}, "metrics": {"costMicros": "100000000", "clicks": "50", "conversions": 4}},
                   {"campaign": {"name": "PMax"}, "metrics": {"costMicros": "50000000", "clicks": "20", "conversions": 1}}]
        elif "FROM search_term_view" in q:
            res = [{"searchTermView": {"searchTerm": "free grooming course"}, "metrics": {"costMicros": "30000000", "clicks": "9", "conversions": 0}},
                   {"searchTermView": {"searchTerm": "mobile groomer austin"}, "metrics": {"costMicros": "40000000", "clicks": "10", "conversions": 3}}]
        elif "FROM conversion_action" in q:
            res = [{"conversionAction": {"name": "Booking", "category": "PURCHASE", "primaryForGoal": True}}]
        else:
            res = []
        return httpx.Response(200, json=[{"results": res}])

    async with AdsClient(PROFILE, guard=make_guard(), inner_transport=google(api)) as c:
        out = await importer.run_import(p["id"], c, days=30, today=date(2026, 10, 13))
    s = out["summary"]
    assert out["date_range"] == "2026-09-13..2026-10-12"
    assert s["account"] == "Acme" and s["cost"] == 150.0 and s["conversions"] == 5 and s["cost_per_conversion"] == 30.0
    assert s["search_terms_without_conversions"]["top"][0]["term"] == "free grooming course"
    assert s["conversion_actions"][0]["primary"] is True
    snap = await importer.latest_snapshot(p["id"])
    assert snap["status"] == "done"
    assert len(await importer.snapshot_rows(snap["id"], "campaigns")) == 2


def test_api_profile_and_verify():
    # TestClient runs the app on its own loop, so this test opens the pool through the app's lifespan.
    from fastapi.testclient import TestClient
    from conftest import reset_schema
    reset_schema()
    from allfix.main import create_app
    from allfix.connectivity import set_guard
    set_guard(make_guard(country="IL"))
    try:
        with TestClient(create_app(load_knowledge=False)) as client:
            pid = client.post("/api/projects", json={"name": "X"}).json()["id"]
            assert client.post(f"/api/projects/{pid}/connectivity/verify").status_code == 400
            r = client.put(f"/api/projects/{pid}/connectivity", json={"required_country": "us", "ads_customer_id": "123-456-7890"})
            assert r.json()["required_country"] == "US"
            v = client.post(f"/api/projects/{pid}/connectivity/verify").json()
            assert v["ok"] is False and any(c["name"] == "country" and c["ok"] is False for c in v["checks"])
            state = client.get(f"/api/projects/{pid}/connectivity").json()
            assert state["checks"][0]["ok"] is False and state["profile"]["last_result"]["ok"] is False
            imp = client.post(f"/api/projects/{pid}/ads/import")
            assert imp.status_code in (400, 423)      # not configured or blocked; never a request
    finally:
        set_guard(None)
