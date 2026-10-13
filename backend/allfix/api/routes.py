"""HTTP API for the interface."""

from __future__ import annotations

import json
from typing import Any, Literal

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from .. import store
from ..knowledge import search as kb
from ..strategist.loop import run_turn
from ..strategist.models import spec_for

router = APIRouter(prefix="/api")


class ProjectIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    entry_path: Literal["new_niche", "website", "ads_account"] = "new_niche"
    objective: str = ""
    objective_type: Literal["profit", "leads", "sales", "traffic", "awareness", "unknown"] = "unknown"
    country: str | None = None
    region: str | None = None
    language: str | None = None
    website_url: str | None = None
    notes: str = ""


class ProjectPatch(BaseModel):
    name: str | None = None
    entry_path: Literal["new_niche", "website", "ads_account"] | None = None
    objective: str | None = None
    objective_type: Literal["profit", "leads", "sales", "traffic", "awareness", "unknown"] | None = None
    country: str | None = None
    region: str | None = None
    language: str | None = None
    website_url: str | None = None
    notes: str | None = None


class FactIn(BaseModel):
    key: str = Field(min_length=1)
    value: str
    label: Literal["verified", "observed", "estimate", "assumption", "hypothesis", "unknown"] = "assumption"
    source: str = "user"


class ItemPatch(BaseModel):
    title: str | None = None
    body: str | None = None
    label: str | None = None
    confidence: str | None = None
    status: str | None = None
    append_note: str | None = None


class ConversationIn(BaseModel):
    title: str = "New conversation"


class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=50000)
    mode: Literal["standard", "deep"] = "standard"


def _404(what: str) -> HTTPException:
    return HTTPException(status_code=404, detail=f"{what} not found")


@router.get("/health")
async def health() -> dict:
    from .. import db
    n = await db.fetch_one("select count(*) as n from kb_entries")
    return {"ok": True, "knowledge_entries": n["n"] if n else 0,
            "models": {"standard": spec_for("standard").model, "deep": spec_for("deep").model}}


@router.get("/stages")
async def stages() -> list[dict]:
    return store.STAGES


# ---------- projects ----------

@router.get("/projects")
async def list_projects() -> list[dict]:
    return await store.list_projects()


@router.post("/projects", status_code=201)
async def create_project(body: ProjectIn) -> dict:
    p = await store.create_project(body.model_dump())
    return await store.get_project(p["id"])


@router.get("/projects/{project_id}")
async def get_project(project_id: str) -> dict:
    p = await store.get_project(project_id)
    if p is None:
        raise _404("project")
    return p


@router.patch("/projects/{project_id}")
async def patch_project(project_id: str, body: ProjectPatch) -> dict:
    try:
        await store.update_project(project_id, body.model_dump(exclude_none=True))
    except KeyError:
        raise _404("project")
    return await store.get_project(project_id)


@router.delete("/projects/{project_id}", status_code=204)
async def delete_project(project_id: str) -> None:
    await store.delete_project(project_id)


@router.put("/projects/{project_id}/facts")
async def put_fact(project_id: str, body: FactIn) -> dict:
    if await store.get_project(project_id) is None:
        raise _404("project")
    return await store.set_fact(project_id, body.key, body.value, body.label, body.source)


# ---------- items ----------

@router.get("/projects/{project_id}/items")
async def list_items(project_id: str, stage: int | None = None, kind: str | None = None) -> list[dict]:
    return await store.list_items(project_id, stage, kind)


@router.patch("/items/{item_id}")
async def patch_item(item_id: str, body: ItemPatch) -> dict:
    try:
        return await store.update_item(item_id, body.model_dump(exclude_none=True))
    except KeyError:
        raise _404("item")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------- conversations ----------

@router.get("/projects/{project_id}/conversations")
async def list_conversations(project_id: str) -> list[dict]:
    return await store.list_conversations(project_id)


@router.post("/projects/{project_id}/conversations", status_code=201)
async def create_conversation(project_id: str, body: ConversationIn) -> dict:
    if await store.get_project(project_id) is None:
        raise _404("project")
    return await store.create_conversation(project_id, body.title)


