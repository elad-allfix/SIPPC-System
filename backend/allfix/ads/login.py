"""`python -m allfix ads-login`: get a Google Ads refresh token on this PC.

Installed-app OAuth with a loopback redirect and PKCE (Google's supported flow for desktop clients).
The browser sign-in is yours; the code-for-token exchange goes through the Stage 01 guard, so it only
happens when PIA is connected in the required country. The token is written to the local .env only.
"""

from __future__ import annotations

import base64
import hashlib
import http.server
import secrets
import threading
import urllib.parse
import webbrowser
from pathlib import Path

import httpx

from ..config import REPO_ROOT, get_settings
from ..connectivity.guard import ConnectivityBlocked, Profile, RouteGuard
from ..connectivity.transport import GuardedTransport

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPE = "https://www.googleapis.com/auth/adwords"


def auth_url(client_id: str, redirect_uri: str, state: str, challenge: str) -> str:
    return AUTH_URL + "?" + urllib.parse.urlencode({
        "client_id": client_id, "redirect_uri": redirect_uri, "response_type": "code", "scope": SCOPE,
        "access_type": "offline", "prompt": "consent", "state": state,
        "code_challenge": challenge, "code_challenge_method": "S256"})


def pkce() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    return verifier, challenge


def set_env_value(path: Path, key: str, value: str) -> None:
    """Replace or append KEY=value in a .env file, keeping everything else as it was."""
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    out, done = [], False
    for line in lines:
        if line.split("=", 1)[0].strip() == key:
            if not done:
                out.append(f"{key}={value}")
                done = True
            continue
        out.append(line)
    if not done:
        out.append(f"{key}={value}")
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def _wait_for_code(state: str) -> tuple[str, int, threading.Event, dict]:
    result: dict = {}
    done = threading.Event()

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if q.get("state", [""])[0] != state:
                self.send_response(400)
                self.end_headers()
                return
            result.update({k: v[0] for k, v in q.items()})
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            msg = "Signed in. You can close this tab and go back to the terminal." if "code" in result \
                else f"Sign-in failed: {result.get('error', 'unknown')}"
            self.wfile.write(f"<p style='font-family:sans-serif'>{msg}</p>".encode())
            done.set()

        def log_message(self, *a):
            pass

    server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    port = server.server_address[1]
    result["_server"] = server
    return f"http://127.0.0.1:{port}", port, done, result


async def run(country: str, env_path: Path | None = None) -> int:
    s = get_settings()
    env_path = env_path or REPO_ROOT / ".env"
    if not (s.google_oauth_client_id and s.google_oauth_client_secret):
        print("Set GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET in .env first (a Desktop app OAuth client, "
              "see docs/GOOGLE_ADS_SETUP.md).")
        return 2
    profile = Profile(id=None, project_id="ads-login", ads_customer_id=None, login_customer_id=None,
                      required_country=country.upper(), required_region=None)
    guard = RouteGuard()
    v = await guard.verify(profile)
    for c in v.checks:
        print(f"  {'ok ' if c.ok else '-- ' if c.ok is None else 'NO '} {c.name}: {c.detail}")
    if not v.ok:
        print("Stopped: the route check failed, so nothing was sent to Google. Connect PIA and try again.")
        return 3

    redirect_uri, _, done, result = _wait_for_code(state := secrets.token_urlsafe(16))
    verifier, challenge = pkce()
    url = auth_url(s.google_oauth_client_id, redirect_uri, state, challenge)
    print("\nSign in with the Google account that can see the Ads account. If no browser opened, paste this link:\n")
    print(url + "\n")
    webbrowser.open(url)
    try:
        if not done.wait(timeout=300):
            print("Timed out waiting for the sign-in.")
            return 4
    finally:
        result.pop("_server").shutdown()
    if "code" not in result:
        print(f"Sign-in failed: {result.get('error', 'no code returned')}")
        return 4

    try:
        async with httpx.AsyncClient(transport=GuardedTransport(guard, profile), trust_env=False, timeout=30) as http:
            r = await http.post(TOKEN_URL, data={
                "grant_type": "authorization_code", "code": result["code"], "redirect_uri": redirect_uri,
                "client_id": s.google_oauth_client_id, "client_secret": s.google_oauth_client_secret,
                "code_verifier": verifier})
    except ConnectivityBlocked as e:
        print(f"Stopped: {e}")
        return 3
    if r.status_code != 200 or "refresh_token" not in r.json():
        print(f"Token exchange failed ({r.status_code}): {r.text[:300]}")
        return 5
    set_env_value(env_path, "ADS_REFRESH_TOKEN", r.json()["refresh_token"])
    print(f"Saved ADS_REFRESH_TOKEN to {env_path}. Restart AllFix, then use Stage 01 > Verify route > Import.")
    return 0
