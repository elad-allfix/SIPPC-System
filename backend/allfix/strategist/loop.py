"""One strategist turn: stream the model, run tools, persist everything, emit UI events.

History is append-only. Every assistant message is stored exactly as the API
returned it, so thinking blocks, server-tool results and compaction blocks stay
valid when the conversation continues.
"""

from __future__ import annotations

import logging
from typing import Any, AsyncIterator

from .. import store
from .models import ModelClient, spec_for
from .prompt import SYSTEM_PROMPT, project_brief
from .tools import ToolContext, run_tool, tool_list

log = logging.getLogger(__name__)

MAX_REQUESTS_PER_TURN = 30
BUDGET_NOTE = ("The tool budget for this turn is used up. Do not call more tools; give your answer "
               "now from what you have, and say what you would research next.")


def build_history(rows: list[dict]) -> list[dict]:
    """Stored rows -> API messages.

    A system message is kept only when an assistant message follows it (or it is
    last). One left behind by a failed turn is skipped, which is deterministic, so
    the history prefix stays stable from turn to turn.
    """
    out: list[dict] = []
    for i, r in enumerate(rows):
        if r["role"] == "system":
            nxt = rows[i + 1]["role"] if i + 1 < len(rows) else None
            if nxt not in (None, "assistant"):
                continue
        out.append({"role": r["role"], "content": r["content"]})
    return out


def _summarise_input(name: str, args: dict) -> str:
    if not isinstance(args, dict):
        return ""
    for key in ("query", "url", "title", "id"):
        if args.get(key):
            return str(args[key])[:160]
    if name == "read_knowledge":
        return ", ".join(args.get("ids", []))[:160]
    if name == "calculate_economics":
        return "value per click and affordable CPC"
    if name == "get_project":
        return f"stage {args['stage']}" if args.get("stage") else "project state"
    if name == "update_project":
        keys = [f["key"] for f in args.get("facts") or []] + list((args.get("profile") or {}).keys())
        return ", ".join(keys)[:160]
    return ""


def _summarise_server_result(block: dict) -> tuple[str, bool]:
    content = block.get("content")
    if isinstance(content, dict) and content.get("type", "").endswith("error"):
        return f"failed: {content.get('error_code', 'error')}", False
    if block.get("type") == "web_search_tool_result" and isinstance(content, list):
        return f"{len(content)} results", True
    if block.get("type") == "web_fetch_tool_result":
        doc = (content or {}).get("content", {}) if isinstance(content, dict) else {}
        title = doc.get("title") if isinstance(doc, dict) else None
        return f"fetched{': ' + title if title else ''}", True
    return "done", True


def _collect_sources(content: list[dict], seen: dict[str, str | None]) -> None:
    for block in content:
        for c in block.get("citations") or []:
            url = c.get("url")
            if url and url not in seen:
                seen[url] = c.get("title")


