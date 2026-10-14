"""Strategist backend that runs on the user's own Claude subscription.

It drives Claude through the Claude Agent SDK, which runs the official Claude Code
binary signed in with `claude login`. Usage then counts against the user's plan
instead of API billing. Anthropic allows this for a person's own use only, so this
backend refuses to serve other machines unless ALLFIX_SINGLE_USER is set.

Claude Code runs the tool loop itself. AllFix exposes its own tools (knowledge,
project memory, economics) as an in-process MCP server and allows only those plus
WebSearch and WebFetch. Every other Claude Code tool is switched off.

The SDK starts a subprocess. On Windows that needs the proactor event loop, while
the async Postgres driver needs the selector loop, so each turn runs the SDK on
its own thread and loop. Database work is sent back to the main loop.
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, AsyncIterator, Awaitable, Callable

from .. import db, store
from ..config import get_settings
from .loop import BUDGET_NOTE, _summarise_input
from .prompt import SYSTEM_PROMPT, project_brief
from .tools import CLIENT_TOOLS, ToolContext, run_tool_blocks

log = logging.getLogger(__name__)

MCP_NAME = "allfix"
MCP_PREFIX = f"mcp__{MCP_NAME}__"
WEB_TOOLS = ["WebSearch", "WebFetch"]
MAX_AGENT_TURNS = 60
LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}
SAVING_TOOLS = {"save_item", "update_item", "update_project", "record_lesson"}
SAVE_ALLOWANCE = 10

# Environment overrides for the agent process. An empty ANTHROPIC_API_KEY makes Claude
# Code ignore any key in the environment, so usage can't silently move to API billing.
# The session ids only exist when AllFix itself runs inside a Claude Code session.
# When AllFix itself was started from inside a Claude Code session (a terminal or Remote Control),
# that session's settings would leak into the strategist: its memory folders, CLAUDE.md folders,
# messaging, skills and session id. The strategist gets none of them.
INHERITED_SESSION_VARS = (
    "CLAUDECODE", "CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_REMOTE_SESSION_ID", "CLAUDE_CODE_CHILD_SESSION",
    "CLAUDE_CODE_PROJECTS_SESSION", "CLAUDE_ADDITIONAL_DIRECTORIES", "CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD",
    "CLAUDE_COWORK_MEMORY_PATH_OVERRIDE", "CLAUDE_MEMORY_STORES", "CLAUDE_CODE_MESSAGING_SOCKET",
    "CLAUDE_CODE_MESSAGING_TOKEN", "CLAUDE_CODE_SKILL_PROPOSALS", "CLAUDE_CODE_SYNC_PLUGINS", "CLAUDE_CODE_SYNC_SKILLS",
    "CLAUDE_CODE_SYNC_SESSION_REFS", "CLAUDE_CODE_COORDINATOR_EXTRA_TOOLS", "CLAUDE_CODE_TERMINAL_MCP_TOOLS",
    "CLAUDE_AUTO_BACKGROUND_TASKS", "CLAUDE_CODE_SILENT_TURN_REMINDER", "CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION",
    "CLAUDE_CODE_ENABLE_REMOTE_RECAP", "CLAUDE_AFTER_LAST_COMPACT", "CLAUDE_CODE_ARTIFACT_ASSETS", "CLAUDE_PID",
    "CLAUDE_EFFORT",
)
AGENT_ENV = {"ANTHROPIC_API_KEY": "", **{k: "" for k in INHERITED_SESSION_VARS}}

# The last authentication and plan-limit status seen, for /api/health.
STATUS: dict[str, Any] = {"backend": "subscription", "auth": None, "rate_limit": None, "checked_at": None}

_locks: dict[str, asyncio.Lock] = {}


def display_name(tool_name: str) -> str:
    if tool_name.startswith(MCP_PREFIX):
        return tool_name[len(MCP_PREFIX):]
    return {"WebSearch": "web_search", "WebFetch": "web_fetch"}.get(tool_name, tool_name)


def guard_error() -> str | None:
    """Policy guard: the subscription backend is for the subscriber's own use."""
    s = get_settings()
    if s.host not in LOCAL_HOSTS and not s.allfix_single_user:
        return ("The subscription backend only serves this computer (HOST=127.0.0.1), because a Claude "
                "plan is for your own use. Set STRATEGIST_BACKEND=api to serve others, or "
                "ALLFIX_SINGLE_USER=true if only you use this server.")
    return None


