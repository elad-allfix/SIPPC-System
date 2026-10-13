"""Stage 01: verify the outbound route before any protected Google Ads access, and fail closed.

The rule: AllFix touches a Google Ads account (OAuth or API) only when this machine's traffic
provably leaves through the expected PIA VPN route in the expected country. A Dolphin Anty
browser profile protects browser sessions only; it does nothing for API calls, so API calls
rely on the system VPN route checked here.

Checks, cheapest first:
1. PIA reports Connected (`piactl get connectionstate`). Run before every protected request.
2. Two independent HTTPS IP-echo services agree on the public IP, and it equals PIA's public
   VPN IP (`piactl get pubip`) when PIA reports one.
3. Geolocation of that IP matches the profile's country (strict) and region (advisory).
4. Optional: the Dolphin Anty app is reachable and knows the profile id.

A full pass (2-3) is cached for `route_cache_seconds`; check 1 and a background monitor of
PIA's connection state (when available) run continuously, so a dropped tunnel blocks at once.
The real enforcement is PIA's own kill switch; this guard is defence in depth and keeps an
audit trail. All HTTP here ignores proxy environment variables and uses IPv4 only.
"""

from __future__ import annotations

import asyncio
import logging
import shutil
import subprocess
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import httpx

from ..config import get_settings

log = logging.getLogger(__name__)

WINDOWS_PIACTL = Path(r"C:\Program Files\Private Internet Access\piactl.exe")
ECHO_TIMEOUT = 8.0


class ConnectivityBlocked(Exception):
    """Raised instead of making a protected request when the route is not verified."""


@dataclass
class Profile:
    id: str | None
    project_id: str
    ads_customer_id: str | None
    login_customer_id: str | None
    required_country: str            # ISO 3166-1 alpha-2, e.g. "US"
    required_region: str | None = None
    vpn_profile: str | None = None   # PIA region id as piactl names it; a mismatch is advisory
    dolphin_profile_id: str | None = None

    @classmethod
    def from_row(cls, row: dict) -> "Profile":
        return cls(id=str(row["id"]) if row.get("id") else None, project_id=str(row["project_id"]),
                   ads_customer_id=row.get("ads_customer_id"), login_customer_id=row.get("login_customer_id"),
                   required_country=(row.get("required_country") or "").upper(),
                   required_region=row.get("required_region"), vpn_profile=row.get("vpn_profile"),
                   dolphin_profile_id=row.get("dolphin_profile_id"))


@dataclass
class Check:
    name: str
    ok: bool | None          # None = not applicable / skipped
    detail: str

    def as_dict(self) -> dict:
        return {"name": self.name, "ok": self.ok, "detail": self.detail}


@dataclass
class Verification:
    ok: bool
    checks: list[Check]
    public_ip: str | None = None
    country: str | None = None
    region: str | None = None
    at: float = field(default_factory=time.time)

    def as_dict(self) -> dict:
        return {"ok": self.ok, "public_ip": self.public_ip, "country": self.country, "region": self.region,
                "at": datetime.fromtimestamp(self.at, tz=timezone.utc).isoformat(),
                "checks": [c.as_dict() for c in self.checks]}


def base_transport() -> httpx.AsyncHTTPTransport:
    """The one network path for verification and account traffic: no proxies, IPv4 only."""
    return httpx.AsyncHTTPTransport(local_address="0.0.0.0", retries=1)


# ---------- PIA ----------

class Pia:
    """Thin wrapper over PIA's official command line, piactl."""

    def __init__(self, path: str | None = None, runner: Callable[[list[str]], str] | None = None):
        self.path = path or get_settings().piactl_path or shutil.which("piactl") or (
            str(WINDOWS_PIACTL) if WINDOWS_PIACTL.exists() else None)
        self._custom_runner = runner is not None
        self._run = runner or self._subprocess

    @property
    def available(self) -> bool:
        return self.path is not None or self._custom_runner

    def _subprocess(self, args: list[str]) -> str:
        if not self.path:
            raise FileNotFoundError("piactl not found")
        out = subprocess.run([self.path, *args], capture_output=True, text=True, timeout=10)
        if out.returncode != 0:
            raise RuntimeError((out.stderr or out.stdout).strip()[:200] or f"piactl exit {out.returncode}")
        return out.stdout.strip()

    async def get(self, what: str) -> str:
        # A thread, not an asyncio subprocess: works on every event loop, including Windows selector loops.
        return await asyncio.to_thread(self._run, ["get", what])


