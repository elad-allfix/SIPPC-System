"""Keep a PC install current without anyone clicking: notice new commits on GitHub and, when no
answer is being written, stop the server so scripts/run.ps1 updates and starts it again.

On only when ALLFIX_AUTO_UPDATE=1 (run.ps1 sets it) and the folder is a git checkout. Updates are
fast-forward only, so local work is never overwritten."""

from __future__ import annotations

import asyncio
import logging
import os
import subprocess

from .config import REPO_ROOT

log = logging.getLogger(__name__)

UPDATE_EXIT_CODE = 75
CHECK_EVERY_SECONDS = 600
state = {"restart": False}


def enabled() -> bool:
    return os.environ.get("ALLFIX_AUTO_UPDATE") == "1" and (REPO_ROOT / ".git").exists()


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, timeout=120)


def update_available() -> bool:
    if _git("fetch", "-q", "origin", "main").returncode != 0:
        return False
    head = _git("rev-parse", "HEAD").stdout.strip()
    remote = _git("rev-parse", "origin/main").stdout.strip()
    if not head or not remote or head == remote:
        return False
    blocked = REPO_ROOT / "logs" / "update-blocked.txt"
    if blocked.exists() and blocked.read_text(encoding="utf-8-sig", errors="replace").strip() == remote:
        return False  # this version could not be applied (local changes); don't restart in a loop
    return _git("merge-base", "--is-ancestor", "HEAD", "origin/main").returncode == 0


def idle() -> bool:
    from .strategist.subscription import _locks
    return not any(lock.locked() for lock in _locks.values())


async def watch(server) -> None:
    """Runs beside uvicorn; asks it to stop when an update is ready and nothing is in progress."""
    while not server.should_exit:
        await asyncio.sleep(CHECK_EVERY_SECONDS)
        try:
            if not await asyncio.to_thread(update_available):
                continue
            while not idle():
                await asyncio.sleep(15)
            log.info("a newer AllFix is on GitHub; restarting to update")
            state["restart"] = True
            server.should_exit = True
            return
        except Exception as e:  # never take the server down over an update check
            log.warning("update check failed: %s", e)
