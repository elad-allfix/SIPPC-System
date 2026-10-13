"""HTTP API for the interface."""

from __future__ import annotations

import json
from typing import Any, Literal

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from .. import store
from ..knowledge import search as kb
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
async def health(request: Request) -> dict:
    from .. import db
    n = await db.fetch_one("select count(*) as n from kb_entries")
    backend = request.app.state.strategist.backend
    out = {"ok": True, "knowledge_entries": n["n"] if n else 0, "backend": backend,
           "models": {"standard": spec_for("standard").model, "deep": spec_for("deep").model}}
    if backend == "subscription":
        from ..strategist.subscription import STATUS
        out["subscription"] = {"api_key_source": STATUS["auth"], "rate_limit": STATUS["rate_limit"],
                               "checked_at": STATUS["checked_at"]}
    return out


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
async def create_conversation(project_id: str, body: ConversationIn, request: Request) -> dict:
    if await store.get_project(project_id) is None:
        raise _404("project")
    return await store.create_conversation(project_id, body.title, request.app.state.strategist.backend)


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
    strategist = request.app.state.strategist

    async def events():
        if conv.get("backend", "api") != strategist.backend:
            msg = (f"This conversation was started on the {conv.get('backend')} backend and AllFix now runs on "
                   f"{strategist.backend}. Start a new conversation; saved findings are kept.")
            yield f"event: error\ndata: {json.dumps({'type': 'error', 'message': msg})}\n\n"
            return
        try:
            async for ev in strategist.run_turn(conv["project_id"], conversation_id, body.message, body.mode):
                yield f"event: {ev['type']}\ndata: {json.dumps(ev, ensure_ascii=False, default=str)}\n\n"
        except Exception as e:  # last resort: tell the browser instead of hanging
            yield f"event: error\ndata: {json.dumps({'type': 'error', 'message': str(e)[:300]})}\n\n"

    return StreamingResponse(events(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


# ---------- stage 01: connectivity and Google Ads ----------

class ProfileIn(BaseModel):
    ads_customer_id: str | None = None
    login_customer_id: str | None = None
    required_country: str | None = Field(default=None, max_length=2)
    required_region: str | None = None
    vpn_profile: str | None = None
    dolphin_profile_id: str | None = None


async def _profile(project_id: str):
    from ..connectivity import profiles
    from ..connectivity.guard import Profile
    row = await profiles.get(project_id)
    if row is None:
        raise HTTPException(status_code=400, detail="Set up the connection profile first (Stage 01).")
    return Profile.from_row(row)


@router.get("/projects/{project_id}/connectivity")
async def get_connectivity(project_id: str) -> dict:
    from ..ads import importer
    from ..config import get_settings
    from ..connectivity import profiles
    s = get_settings()
    return {"profile": await profiles.get(project_id), "checks": await profiles.recent_checks(project_id, 5),
            "ads_configured": bool(s.google_oauth_client_id and s.google_oauth_client_secret and s.ads_refresh_token),
            "ads_api_version": s.ads_api_version, "snapshot": await importer.latest_snapshot(project_id)}


@router.put("/projects/{project_id}/connectivity")
async def put_connectivity(project_id: str, body: ProfileIn) -> dict:
    from ..connectivity import profiles
    if await store.get_project(project_id) is None:
        raise _404("project")
    try:
        return await profiles.upsert(project_id, body.model_dump(exclude_none=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/projects/{project_id}/connectivity/verify")
async def verify_connectivity(project_id: str) -> dict:
    from ..connectivity import get_guard, profiles
    profile = await _profile(project_id)
    v = await get_guard().verify(profile)
    await profiles.record(profile, v)
    return v.as_dict()


@router.post("/projects/{project_id}/ads/import")
async def import_ads(project_id: str, days: int = 90) -> dict:
    from ..ads.client import AdsApiError, AdsClient, AdsNotConfigured
    from ..ads.importer import run_import
    from ..connectivity import ConnectivityBlocked, get_guard, profiles
    profile = await _profile(project_id)
    try:
        async with AdsClient(profile) as client:
            result = await run_import(project_id, client, days=max(7, min(days, 365)))
    except AdsNotConfigured as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectivityBlocked as e:
        await profiles.record_last(get_guard(), profile)
        raise HTTPException(status_code=423, detail=f"Blocked by Stage 01: {e}")
    except AdsApiError as e:
        raise HTTPException(status_code=502, detail=str(e))
    return result


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
                if current.get("after_tool") and current["text"] and b.get("text"):
                    current["text"] += "\n\n"
                current["after_tool"] = False
                current["text"] += b.get("text", "")
                for c in b.get("citations") or []:
                    if c.get("url") and c["url"] not in seen:
                        seen.add(c["url"])
                        current["sources"].append({"url": c["url"], "title": c.get("title")})
            elif t in ("tool_use", "server_tool_use"):
                current["after_tool"] = True
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
    for t in turns:
        t.pop("after_tool", None)
    return turns