# ---------- IP echo ----------

async def _echo(client: httpx.AsyncClient) -> list[dict]:
    """Ask independent services for this machine's public IP and location."""

    async def ipinfo():
        r = await client.get("https://ipinfo.io/json")
        d = r.json()
        return {"service": "ipinfo.io", "ip": d.get("ip"), "country": d.get("country"), "region": d.get("region"),
                "org": d.get("org")}

    async def ipapi():
        r = await client.get("https://ipapi.co/json/")
        d = r.json()
        return {"service": "ipapi.co", "ip": d.get("ip"), "country": d.get("country_code") or d.get("country"),
                "region": d.get("region"), "org": d.get("org")}

    async def ipify():
        r = await client.get("https://api.ipify.org?format=json")
        return {"service": "ipify.org", "ip": r.json().get("ip"), "country": None, "region": None, "org": None}

    results = []
    for res in await asyncio.gather(ipinfo(), ipapi(), ipify(), return_exceptions=True):
        if isinstance(res, Exception):
            results.append({"service": "?", "error": f"{type(res).__name__}: {str(res)[:120]}"})
        else:
            results.append(res)
    return results


# ---------- the guard ----------

class RouteGuard:
    """Decides whether protected Google Ads traffic may leave this machine right now."""

    def __init__(self, pia: Pia | None = None, transport: httpx.AsyncBaseTransport | None = None,
                 cache_seconds: int | None = None, dolphin: "Dolphin | None" = None):
        self.pia = pia or Pia()
        self.transport = transport
        self.cache_seconds = get_settings().route_cache_seconds if cache_seconds is None else cache_seconds
        self.dolphin = dolphin or Dolphin()
        self._last: dict[str, Verification] = {}
        self._tunnel_down = threading.Event()   # set by the PIA monitor when the tunnel drops
        self._monitor: threading.Thread | None = None

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=self.transport or base_transport(), trust_env=False, timeout=ECHO_TIMEOUT)

    async def verify(self, profile: Profile) -> Verification:
        """Run every check now. Never raises; the result says what failed."""
        checks: list[Check] = []
        if not profile.required_country:
            checks.append(Check("profile", False, "the connection profile has no required country"))
            return self._remember(profile, Verification(False, checks))

        # 1. PIA state
        pia_ip = None
        pia_up = False
        if not self.pia.available:
            checks.append(Check("pia_connected", False, "piactl (Private Internet Access command line) was not found"))
        else:
            try:
                state = await self.pia.get("connectionstate")
                pia_up = state == "Connected"
                checks.append(Check("pia_connected", pia_up, f"PIA reports {state}"))
                try:
                    pia_ip = (await self.pia.get("pubip")).strip() or None
                except Exception as e:
                    checks.append(Check("pia_public_ip", None, f"could not read PIA public IP: {e}"))
                if profile.vpn_profile:
                    try:
                        region = await self.pia.get("region")
                        checks.append(Check("pia_region (advisory)", None if region == "auto" else region == profile.vpn_profile,
                                            f"PIA region {region}, expected {profile.vpn_profile}"))
                    except Exception as e:
                        checks.append(Check("pia_region (advisory)", None, f"could not read PIA region: {e}"))
            except Exception as e:
                checks.append(Check("pia_connected", False, f"piactl failed: {e}"))

        if not pia_up:
            # Without the tunnel, asking outside services would show them the real IP. Stop here.
            checks.append(Check("ip_echo", None, "skipped because PIA is not connected; nothing was sent"))
            return self._remember(profile, Verification(False, checks))

        # 2-3. What the internet sees
        async with self._client() as client:
            echoes = await _echo(client)
        good = [e for e in echoes if e.get("ip")]
        ips = {e["ip"] for e in good}
        if len(good) < 2:
            checks.append(Check("ip_echo", False, "fewer than two IP-echo services answered: "
                                + "; ".join(dict.fromkeys(e["error"] for e in echoes if e.get("error")))))
        else:
            checks.append(Check("ip_echo", len(ips) == 1, f"{len(good)} services saw {sorted(ips)}"))
        public_ip = next(iter(ips)) if len(ips) == 1 else None
        if pia_ip and public_ip:
            checks.append(Check("matches_pia", public_ip == pia_ip, f"public IP {public_ip}, PIA VPN IP {pia_ip}"))
        countries = {(e.get("country") or "").upper() for e in good if e.get("country")}
        country = next(iter(countries)) if len(countries) == 1 else None
        if not countries:
            checks.append(Check("country", False, "no service reported a country"))
        else:
            checks.append(Check("country", countries == {profile.required_country},
                                f"seen {sorted(countries)}, required {profile.required_country}"))
        regions = sorted({e["region"] for e in good if e.get("region")})
        if profile.required_region:
            match = any(profile.required_region.lower() in r.lower() for r in regions)
            # Region databases disagree on VPN ranges, so a mismatch is reported but does not block.
            checks.append(Check("region (advisory)", None if not regions else match,
                                f"seen {regions}, wanted {profile.required_region}"))

        # 4. Dolphin (browser sessions only)
        if profile.dolphin_profile_id:
            checks.append(await self.dolphin.check(profile.dolphin_profile_id))

        ok = all(c.ok is not False for c in checks if not c.name.endswith("(advisory)") and c.name != "dolphin")
        v = Verification(ok, checks, public_ip, country, regions[0] if regions else None)
        if ok:
            self._tunnel_down.clear()   # PIA says Connected and the route checks out right now
        return self._remember(profile, v)

    def _remember(self, profile: Profile, v: Verification) -> Verification:
        self._last[profile.id or profile.project_id] = v
        return v

    async def ensure(self, profile: Profile) -> Verification:
        """Raise ConnectivityBlocked unless the route is verified now. Called before protected requests."""
        key = profile.id or profile.project_id
        if self._tunnel_down.is_set():
            self._last.pop(key, None)   # the monitor saw a drop: no cached pass counts, check everything again
        last = self._last.get(key)
        if last and last.ok and time.time() - last.at < self.cache_seconds:
            # Cheap re-check of the tunnel on every request; the full echo/geo check is cached.
            try:
                state = await self.pia.get("connectionstate")
            except Exception as e:
                self._last.pop(key, None)
                raise ConnectivityBlocked(f"could not confirm PIA is connected: {e}") from e
            if state != "Connected":
                self._last.pop(key, None)
                raise ConnectivityBlocked(f"PIA reports {state}")
            return last
        v = await self.verify(profile)
        if not v.ok:
            failed = [f"{c.name}: {c.detail}" for c in v.checks if c.ok is False]
            raise ConnectivityBlocked("route not verified; " + "; ".join(failed))
        return v

    def start_monitor(self) -> None:
        """Watch PIA's connection state in the background; a drop blocks protected traffic at once."""
        if self._monitor or not self.pia.path:
            return

        def run():
            try:
                proc = subprocess.Popen([self.pia.path, "monitor", "connectionstate"], stdout=subprocess.PIPE, text=True)
            except OSError:
                return
            for line in proc.stdout:  # one line per state change
                if line.strip() == "Connected":
                    self._tunnel_down.clear()
                else:
                    self._tunnel_down.set()
                    self._last.clear()
            self._monitor = None   # the monitor ended; ensure() still checks PIA on every request

        self._monitor = threading.Thread(target=run, name="pia-monitor", daemon=True)
        self._monitor.start()