def _text_of(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text")
    return "" if content is None else str(content)


def _limit_message(info: Any) -> str:
    resets = getattr(info, "resets_at", None)
    when = ""
    if resets:
        when = " It resets at " + datetime.fromtimestamp(resets, tz=timezone.utc).strftime("%H:%M UTC on %d %b") + "."
    kind = (getattr(info, "rate_limit_type", None) or "usage").replace("_", " ")
    return f"Your Claude plan's {kind} limit is reached, so the strategist can't run right now.{when}"


async def history_seed(conversation_id: str, limit_chars: int = 12000) -> str:
    """A plain-text recap of earlier turns, used when the agent session can't be resumed."""
    from ..api.routes import render_messages
    turns = render_messages(await store.load_messages(conversation_id))
    lines: list[str] = []
    for t in turns:
        who = "User" if t["role"] == "user" else "Strategist"
        lines.append(f"{who}: {t['text'].strip()}")
    text = "\n\n".join(lines)
    return text[-limit_chars:]


class PgSessionStore:
    """Keeps a copy of each agent transcript in Postgres (the SDK's SessionStore protocol).

    Called on the agent thread; the database work runs on the main loop.
    """

    def __init__(self, call_main: Callable[[Awaitable[Any]], Awaitable[Any]]):
        self._call = call_main

    async def append(self, key: dict, entries: list[dict]) -> None:
        rows = [(key["project_key"], key["session_id"], key.get("subpath") or "", e.get("uuid"),
                 json.dumps(e, ensure_ascii=False)) for e in entries]
        await self._call(_append_rows(rows))

    async def load(self, key: dict) -> list[dict] | None:
        return await self._call(_load_rows(key["session_id"], key.get("subpath") or ""))


async def _append_rows(rows: list[tuple]) -> None:
    async with db.pool().connection() as conn:
        async with conn.cursor() as cur:
            await cur.executemany(
                """insert into agent_transcripts (project_key, session_id, subpath, uuid, entry)
                   values (%s, %s, %s, %s, %s::jsonb) on conflict do nothing""", rows)


async def _load_rows(session_id: str, subpath: str) -> list[dict] | None:
    rows = await db.fetch_all(
        "select entry from agent_transcripts where session_id = %s and subpath = %s order by seq",
        (session_id, subpath))
    return [r["entry"] for r in rows] or None


@dataclass
class _Turn:
    """State shared between the main loop and the agent thread for one turn."""
    main: asyncio.AbstractEventLoop
    queue: asyncio.Queue
    stop: threading.Event = field(default_factory=threading.Event)

    def emit(self, ev: dict | None) -> None:
        self.main.call_soon_threadsafe(self.queue.put_nowait, ev)

    def call_main(self, coro: Awaitable[Any]) -> Awaitable[Any]:
        return asyncio.wrap_future(asyncio.run_coroutine_threadsafe(coro, self.main))


class SubscriptionStrategist:
    """One strategist turn through the Agent SDK. Yields the same UI events as the API backend."""

    def __init__(self, cli_path: str | None = None, options_hook: Callable[[Any], None] | None = None):
        self.cli_path = cli_path or get_settings().claude_cli_path
        self.options_hook = options_hook  # tests use this to inspect or adjust the options

    async def run_turn(self, project_id: str, conversation_id: str, user_text: str,
                       mode: str = "standard") -> AsyncIterator[dict]:
        problem = guard_error()
        if problem:
            yield {"type": "error", "message": problem}
            return
        lock = _locks.setdefault(conversation_id, asyncio.Lock())
        if lock.locked():
            yield {"type": "error", "message": "This conversation is still working on the previous message."}
            return
        async with lock:
            async for ev in self._run(project_id, conversation_id, user_text, mode):
                yield ev

    async def _run(self, project_id: str, conversation_id: str, user_text: str, mode: str) -> AsyncIterator[dict]:
        from .models import spec_for
        spec = spec_for(mode)
        conv = await store.get_conversation(conversation_id)
        rows = await store.load_messages(conversation_id)
        if not rows:
            await store.rename_conversation(conversation_id, user_text.strip().splitlines()[0][:80] or "Conversation")
        resume = conv.get("agent_session_id")
        seed = "" if resume or not rows else await history_seed(conversation_id)
        brief = await project_brief(project_id)
        await store.append_message(conversation_id, "user", [{"type": "text", "text": user_text}])

        turn = _Turn(main=asyncio.get_running_loop(), queue=asyncio.Queue())
        ctx = ToolContext(project_id=project_id, conversation_id=conversation_id)
        prompt = _compose_prompt(brief, user_text, seed)
        thread = threading.Thread(
            target=_thread_main,
            args=(self, turn, ctx, spec, conversation_id, prompt, resume, brief, user_text, rows),
            name=f"allfix-agent-{conversation_id[:8]}", daemon=True)
        yield {"type": "turn_start", "model": spec.model, "mode": spec.mode, "backend": "subscription"}
        thread.start()
        try:
            while True:
                ev = await turn.queue.get()
                if ev is None:
                    break
                yield ev
        finally:
            # Stop pressed or the browser went away: interrupt the agent and let it wind down.
            turn.stop.set()
            await asyncio.to_thread(thread.join, 30)


def _compose_prompt(brief: str, user_text: str, seed: str) -> str:
    parts = [f"<project_brief>\n{brief}\n</project_brief>"]
    if seed:
        parts.append("<earlier_conversation note=\"recap; the original session could not be resumed\">\n"
                     f"{seed}\n</earlier_conversation>")
    parts.append(user_text)
    return "\n\n".join(parts)


def _thread_main(strategist: SubscriptionStrategist, turn: _Turn, *args) -> None:
    factory = asyncio.ProactorEventLoop if sys.platform == "win32" else asyncio.SelectorEventLoop
    try:
        asyncio.run(_agent_turn(strategist, turn, *args), loop_factory=factory)
    except Exception as e:  # anything unexpected still reaches the browser
        log.exception("agent turn failed")
        turn.emit({"type": "error", "message": f"{type(e).__name__}: {str(e)[:300]}"})
    finally:
        turn.emit(None)


def _build_mcp_server(turn: _Turn, ctx: ToolContext):
    from claude_agent_sdk import create_sdk_mcp_server, tool

    def make(defn: dict):
        name = defn["name"]

        async def handler(args: dict) -> dict:
            blocks, is_error = await turn.call_main(run_tool_blocks(ctx, name, args))
            for item in list(ctx.saved_items):
                turn.emit({"type": "item_saved", "item": item})
            ctx.saved_items.clear()
            return {"content": blocks, **({"is_error": True} if is_error else {})}

        return tool(name, defn["description"], defn["input_schema"])(handler)

    return create_sdk_mcp_server(MCP_NAME, "1.0.0", [make(d) for d in CLIENT_TOOLS])


def build_options(strategist: SubscriptionStrategist, turn: _Turn, ctx: ToolContext, spec, resume: str | None):
    from claude_agent_sdk import ClaudeAgentOptions, HookMatcher

    settings = get_settings()
    settings.agent_workdir.mkdir(parents=True, exist_ok=True)
    calls = {"n": 0}

    async def budget(input_data, tool_use_id, context):  # PreToolUse hook: cap tool calls per turn
        calls["n"] += 1
        name = display_name(str((input_data or {}).get("tool_name", "")))
        limit = settings.max_tool_calls_per_turn
        # Research stops a little before the cap; saving stays open past it, so findings are never lost.
        if name in SAVING_TOOLS:
            ok = calls["n"] <= limit + SAVE_ALLOWANCE
        else:
            ok = calls["n"] <= limit - SAVE_ALLOWANCE // 2
        if ok:
            return {}
        return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                       "permissionDecisionReason": BUDGET_NOTE}}

    allowed = WEB_TOOLS + [MCP_PREFIX + d["name"] for d in CLIENT_TOOLS]
    opts = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        model=spec.model,
        effort=spec.effort,
        tools=list(WEB_TOOLS),
        allowed_tools=allowed,
        mcp_servers={MCP_NAME: _build_mcp_server(turn, ctx)},
        strict_mcp_config=True,
        setting_sources=[],
        skills=[],
        permission_mode="dontAsk",
        include_partial_messages=True,
        cwd=str(settings.agent_workdir),
        max_turns=MAX_AGENT_TURNS,
        resume=resume,
        session_store=PgSessionStore(turn.call_main),
        env=dict(AGENT_ENV),
        hooks={"PreToolUse": [HookMatcher(matcher=None, hooks=[budget])]},
        cli_path=strategist.cli_path,
    )
    if strategist.options_hook:
        strategist.options_hook(opts)
    return opts


