"""Command line: `python -m allfix [serve|migrate|load-knowledge]`."""

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


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    cmd = sys.argv[1] if len(sys.argv) > 1 else "serve"
    if cmd == "migrate":
        asyncio.run(_migrate_and_load(load=False))
    elif cmd == "load-knowledge":
        asyncio.run(_migrate_and_load(load=True))
    elif cmd == "serve":
        import uvicorn

        s = get_settings()
        uvicorn.run("allfix.main:app", host=s.host, port=s.port, log_level="info")
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
