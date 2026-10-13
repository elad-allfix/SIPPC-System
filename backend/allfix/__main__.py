"""Command line: `python -m allfix [serve|migrate|load-knowledge|ads-login --country US|check-accounts]`."""

from __future__ import annotations

import asyncio
import logging
import sys

from .config import get_settings


async def _migrate_and_load(load: bool) -> None:
    from . import db
    from .knowledge import loader

    await db.open_pool()
    try:
        applied = await db.migrate()
        print(f"migrations applied: {applied or 'none (up to date)'}")
        if load:
            print(f"knowledge loaded: {await loader.load(get_settings().knowledge_dir)}")
    finally:
        await db.close_pool()


def _run(coro) -> None:
    # psycopg's async driver needs a selector event loop; Windows defaults to the proactor loop.
    if sys.platform == "win32":
        asyncio.run(coro, loop_factory=asyncio.SelectorEventLoop)
    else:
        asyncio.run(coro)


def _check_accounts() -> int:
    """Ask the running AllFix server to run today's account checks (used by the scheduled task)."""
    import httpx

    s = get_settings()
    host = "127.0.0.1" if s.host in ("0.0.0.0", "::") else s.host
    auth = ("allfix", s.allfix_password) if s.allfix_password else None
    try:
        r = httpx.post(f"http://{host}:{s.port}/api/rounds/account-check", auth=auth, timeout=900, trust_env=False)
    except httpx.ConnectError:
        print("AllFix is not running; skipped. Start it and the next scheduled run will check.")
        return 0
    if r.status_code != 200:
        print(f"Account check failed: {r.status_code} {r.text[:300]}")
        return 1
    out = r.json()
    for res in out["results"]:
        print(f"{res['project_id']}: {res['status']}: {res['summary']}")
    if not out["results"]:
        print("No project has a Google Ads customer id yet; nothing to check.")
    return 0


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    cmd = sys.argv[1] if len(sys.argv) > 1 else "serve"
    if cmd == "migrate":
        _run(_migrate_and_load(load=False))
    elif cmd == "load-knowledge":
        _run(_migrate_and_load(load=True))
    elif cmd == "ads-login":
        from .ads import login

        args = sys.argv[2:]
        country = args[args.index("--country") + 1] if "--country" in args and len(args) > args.index("--country") + 1 else None
        if not country:
            print("usage: python -m allfix ads-login --country US   (the country PIA must exit in)")
            sys.exit(2)
        sys.exit(asyncio.run(login.run(country)))
    elif cmd == "check-accounts":
        sys.exit(_check_accounts())
    elif cmd == "serve":
        import uvicorn

        s = get_settings()
        print(f"AllFix is running at http://{s.host}:{s.port}")
        _run(uvicorn.Server(uvicorn.Config("allfix.main:app", host=s.host, port=s.port, log_level="info")).serve())
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