async def _agent_turn(strategist: SubscriptionStrategist, turn: _Turn, ctx: ToolContext, spec,
                      conversation_id: str, prompt: str, resume: str | None, brief: str,
                      user_text: str, prior_rows: list) -> None:
    try:
        await _agent_session(strategist, turn, ctx, spec, conversation_id, prompt, resume)
    except _ResumeFailed:
        # The stored session is gone or unreadable: start a new one seeded with a recap.
        log.warning("could not resume agent session %s; starting a new one", resume)
        seed = await turn.call_main(history_seed(conversation_id))
        await turn.call_main(store.set_agent_session(conversation_id, None))
        await _agent_session(strategist, turn, ctx, spec, conversation_id,
                             _compose_prompt(brief, user_text, seed), None)


class _ResumeFailed(Exception):
    pass


async def _agent_session(strategist: SubscriptionStrategist, turn: _Turn, ctx: ToolContext, spec,
                         conversation_id: str, prompt: str, resume: str | None) -> None:
    from claude_agent_sdk import (AssistantMessage, ClaudeSDKClient, RateLimitEvent, ResultMessage,
                                  StreamEvent, SystemMessage, TextBlock, ToolResultBlock, ToolUseBlock,
                                  UserMessage)

    options = build_options(strategist, turn, ctx, spec, resume)
    pending: dict[str, dict] = {}       # tool_use id -> {name, input}
    sources: dict[str, str | None] = {}
    got_output = False
    usage: dict[str, Any] = {}

    async def watch_stop(client) -> None:
        while not turn.stop.is_set():
            await asyncio.sleep(0.3)
        try:
            await client.interrupt()
        except Exception:
            pass

    try:
        async with ClaudeSDKClient(options) as client:
            watcher = asyncio.create_task(watch_stop(client))
            try:
                await client.query(prompt)
                async for msg in client.receive_response():
                    if isinstance(msg, StreamEvent):
                        if msg.parent_tool_use_id:
                            continue
                        e = msg.event
                        if e.get("type") == "content_block_delta":
                            d = e.get("delta", {})
                            if d.get("type") == "text_delta":
                                got_output = True
                                turn.emit({"type": "text", "text": d.get("text", "")})
                            elif d.get("type") == "thinking_delta":
                                turn.emit({"type": "thinking", "text": d.get("thinking", "")})
                    elif isinstance(msg, SystemMessage):
                        if msg.subtype == "init":
                            source = msg.data.get("apiKeySource")
                            STATUS.update(auth=source, checked_at=datetime.now(timezone.utc).isoformat())
                            if source not in (None, "none"):
                                turn.emit({"type": "error", "message":
                                           f"Claude Code is using an API key ({source}) instead of your Claude "
                                           "subscription, so AllFix stopped before using it. Remove that key "
                                           "or set STRATEGIST_BACKEND=api."})
                                await client.interrupt()
                                return
                            sid = msg.data.get("session_id")
                            if sid:
                                await turn.call_main(store.set_agent_session(conversation_id, sid))
                    elif isinstance(msg, RateLimitEvent):
                        info = msg.rate_limit_info
                        STATUS["rate_limit"] = getattr(info, "raw", None) or {"status": info.status}
                        if info.status == "rejected":
                            turn.emit({"type": "error", "message": _limit_message(info)})
                    elif isinstance(msg, AssistantMessage):
                        if msg.parent_tool_use_id:
                            continue
                        blocks = []
                        for b in msg.content:
                            if isinstance(b, TextBlock) and b.text:
                                blocks.append({"type": "text", "text": b.text})
                            elif isinstance(b, ToolUseBlock):
                                name = display_name(b.name)
                                pending[b.id] = {"name": name, "input": b.input}
                                blocks.append({"type": "tool_use", "id": b.id, "name": name, "input": b.input})
                                turn.emit({"type": "tool_start", "id": b.id, "name": name,
                                           "summary": _summarise_input(name, b.input)})
                        if blocks:
                            got_output = True
                            await turn.call_main(store.append_message(
                                conversation_id, "assistant", blocks, model=msg.model, mode=spec.mode))
                    elif isinstance(msg, UserMessage):
                        if msg.parent_tool_use_id or not isinstance(msg.content, list):
                            continue
                        results = []
                        for b in msg.content:
                            if not isinstance(b, ToolResultBlock):
                                continue
                            call = pending.pop(b.tool_use_id, {"name": "tool", "input": {}})
                            text = _text_of(b.content)
                            ok = not b.is_error
                            summary = "done" if ok else text[:200]
                            if call["name"] == "web_search" and ok:
                                summary = _search_summary(msg.tool_use_result)
                            if call["name"] == "web_fetch" and ok and call["input"].get("url"):
                                sources.setdefault(call["input"]["url"], None)
                            results.append({"type": "tool_result", "tool_use_id": b.tool_use_id,
                                            "content": text[:4000], **({"is_error": True} if not ok else {})})
                            turn.emit({"type": "tool_end", "id": b.tool_use_id, "name": call["name"],
                                       "ok": ok, "summary": summary})
                        if results:
                            await turn.call_main(store.append_message(conversation_id, "user", results))
                    elif isinstance(msg, ResultMessage):
                        usage = {"num_turns": msg.num_turns, "duration_ms": msg.duration_ms,
                                 "nominal_cost_usd": msg.total_cost_usd, **(msg.usage or {})}
                        if msg.is_error:
                            if resume and not got_output:
                                raise _ResumeFailed()
                            turn.emit({"type": "error", "message": _result_error(msg)})
            finally:
                watcher.cancel()
    except _ResumeFailed:
        raise
    except Exception as e:
        if resume and not got_output and not turn.stop.is_set():
            raise _ResumeFailed() from e
        if turn.stop.is_set():
            return
        raise

    if sources:
        turn.emit({"type": "sources", "sources": [{"url": u, "title": t} for u, t in sources.items()]})
    turn.emit({"type": "done", "usage": usage})


def _search_summary(result: Any) -> str:
    if isinstance(result, dict):
        res = result.get("results")
        if isinstance(res, list):
            n = 0
            for r in res:
                if isinstance(r, dict) and isinstance(r.get("content"), list):
                    n += len(r["content"])
            if n:
                return f"{n} results"
    return "done"


def _result_error(msg: Any) -> str:
    sub = getattr(msg, "subtype", "")
    if sub == "error_max_turns":
        return "Stopped after too many steps in one turn. Ask again to continue."
    status = getattr(msg, "api_error_status", None)
    detail = "; ".join(getattr(msg, "errors", None) or []) or (getattr(msg, "result", None) or "")
    if status == 429 or "limit" in detail.lower():
        return f"Your Claude plan's usage limit was reached. {detail[:200]}".strip()
    return f"The strategist stopped with an error ({sub or status}). {detail[:300]}".strip()
