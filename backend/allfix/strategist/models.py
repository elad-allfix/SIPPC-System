"""Model access behind a small interface, so the strategist is not tied to one model.

`ModelClient.stream_turn` takes a fully built request (system, messages, tools)
and yields stream events, ending with a `final` event that carries the complete
assistant message as plain JSON-able content blocks. The Anthropic
implementation is the only one today; tests use a scripted fake.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, AsyncIterator, Protocol

import anthropic

from ..config import get_settings


@dataclass(frozen=True)
class ModelSpec:
    mode: str
    model: str
    effort: str
    web_search: str = "web_search_20260209"
    web_fetch: str = "web_fetch_20260209"


def spec_for(mode: str) -> ModelSpec:
    s = get_settings()
    if mode == "deep":
        return ModelSpec("deep", s.model_deep, s.effort_deep)
    return ModelSpec("standard", s.model_standard, s.effort_standard)


class ModelClient(Protocol):
    def stream_turn(self, spec: ModelSpec, system: list[dict], messages: list[dict],
                    tools: list[dict]) -> AsyncIterator[dict]: ...


BETAS = ["server-side-fallback-2026-07-01", "compact-2026-01-12"]


class AnthropicModelClient:
    """Claude via the official SDK: streaming, adaptive thinking, refusal fallback, compaction."""

    def __init__(self, api_key: str | None = None):
        key = api_key or get_settings().anthropic_api_key
        self._client = anthropic.AsyncAnthropic(api_key=key) if key else anthropic.AsyncAnthropic()

    async def stream_turn(self, spec: ModelSpec, system: list[dict], messages: list[dict],
                          tools: list[dict]) -> AsyncIterator[dict]:
        async with self._client.beta.messages.stream(
            model=spec.model,
            max_tokens=64000,
            system=system,
            messages=messages,
            tools=tools,
            thinking={"type": "adaptive", "display": "summarized"},
            output_config={"effort": spec.effort},
            betas=BETAS,
            fallbacks="default",
            context_management={"edits": [{"type": "compact_20260112"}]},
            cache_control={"type": "ephemeral"},
        ) as stream:
            async for event in stream:
                if getattr(event, "type", None) == "content_block_stop":
                    # Tool inputs arrive as JSON deltas; report them once complete.
                    snapshot = stream.current_message_snapshot.content
                    if event.index < len(snapshot):
                        block = snapshot[event.index]
                        if getattr(block, "type", None) in ("server_tool_use", "tool_use"):
                            yield {"type": "tool_input", "name": block.name, "id": block.id,
                                   "input": block.input if isinstance(block.input, dict) else {}}
                    continue
                out = _translate(event)
                if out is not None:
                    yield out
            final = await stream.get_final_message()
        yield {
            "type": "final",
            "content": [b.model_dump(mode="json", exclude_none=True) for b in final.content],
            "stop_reason": final.stop_reason,
            "stop_details": final.stop_details.model_dump(mode="json") if getattr(final, "stop_details", None) else None,
            "model": final.model,
            "usage": final.usage.model_dump(mode="json", exclude_none=True) if final.usage else None,
        }


def _translate(event: Any) -> dict | None:
    """Reduce raw stream events to the few the interface needs."""
    etype = getattr(event, "type", None)
    if etype == "content_block_start":
        block = event.content_block
        btype = getattr(block, "type", None)
        if btype == "server_tool_use":
            return {"type": "server_tool_start", "name": block.name, "id": block.id}
        if btype == "tool_use":
            return {"type": "tool_call_start", "name": block.name, "id": block.id}
        if btype in ("web_search_tool_result", "web_fetch_tool_result"):
            return {"type": "server_tool_result", "block": block.model_dump(mode="json", exclude_none=True)}
        return None
    if etype == "content_block_delta":
        delta = event.delta
        dtype = getattr(delta, "type", None)
        if dtype == "text_delta":
            return {"type": "text", "text": delta.text}
        if dtype == "thinking_delta":
            return {"type": "thinking", "text": delta.thinking}
        if dtype == "citations_delta":
            c = delta.citation
            url = getattr(c, "url", None)
            if url:
                return {"type": "citation", "url": url, "title": getattr(c, "title", None)}
    return None