class Dolphin:
    """Optional check that the Dolphin Anty app is running and knows the browser profile."""

    def __init__(self, base_url: str | None = None, token: str | None = None,
                 transport: httpx.AsyncBaseTransport | None = None):
        s = get_settings()
        self.base_url = (base_url or s.dolphin_api_url).rstrip("/")
        self.token = token or s.dolphin_api_token
        self.transport = transport

    async def check(self, profile_id: str) -> Check:
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        try:
            async with httpx.AsyncClient(transport=self.transport, trust_env=False, timeout=5.0) as c:
                r = await c.get(f"{self.base_url}/browser_profiles/{profile_id}", headers=headers)
        except httpx.HTTPError as e:
            return Check("dolphin", False, f"Dolphin Anty local API not reachable ({type(e).__name__})")
        if r.status_code == 200:
            return Check("dolphin", True, f"Dolphin Anty knows profile {profile_id}")
        return Check("dolphin", False, f"Dolphin Anty answered {r.status_code} for profile {profile_id}")


_guard: RouteGuard | None = None


def get_guard() -> RouteGuard:
    global _guard
    if _guard is None:
        _guard = RouteGuard()
        _guard.start_monitor()
    return _guard


def set_guard(guard: RouteGuard | None) -> None:
    """Tests replace the process-wide guard."""
    global _guard
    _guard = guard
