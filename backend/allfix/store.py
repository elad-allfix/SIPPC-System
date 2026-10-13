"""Persistence for projects, facts, conversations, messages, items and lessons."""

from __future__ import annotations

import json
from typing import Any
from uuid import UUID

from psycopg.types.json import Jsonb

from . import db

LABELS = ("verified", "observed", "estimate", "assumption", "hypothesis", "unknown")
KINDS = ("finding", "intent_cluster", "competitor", "economics", "website_issue", "opportunity",
         "risk", "decision", "forecast", "experiment", "question")
STATUSES = ("open", "confirmed", "refuted", "done", "dropped", "superseded")
ENTRY_PATHS = ("new_niche", "website", "ads_account")
OBJECTIVE_TYPES = ("profit", "leads", "sales", "traffic", "awareness", "unknown")
PROJECT_FIELDS = ("name", "entry_path", "objective", "objective_type", "country", "region",
                  "language", "website_url", "notes")

# Default stage for each kind of item (the strategist can override).
KIND_STAGE = {
    "finding": 3, "intent_cluster": 3, "competitor": 3, "economics": 5, "website_issue": 4,
    "opportunity": 5, "risk": 5, "decision": 6, "forecast": 6, "experiment": 6, "question": 2,
}

STAGES = [
    {"n": 1, "key": "connectivity", "title": "Secure connectivity",
     "summary": "Verified PIA and Dolphin route before any protected account access."},
    {"n": 2, "key": "understanding", "title": "Business & campaign understanding",
     "summary": "Objective, business facts, economics inputs and measurement status."},
    {"n": 3, "key": "research", "title": "Market & niche research",
     "summary": "Demand, intent clusters, competitors, offers and the results page."},
    {"n": 4, "key": "intelligence", "title": "Campaign & website intelligence",
     "summary": "How intent, keyword, ad, page and outcome connect; what breaks the chain."},
    {"n": 5, "key": "strategy", "title": "Growth & optimisation strategy",
     "summary": "Opportunities, economics and recommended moves with their evidence."},
    {"n": 6, "key": "learning", "title": "Continuous learning",
     "summary": "Decisions, forecasts, experiments, outcomes and lessons."},
    {"n": 7, "key": "control", "title": "Control center",
     "summary": "Overview of the project and what needs attention."},
]


def _clean(row: dict | None) -> dict | None:
    if row is None:
        return None
    out = {}
    for k, v in row.items():
        if isinstance(v, UUID):
            v = str(v)
        elif hasattr(v, "isoformat"):
            v = v.isoformat()
        out[k] = v
    return out


def _clean_all(rows: list[dict]) -> list[dict]:
    return [_clean(r) for r in rows]


# ---------- projects ----------

async def list_projects() -> list[dict]:
    return _clean_all(await db.fetch_all(
        """select p.*, (select count(*) from items i where i.project_id = p.id) as item_count
           from projects p order by p.updated_at desc"""))


async def create_project(data: dict) -> dict:
    fields = {k: v for k, v in data.items() if k in PROJECT_FIELDS and v is not None}
    if not fields.get("name"):
        raise ValueError("name is required")
    cols = ", ".join(fields)
    vals = ", ".join(f"%({k})s" for k in fields)
    return _clean(await db.fetch_one(f"insert into projects ({cols}) values ({vals}) returning *", fields))


async def update_project(project_id: str, data: dict) -> dict:
    fields = {k: v for k, v in data.items() if k in PROJECT_FIELDS}
    if not fields:
        return await get_project(project_id)
    sets = ", ".join(f"{k} = %({k})s" for k in fields)
    row = await db.fetch_one(
        f"update projects set {sets}, updated_at = now() where id = %(id)s returning *",
        {**fields, "id": project_id})
    if row is None:
        raise KeyError("project not found")
    return _clean(row)


async def get_project(project_id: str) -> dict | None:
    row = _clean(await db.fetch_one("select * from projects where id = %s", (project_id,)))
    if row is None:
        return None
    row["facts"] = await list_facts(project_id)
    counts = await db.fetch_all(
        """select stage, kind, count(*) as n from items
           where project_id = %s and status <> 'superseded' group by stage, kind""",
        (project_id,))
    by_stage: dict[int, dict[str, int]] = {}
    for c in counts:
        by_stage.setdefault(c["stage"], {})[c["kind"]] = c["n"]
    row["stage_counts"] = {str(s["n"]): by_stage.get(s["n"], {}) for s in STAGES}
    return row


async def delete_project(project_id: str) -> None:
    await db.execute("delete from projects where id = %s", (project_id,))


async def list_facts(project_id: str) -> list[dict]:
    return _clean_all(await db.fetch_all(
        "select key, value, label, source, updated_at from project_facts where project_id = %s order by key",
        (project_id,)))


async def set_fact(project_id: str, key: str, value: str, label: str, source: str = "") -> dict:
    if label not in LABELS:
        raise ValueError(f"label must be one of {LABELS}")
    row = await db.fetch_one(
        """insert into project_facts (project_id, key, value, label, source) values (%s, %s, %s, %s, %s)
           on conflict (project_id, key) do update set value = excluded.value, label = excluded.label,
             source = excluded.source, updated_at = now()
           returning key, value, label, source, updated_at""",
        (project_id, key.strip(), str(value), label, source))
    await db.execute("update projects set updated_at = now() where id = %s", (project_id,))
    return _clean(row)


# ---------- items ----------

def _normalise_sources(sources: Any) -> list[dict]:
    out = []
    for s in sources or []:
        if isinstance(s, str):
            out.append({"url": s} if s.startswith("http") else {"note": s})
        elif isinstance(s, dict):
            out.append({k: v for k, v in s.items() if k in ("url", "title", "note", "checked", "kb")})
    return out


