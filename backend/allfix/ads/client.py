"""Read-only Google Ads API client over REST.

Every request (including OAuth token refresh) goes through GuardedTransport, so it is refused
unless the Stage 01 route verifies and the endpoint is on the read-only allowlist.
"""

from __future__ import annotations

import time
from typing import Any

import httpx

from ..config import get_settings
from ..connectivity.guard import Profile, RouteGuard, get_guard
from ..connectivity.transport import GuardedTransport
from . import gaql

ADS_HOST = "https://googleads.googleapis.com"
TOKEN_URL = "https://oauth2.googleapis.com/token"


class AdsNotConfigured(Exception):
    pass


class AdsApiError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(f"Google Ads API error {status}: {message}")
        self.status = status


def digits(customer_id: str | None) -> str | None:
    return "".join(ch for ch in customer_id if ch.isdigit()) if customer_id else None


def flatten(row: dict, prefix: str = "") -> dict:
    """{"campaign": {"name": "x"}, "metrics": {"costMicros": "5"}} -> {"campaign.name": "x", "metrics.costMicros": "5"}"""
    out: dict[str, Any] = {}
    for k, v in row.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(flatten(v, key + "."))
        else:
            out[key] = v
    return out


class AdsClient:
    def __init__(self, profile: Profile, guard: RouteGuard | None = None,
                 inner_transport: httpx.AsyncBaseTransport | None = None):
        s = get_settings()
        missing = [n for n, v in (("GOOGLE_OAUTH_CLIENT_ID", s.google_oauth_client_id),
                                  ("GOOGLE_OAUTH_CLIENT_SECRET", s.google_oauth_client_secret),
                                  ("ADS_REFRESH_TOKEN", s.ads_refresh_token)) if not v]
        if missing:
            raise AdsNotConfigured("Google Ads access is not set up: missing " + ", ".join(missing)
                                   + ". Run `python -m allfix ads-login` on the PC (see docs/GOOGLE_ADS_SETUP.md).")
        self.settings = s
        self.profile = profile
        self.version = s.ads_api_version
        transport = GuardedTransport(guard or get_guard(), profile, inner_transport)
        self.http = httpx.AsyncClient(transport=transport, trust_env=False, timeout=60.0)
        self._token: str | None = None
        self._token_expires = 0.0

    async def __aenter__(self) -> "AdsClient":
        return self

    async def __aexit__(self, *exc) -> None:
        await self.http.aclose()

    async def _access_token(self) -> str:
        if self._token and time.time() < self._token_expires - 60:
            return self._token
        r = await self.http.post(TOKEN_URL, data={
            "grant_type": "refresh_token", "refresh_token": self.settings.ads_refresh_token,
            "client_id": self.settings.google_oauth_client_id,
            "client_secret": self.settings.google_oauth_client_secret})
        if r.status_code != 200:
            raise AdsApiError(r.status_code, f"token refresh failed: {r.text[:200]}")
        d = r.json()
        self._token = d["access_token"]
        self._token_expires = time.time() + int(d.get("expires_in", 3600))
        return self._token

    async def _headers(self) -> dict:
        h = {"Authorization": f"Bearer {await self._access_token()}"}
        login = digits(self.profile.login_customer_id)
        if login:
            h["login-customer-id"] = login
        return h

    @staticmethod
    def _error(r: httpx.Response) -> AdsApiError:
        try:
            body = r.json()
            body = body[0] if isinstance(body, list) and body else body
            err = body.get("error", {})
            msg = err.get("message") or str(body)[:300]
            details = err.get("details") or []
            for d in details:
                for e in d.get("errors", []) if isinstance(d, dict) else []:
                    msg += f" ({e.get('message', '')})"
        except ValueError:
            msg = r.text[:300]
        return AdsApiError(r.status_code, msg[:500])

    async def list_accessible_customers(self) -> list[str]:
        r = await self.http.get(f"{ADS_HOST}/{self.version}/customers:listAccessibleCustomers",
                                headers=await self._headers())
        if r.status_code != 200:
            raise self._error(r)
        return [n.split("/")[-1] for n in r.json().get("resourceNames", [])]

    async def search(self, query: str, customer_id: str | None = None, validate: bool = True,
                     max_rows: int = 10000) -> list[dict]:
        cid = digits(customer_id or self.profile.ads_customer_id)
        if not cid:
            raise AdsNotConfigured("the connection profile has no Google Ads customer id")
        q = gaql.validate(query) if validate else query
        r = await self.http.post(f"{ADS_HOST}/{self.version}/customers/{cid}/googleAds:searchStream",
                                 headers=await self._headers(), json={"query": q})
        if r.status_code != 200:
            raise self._error(r)
        rows: list[dict] = []
        for batch in r.json():
            rows.extend(flatten(x) for x in batch.get("results", []))
            if len(rows) >= max_rows:
                break
        return rows[:max_rows]
