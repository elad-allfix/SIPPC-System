"""The only HTTP path to Google's account APIs.

Every request is checked against an allowlist of read-only endpoints, and the route guard must
pass right before it is sent. Anything else is refused before it leaves the machine.
"""

from __future__ import annotations

import re

import httpx

from .guard import ConnectivityBlocked, Profile, RouteGuard, base_transport

# host, method, path pattern. Search endpoints cannot change an account; mutate endpoints are absent.
ALLOWED = [
    ("oauth2.googleapis.com", "POST", re.compile(r"^/token$")),
    ("googleads.googleapis.com", "GET", re.compile(r"^/v\d+(\.\d+)?/customers:listAccessibleCustomers$")),
    ("googleads.googleapis.com", "POST", re.compile(r"^/v\d+(\.\d+)?/customers/\d+/googleAds:search(Stream)?$")),
]


class EndpointNotAllowed(Exception):
    pass


def check_allowed(request: httpx.Request) -> None:
    host, method, path = request.url.host, request.method, request.url.path
    if request.url.scheme != "https" or not any(
            h == host and m == method and p.match(path) for h, m, p in ALLOWED):
        raise EndpointNotAllowed(f"{method} {request.url.scheme}://{host}{path} is not an allowed read-only endpoint")


class GuardedTransport(httpx.AsyncBaseTransport):
    def __init__(self, guard: RouteGuard, profile: Profile, inner: httpx.AsyncBaseTransport | None = None):
        self.guard = guard
        self.profile = profile
        self.inner = inner or base_transport()

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        check_allowed(request)
        await self.guard.ensure(self.profile)          # raises ConnectivityBlocked
        return await self.inner.handle_async_request(request)

    async def aclose(self) -> None:
        await self.inner.aclose()


__all__ = ["GuardedTransport", "EndpointNotAllowed", "ConnectivityBlocked", "check_allowed"]