async def run_turn(client: ModelClient, project_id: str, conversation_id: str,
                   user_text: str, mode: str = "standard") -> AsyncIterator[dict]:
    spec = spec_for(mode)
    tools = tool_list(spec)
    system = [{"type": "text", "text": SYSTEM_PROMPT}]
    ctx = ToolContext(project_id=project_id, conversation_id=conversation_id)

    rows = await store.load_messages(conversation_id)
    if not rows:
        await store.rename_conversation(conversation_id, user_text.strip().splitlines()[0][:80] or "Conversation")
    await store.append_message(conversation_id, "user", [{"type": "text", "text": user_text}])
    await store.append_message(conversation_id, "system",
                               [{"type": "text", "text": await project_brief(project_id)}])

    yield {"type": "turn_start", "model": spec.model, "mode": spec.mode}
    tool_calls = 0
    budget_noted = False
    usage_total: dict[str, int] = {}
    sources: dict[str, str | None] = {}

    for _ in range(MAX_REQUESTS_PER_TURN):
        history = build_history(await store.load_messages(conversation_id))
        final: dict[str, Any] | None = None
        server_names: dict[str, str] = {}
        try:
            async for ev in client.stream_turn(spec, system, history, tools):
                t = ev["type"]
                if t in ("text", "thinking"):
                    yield ev
                elif t == "tool_input":
                    tool_calls += 1
                    if ev["name"] in ("web_search", "web_fetch"):
                        server_names[ev["id"]] = ev["name"]
                    yield {"type": "tool_start", "id": ev["id"], "name": ev["name"],
                           "summary": _summarise_input(ev["name"], ev["input"])}
                elif t == "server_tool_result":
                    block = ev["block"]
                    summary, ok = _summarise_server_result(block)
                    name = server_names.get(block.get("tool_use_id"), block.get("type", "").replace("_tool_result", ""))
                    yield {"type": "tool_end", "id": block.get("tool_use_id"), "name": name,
                           "ok": ok, "summary": summary}
                elif t == "citation":
                    if ev["url"] not in sources:
                        sources[ev["url"]] = ev.get("title")
                elif t == "final":
                    final = ev
        except Exception as e:  # API or network failure: nothing partial is stored
            log.exception("model request failed")
            yield {"type": "error", "message": _error_message(e)}
            return

        if final is None:
            yield {"type": "error", "message": "the model stream ended without a final message"}
            return
        for k, v in (final.get("usage") or {}).items():
            if isinstance(v, int):
                usage_total[k] = usage_total.get(k, 0) + v

        stop = final["stop_reason"]
        content = final["content"]
        if stop == "refusal":
            yield {"type": "error", "message": "The model declined this request. Try rephrasing it."}
            return
        tool_uses = [b for b in content if b.get("type") == "tool_use"]
        if stop == "max_tokens" and tool_uses:
            yield {"type": "error", "message": "The answer was cut off mid tool call. Try a narrower request."}
            return
        if not content:
            yield {"type": "error", "message": "The model returned an empty response."}
            return

        await store.append_message(conversation_id, "assistant", content,
                                   model=final.get("model"), mode=spec.mode, usage=final.get("usage"))
        _collect_sources(content, sources)

        if stop == "pause_turn":
            continue
        if not tool_uses:
            break

        results = []
        for block in tool_uses:
            text, is_error = await run_tool(ctx, block["name"], block.get("input"))
            results.append({"type": "tool_result", "tool_use_id": block["id"], "content": text,
                            **({"is_error": True} if is_error else {})})
            yield {"type": "tool_end", "id": block["id"], "name": block["name"], "ok": not is_error,
                   "summary": text[:200] if is_error else "done"}
        await store.append_message(conversation_id, "user", results)
        for item in ctx.saved_items:
            yield {"type": "item_saved", "item": item}
        ctx.saved_items.clear()
        if tool_calls >= _max_tool_calls() and not budget_noted:
            budget_noted = True
            await store.append_message(conversation_id, "system", [{"type": "text", "text": BUDGET_NOTE}])
    else:
        yield {"type": "error", "message": "Stopped after too many steps in one turn."}

    if sources:
        yield {"type": "sources", "sources": [{"url": u, "title": t} for u, t in sources.items()]}
    yield {"type": "done", "usage": usage_total}


def _max_tool_calls() -> int:
    from ..config import get_settings
    return get_settings().max_tool_calls_per_turn


def _error_message(e: Exception) -> str:
    import anthropic
    if isinstance(e, anthropic.AuthenticationError):
        return "The Anthropic API key is missing or invalid. Set ANTHROPIC_API_KEY."
    if isinstance(e, anthropic.RateLimitError):
        return "Rate limited by the Anthropic API. Try again shortly."
    if isinstance(e, anthropic.APIStatusError):
        return f"Anthropic API error {e.status_code}: {getattr(e, 'message', str(e))[:300]}"
    if isinstance(e, anthropic.APIConnectionError):
        return "Could not reach the Anthropic API."
    if isinstance(e, TypeError) and "api_key" in str(e).lower():
        return "The Anthropic API key is missing. Set ANTHROPIC_API_KEY."
    return f"{type(e).__name__}: {str(e)[:300]}"
