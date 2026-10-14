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


def _run(coro):
    # psycopg's async driver needs a selector event loop; Windows defaults to the proactor loop.
    if sys.platform == "win32":
        return asyncio.run(coro, loop_factory=asyncio.SelectorEventLoop)
    return asyncio.run(coro)


async def _serve(server) -> bool:
    """Serve until stopped; True when stopping to take an update from GitHub."""
    from . import updater
    watcher = asyncio.create_task(updater.watch(server)) if updater.enabled() else None
    try:
        await server.serve()
    finally:
        if watcher:
            watcher.cancel()
    return updater.state["restart"]


def _check_accounts() -> int:
    """Ask the running AllFix server to run today's account checks (used by the scheduled task).

    Output also goes to logs/check-accounts.log, since the scheduled task runs without a window."""
    import httpx
    from datetime import datetime

    from .config import REPO_ROOT

    log_path = REPO_ROOT / "logs" / "check-accounts.log"
    log_path.parent.mkdir(exist_ok=True)

    def print(msg: str) -> None:  # noqa: A001 - shadow print for this command only
        with log_path.open("a", encoding="utf-8") as f:
            f.write(f"{datetime.now():%Y-%m-%d %H:%M} {msg}\n")
        if sys.stdout is not None:
            sys.stdout.write(msg + "\n")

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
        print(f"{res.get('project') or res['project_id']}: {res['status']}: {res['summary']}")
    if not out["results"]:
        print("No project has a Google Ads customer id yet; nothing to check.")
    return 0


def main() -> None:
    # Hebrew text and symbols must not crash output on a Windows console or when redirected.
    for stream in (sys.stdout, sys.stderr):
        if stream is not None and hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
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
        from .updater import UPDATE_EXIT_CODE
        print(f"AllFix is running at http://{s.host}:{s.port}")
        server = uvicorn.Server(uvicorn.Config("allfix.main:app", host=s.host, port=s.port, log_level="info"))
        if _run(_serve(server)):
            sys.exit(UPDATE_EXIT_CODE)
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