@router.get("/conversations/{conversation_id}/messages")
async def conversation_messages(conversation_id: str) -> list[dict]:
    if await store.get_conversation(conversation_id) is None:
        raise _404("conversation")
    return render_messages(await store.load_messages(conversation_id))


@router.post("/conversations/{conversation_id}/chat")
async def chat(conversation_id: str, body: ChatIn, request: Request) -> StreamingResponse:
    conv = await store.get_conversation(conversation_id)
    if conv is None:
        raise _404("conversation")
    try:
        client = request.app.state.model_client_factory()
    except Exception as e:  # e.g. no API key configured
        client = None
        setup_error = f"The strategist is not configured: {str(e)[:200]}. Set ANTHROPIC_API_KEY."

    async def events():
        if client is None:
            yield f"event: error\ndata: {json.dumps({'type': 'error', 'message': setup_error})}\n\n"
            return
        try:
            async for ev in run_turn(client, conv["project_id"], conversation_id, body.message, body.mode):
                yield f"event: {ev['type']}\ndata: {json.dumps(ev, ensure_ascii=False, default=str)}\n\n"
        except Exception as e:  # last resort: tell the browser instead of hanging
            yield f"event: error\ndata: {json.dumps({'type': 'error', 'message': str(e)[:300]})}\n\n"

    return StreamingResponse(events(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


# ---------- knowledge ----------

@router.get("/knowledge/search")
async def knowledge_search(q: str, limit: int = 12, area: str | None = None) -> dict:
    return await kb.search(q, limit, area)


@router.get("/knowledge/documents")
async def knowledge_documents() -> list[dict]:
    return await kb.list_documents()


@router.get("/knowledge/{entry_id:path}")
async def knowledge_read(entry_id: str) -> dict:
    rows = await kb.read([entry_id])
    if not rows or rows[0].get("error"):
        raise _404("knowledge entry")
    return rows[0]


# ---------- rendering stored messages for display ----------

def render_messages(rows: list[dict]) -> list[dict[str, Any]]:
    """Turn stored API messages into display turns: user text, then one assistant
    turn per user message with its text, tool activity and sources."""
    turns: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    tool_names: dict[str, str] = {}
    for r in rows:
        if r["role"] == "system":
            continue
        content = r["content"] if isinstance(r["content"], list) else [{"type": "text", "text": str(r["content"])}]
        if r["role"] == "user":
            texts = [b.get("text", "") for b in content if b.get("type") == "text"]
            if texts:
                turns.append({"role": "user", "text": "\n".join(texts), "created_at": r["created_at"]})
                current = None
            for b in content:
                if b.get("type") == "tool_result" and current is not None:
                    for a in current["activity"]:
                        if a["id"] == b.get("tool_use_id"):
                            a["ok"] = not b.get("is_error", False)
            continue
        if current is None:
            current = {"role": "assistant", "text": "", "activity": [], "sources": [], "model": r.get("model"),
                       "mode": r.get("mode"), "created_at": r["created_at"]}
            turns.append(current)
        seen = {s["url"] for s in current["sources"]}
        for b in content:
            t = b.get("type")
            if t == "text":
                current["text"] += b.get("text", "")
                for c in b.get("citations") or []:
                    if c.get("url") and c["url"] not in seen:
                        seen.add(c["url"])
                        current["sources"].append({"url": c["url"], "title": c.get("title")})
            elif t in ("tool_use", "server_tool_use"):
                inp = b.get("input") or {}
                tool_names[b["id"]] = b["name"]
                summary = next((str(inp[k])[:160] for k in ("query", "url", "title", "id") if inp.get(k)), "")
                current["activity"].append({"id": b["id"], "name": b["name"], "summary": summary, "ok": True})
            elif t in ("web_search_tool_result", "web_fetch_tool_result"):
                c = b.get("content")
                if isinstance(c, dict) and str(c.get("type", "")).endswith("error"):
                    for a in current["activity"]:
                        if a["id"] == b.get("tool_use_id"):
                            a["ok"] = False
    return turns