async def create_item(project_id: str, data: dict, conversation_id: str | None = None) -> dict:
    kind = data.get("kind")
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {KINDS}")
    label = data.get("label", "hypothesis")
    if label not in LABELS:
        raise ValueError(f"label must be one of {LABELS}")
    stage = int(data.get("stage") or KIND_STAGE[kind])
    if not 1 <= stage <= 7:
        raise ValueError("stage must be 1-7")
    title = (data.get("title") or "").strip()
    if not title:
        raise ValueError("title is required")
    row = await db.fetch_one(
        """insert into items (project_id, stage, kind, title, body, data, label, confidence, sources,
                              conversation_id)
           values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning *""",
        (project_id, stage, kind, title, data.get("body", ""), Jsonb(data.get("data") or {}), label,
         data.get("confidence", "medium"), Jsonb(_normalise_sources(data.get("sources"))),
         conversation_id))
    await db.execute("update projects set updated_at = now() where id = %s", (project_id,))
    return _clean(row)


async def update_item(item_id: str, data: dict) -> dict:
    allowed = {"title", "body", "label", "confidence", "status", "stage", "superseded_by"}
    fields = {k: v for k, v in data.items() if k in allowed and v is not None}
    if "label" in fields and fields["label"] not in LABELS:
        raise ValueError(f"label must be one of {LABELS}")
    if "status" in fields and fields["status"] not in STATUSES:
        raise ValueError(f"status must be one of {STATUSES}")
    if "superseded_by" in fields:
        fields["status"] = "superseded"
    sets = [f"{k} = %({k})s" for k in fields]
    params: dict[str, Any] = dict(fields)
    if data.get("append_note"):
        sets.append("body = body || %(note)s")
        params["note"] = "\n\n**Update:** " + data["append_note"]
    if data.get("data"):
        sets.append("data = data || %(data)s")
        params["data"] = Jsonb(data["data"])
    if data.get("sources"):
        sets.append("sources = sources || %(sources)s")
        params["sources"] = Jsonb(_normalise_sources(data["sources"]))
    if not sets:
        raise ValueError("nothing to update")
    params["id"] = item_id
    row = await db.fetch_one(
        f"update items set {', '.join(sets)}, updated_at = now() where id = %(id)s returning *", params)
    if row is None:
        raise KeyError("item not found")
    return _clean(row)


async def list_items(project_id: str, stage: int | None = None, kind: str | None = None,
                     include_superseded: bool = False, limit: int = 200) -> list[dict]:
    return _clean_all(await db.fetch_all(
        """select * from items where project_id = %(p)s
             and (%(s)s::smallint is null or stage = %(s)s)
             and (%(k)s::text is null or kind = %(k)s)
             and (%(all)s or status <> 'superseded')
           order by stage, created_at desc limit %(lim)s""",
        {"p": project_id, "s": stage, "k": kind, "all": include_superseded, "lim": limit}))


async def get_item(item_id: str) -> dict | None:
    return _clean(await db.fetch_one("select * from items where id = %s", (item_id,)))


# ---------- lessons ----------

async def create_lesson(project_id: str | None, data: dict) -> dict:
    return _clean(await db.fetch_one(
        """insert into lessons (project_id, what_was_wrong, correction, applies_to, kb_entry_ids)
           values (%s, %s, %s, %s, %s) returning *""",
        (project_id, data["what_was_wrong"], data["correction"], data.get("applies_to", ""),
         data.get("kb_entry_ids") or [])))


async def list_lessons(project_id: str | None = None, limit: int = 20) -> list[dict]:
    """Lessons for this project plus lessons shared across projects."""
    return _clean_all(await db.fetch_all(
        """select * from lessons where project_id is null or project_id = %s
           order by created_at desc limit %s""", (project_id, limit)))


# ---------- conversations ----------

async def list_conversations(project_id: str) -> list[dict]:
    return _clean_all(await db.fetch_all(
        "select * from conversations where project_id = %s order by updated_at desc", (project_id,)))


async def create_conversation(project_id: str, title: str = "New conversation") -> dict:
    return _clean(await db.fetch_one(
        "insert into conversations (project_id, title) values (%s, %s) returning *", (project_id, title)))


async def get_conversation(conversation_id: str) -> dict | None:
    return _clean(await db.fetch_one("select * from conversations where id = %s", (conversation_id,)))


async def rename_conversation(conversation_id: str, title: str) -> None:
    await db.execute("update conversations set title = %s where id = %s", (title, conversation_id))


async def load_messages(conversation_id: str) -> list[dict]:
    rows = await db.fetch_all(
        "select seq, role, content, model, mode, usage, created_at from messages "
        "where conversation_id = %s order by seq", (conversation_id,))
    return _clean_all(rows)


async def append_message(conversation_id: str, role: str, content: list | str,
                         model: str | None = None, mode: str | None = None,
                         usage: dict | None = None) -> int:
    async with db.pool().connection() as conn:
        async with conn.transaction():
            # lock the conversation row so concurrent appends get distinct seq numbers
            await conn.execute("select id from conversations where id = %s for update", (conversation_id,))
            cur = await conn.execute(
                "select coalesce(max(seq), 0) + 1 as next from messages where conversation_id = %s",
                (conversation_id,))
            seq = (await cur.fetchone())["next"]
            await conn.execute(
                """insert into messages (conversation_id, seq, role, content, model, mode, usage)
                   values (%s, %s, %s, %s, %s, %s, %s)""",
                (conversation_id, seq, role, Jsonb(content), model, mode,
                 Jsonb(usage) if usage is not None else None))
            await conn.execute("update conversations set updated_at = now() where id = %s",
                               (conversation_id,))
    return seq


def to_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, default=str)
