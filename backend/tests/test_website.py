from pathlib import Path

import httpx
import pytest

from allfix.intelligence import website

FIX = Path(__file__).parent / "fixtures"


def _html(name):
    return (FIX / name).read_text()


def test_plain_page_facts():
    r = website.analyse(_html("landing_plain.html"), "https://pawsonwheels.example/",
                        intent="mobile dog grooming austin", ad_headline="Mobile Dog Grooming in Austin")
    assert r["title"].startswith("Mobile Dog Grooming Austin")
    assert r["h1"] == ["Mobile Dog Grooming in Austin"]
    assert r["phone_links"] == ["+15125550123"]
    assert r["has_mobile_viewport"] and r["schema_types"] == ["LocalBusiness"]
    form = r["forms"][0]
    assert form["fields"] == 5 and form["required"] == 2 and form["asks_phone"] and form["asks_email"]
    assert form["submit_text"] == "Get my quote"
    assert "$95" in r["prices_mentioned"]
    assert r["trust_signals"]["licensed_insured"]["pattern_match"]
    assert "insured" in r["trust_signals"]["licensed_insured"]["snippet"]
    m = r["measurement"]
    assert m["visibility"] == "observed" and "google_ads_conversion" in m["tags_seen"]
    assert m["ids"]["google_ads"] == ["AW-123456789"] and "consent_mode" in m["tags_seen"]
    assert r["images_missing_alt"] == 1
    kinds = {l["url"]: l["looks_like"] for l in r["notable_internal_links"]}
    assert "pricing" in kinds["https://pawsonwheels.example/pricing"]
    assert r["ad_message_match"]["exact_in_h1"] and r["intent_terms"]["austin"]["h1"]
    assert not r["looks_javascript_rendered"]


def test_gtm_page_never_reports_tracking_missing():
    r = website.analyse(_html("landing_gtm_only.html"), "https://x.example/")
    assert r["measurement"]["visibility"] == "gtm_present_cannot_inspect"
    assert r["measurement"]["ids"]["gtm"] == ["GTM-ABC1234"]
    assert "Do not conclude" in r["measurement"]["note"]


def test_js_shell_is_flagged():
    r = website.analyse(_html("landing_js_shell.html"), "https://x.example/")
    assert r["looks_javascript_rendered"]


@pytest.mark.parametrize("url", ["http://127.0.0.1:8000", "http://localhost/", "http://[::1]/",
                                 "http://169.254.169.254/latest", "http://10.0.0.5/", "ftp://example.com/",
                                 "http://printer.local/"])
async def test_private_and_non_http_targets_are_refused(url):
    r = await website.audit_page(url)
    assert "error" in r


@pytest.fixture
def mock_web(monkeypatch):
    pages = {}

    def handler(request: httpx.Request):
        status, headers, body = pages[str(request.url)]
        return httpx.Response(status, headers=headers, content=body.encode())

    monkeypatch.setattr(website, "_transport", httpx.MockTransport(handler))
    monkeypatch.setattr(website, "_check_target", lambda u: _fake_check(u))
    return pages


def _fake_check(url):
    if "169.254" in url or "127.0.0.1" in url:
        raise website.AuditError("that address is private or local; only public sites can be audited")
    return url


async def test_audit_follows_redirects_and_reports_http_facts(mock_web):
    mock_web["https://a.example/"] = (301, {"location": "https://a.example/home"}, "")
    mock_web["https://a.example/home"] = (200, {"content-type": "text/html", "server": "nginx", "cf-ray": "1"},
                                          _html("landing_plain.html"))
    r = await website.audit_page("https://a.example/")
    assert r["final_url"] == "https://a.example/home" and r["redirects"] == ["https://a.example/"]
    assert r["http"]["server"] == "nginx" and r["http"]["cdn_hint"] == "cloudflare"
    assert r["h1"] == ["Mobile Dog Grooming in Austin"] and "limits" in r


async def test_redirect_to_private_address_is_refused(mock_web):
    mock_web["https://a.example/"] = (302, {"location": "http://169.254.169.254/latest/meta-data"}, "")
    r = await website.audit_page("https://a.example/")
    assert "private" in r["error"]


async def test_challenge_page_is_reported_as_blocked(mock_web):
    mock_web["https://b.example/"] = (403, {"content-type": "text/html"}, _html("blocked_cloudflare.html"))
    r = await website.audit_page("https://b.example/")
    assert r["blocked"] and r["block_vendor"] == "cloudflare" and "h1" not in r


async def test_non_html_is_reported(mock_web):
    mock_web["https://c.example/file.pdf"] = (200, {"content-type": "application/pdf"}, "%PDF-1.4")
    r = await website.audit_page("https://c.example/file.pdf")
    assert "not an HTML page" in r["error"]
