"""Persistence for projects, facts, conversations, messages, items and lessons."""

from __future__ import annotations

from datetime import date

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

# The growth plan every project gets: qualified traffic at the lowest cost, whatever the objective.
# Saved as opportunity items (stage 5) whose data.plan_part names the part.
PLAN_PARTS = {
    "keywords_add": "Keywords to add",
    "keywords_cut": "Searches to cut or bid down",
    "bids_budgets": "Bids and budgets",
    "settings": "Settings (match types, locations, schedule, networks)",
    "ads": "Ads to add or change",
    "website": "Website changes",
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
           from projects p where p.deleted_at is null order by p.updated_at desc"""))


def is_due(item: dict, today: date | None = None) -> bool:
    """An open forecast or experiment whose review date has passed and that has no outcome yet."""
    data = item.get("data") or {}
    if item.get("kind") not in ("forecast", "experiment") or item.get("status", "open") != "open" or data.get("outcome"):
        return False
    try:
        return date.fromisoformat(str(data.get("review_after"))) <= (today or date.today())
    except ValueError:
        return False


async def overview(project_id: str | None = None) -> list[dict]:
    """Every project with its main details and what it needs next, for the projects page.
    Deterministic: built from the saved items, files and conversations, no model call, nothing invented."""
    projects = _clean_all(await db.fetch_all(
        """select p.*,
                  (select count(*) from project_files f where f.project_id = p.id) as file_count,
                  (select count(*) from conversations c where c.project_id = p.id
                     and exists (select 1 from messages m where m.conversation_id = c.id)) as conversation_count,
                  greatest(p.updated_at,
                           (select max(c.updated_at) from conversations c where c.project_id = p.id),
                           (select max(f.created_at) from project_files f where f.project_id = p.id),
                           (select max(i.updated_at) from items i where i.project_id = p.id)) as last_activity
           from projects p where (%(pid)s::uuid is null and p.deleted_at is null) or p.id = %(pid)s::uuid
           order by p.updated_at desc""", {"pid": project_id}))
    counts = await db.fetch_all(
        """select project_id, stage, kind, count(*) as n from items where status <> 'superseded'
             and (%(pid)s::uuid is null or project_id = %(pid)s::uuid)
           group by project_id, stage, kind""", {"pid": project_id})
    # Only the kinds that can become a need, and only open ones: small even with many items.
    open_items = _clean_all(await db.fetch_all(
        """select id, project_id, stage, kind, title, label, confidence, status, data from items
           where status = 'open' and kind in ('forecast', 'experiment', 'question', 'website_issue', 'risk', 'decision', 'finding')
             and (%(pid)s::uuid is null or project_id = %(pid)s::uuid)
           order by created_at desc""", {"pid": project_id}))
    by_kind: dict[str, dict[str, int]] = {}
    stages: dict[str, set] = {}
    for r in counts:
        pid = str(r["project_id"])
        by_kind.setdefault(pid, {})
        by_kind[pid][r["kind"]] = by_kind[pid].get(r["kind"], 0) + r["n"]
        stages.setdefault(pid, set()).add(r["stage"])
    by_project: dict[str, list[dict]] = {}
    for i in open_items:
        by_project.setdefault(i["project_id"], []).append(i)
    today = date.today()
    out = []
    for p in projects:
        mine = by_project.get(p["id"], [])
        of = lambda *kinds: [i for i in mine if i["kind"] in kinds]  # noqa: E731
        firm = lambda i: i["label"] in ("verified", "observed")  # noqa: E731
        needs: list[dict] = []
        if not p["conversation_count"]:
            needs.append({"kind": "do", "text": "Run the account check on the report exports" if p["entry_path"] == "ads_account"
                          else "Start the first research conversation"})
        if p["entry_path"] == "ads_account" and not p["file_count"]:
            needs.append({"kind": "do", "text": "Upload the account's report exports"})
        if p["entry_path"] != "new_niche" and not p.get("website_url"):
            needs.append({"kind": "do", "text": "Add the website address"})
        ref = lambda i: {"item_id": i["id"], "stage": i["stage"]}  # noqa: E731
        needs += [{"kind": "fix", "text": i["title"], **ref(i)} for i in of("website_issue") if firm(i)]
        needs += [{"kind": "risk", "text": i["title"], **ref(i)} for i in of("risk") if firm(i)][:1]
        needs += [{"kind": "check", "text": i["title"], **ref(i)} for i in mine if is_due(i, today)]
        needs += [{"kind": "answer", "text": i["title"], **ref(i)} for i in of("question")]
        plan = next(iter(of("decision")), None)
        kinds = by_kind.get(p["id"], {})
        out.append({**p, "item_counts": kinds, "item_total": sum(kinds.values()),
                    "stages_with_items": sorted(stages.get(p["id"], set())),
                    "plan": plan["title"] if plan else None, "needs": needs,
                    "findings": _findings(of("website_issue", "risk", "finding")),
                    "missing": [n for n in needs if n["kind"] in ("answer", "do", "check")]})
    return out


FINDING_RANK = {"website_issue": 0, "risk": 1, "finding": 2}
CONFIDENCE_RANK = {"high": 0, "medium": 1, "low": 2}


def _findings(items: list[dict]) -> list[dict]:
    """What the strategist found that the owner should know or change: firm (verified or observed) first,
    then by confidence, kind and stage (measurement and business findings before campaign ones).
    Items arrive newest first, and the sort keeps that order within a tie."""
    firm = lambda i: i["label"] in ("verified", "observed")  # noqa: E731
    ranked = sorted(items, key=lambda i: (not firm(i), CONFIDENCE_RANK.get(i.get("confidence"), 1),
                                          FINDING_RANK[i["kind"]], i["stage"]))
    return [{"kind": i["kind"], "text": i["title"], "firm": firm(i), "item_id": i["id"], "stage": i["stage"]}
            for i in ranked]


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
    """Delete forever: only a project already in the recycle bin."""
    await db.execute("delete from projects where id = %s and deleted_at is not null", (project_id,))


async def trash_project(project_id: str) -> bool:
    """Move to the recycle bin; everything stays until it is deleted forever."""
    row = await db.fetch_one("update projects set deleted_at = now() where id = %s and deleted_at is null returning id",
                             (project_id,))
    return row is not None


async def restore_project(project_id: str) -> bool:
    row = await db.fetch_one("update projects set deleted_at = null where id = %s and deleted_at is not null returning id",
                             (project_id,))
    return row is not None


async def list_trash() -> list[dict]:
    return _clean_all(await db.fetch_all(
        """select id, name, country, region, deleted_at,
                  (select count(*) from items i where i.project_id = p.id) as item_count
           from projects p where deleted_at is not null order by deleted_at desc"""))


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


def item_stage(kind: str, stage: int) -> int:
    """Stage 1 (Connection) and 7 (Control) hold no items of their own: a measurement or tracking
    item asked for Stage 1 goes to Business (2), anything asked for Control to its kind's stage."""
    if not 1 <= stage <= 7:
        raise ValueError("stage must be 1-7")
    if stage == 1:
        return 2 if kind in ("finding", "risk", "question", "economics") else KIND_STAGE[kind]
    if stage == 7:
        return KIND_STAGE[kind]
    return stage


async def create_item(project_id: str, data: dict, conversation_id: str | None = None) -> dict:
    kind = data.get("kind")
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {KINDS}")
    label = data.get("label", "hypothesis")
    if label not in LABELS:
        raise ValueError(f"label must be one of {LABELS}")
    stage = item_stage(kind, int(data.get("stage") or KIND_STAGE[kind]))
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


VERDICT_STATUS = {"hit": "confirmed", "miss": "refuted", "partial": "done", "unscorable": "done"}


async def score_item(item_id: str, actual: str, verdict: str, evidence: str = "") -> dict:
    """Record what happened to a forecast or experiment, as the user saw it, and close it."""
    if verdict not in VERDICT_STATUS:
        raise ValueError(f"verdict must be one of {tuple(VERDICT_STATUS)}")
    cur = await db.fetch_one("select kind from items where id = %s", (item_id,))
    if cur is None:
        raise KeyError("item not found")
    if cur["kind"] not in ("forecast", "experiment"):
        raise ValueError("only forecasts and experiments are scored")
    outcome = {"actual": actual, "verdict": verdict, "evidence": evidence or "entered by the user",
               "scored_at": date.today().isoformat(), "scored_by": "user"}
    return await update_item(item_id, {"status": VERDICT_STATUS[verdict], "data": {"outcome": outcome}})


async def update_item(item_id: str, data: dict) -> dict:
    allowed = {"title", "body", "label", "confidence", "status", "stage", "superseded_by"}
    fields = {k: v for k, v in data.items() if k in allowed and v is not None}
    if "label" in fields and fields["label"] not in LABELS:
        raise ValueError(f"label must be one of {LABELS}")
    if "status" in fields and fields["status"] not in STATUSES:
        raise ValueError(f"status must be one of {STATUSES}")
    if "superseded_by" in fields:
        fields["status"] = "superseded"
    if "stage" in fields:
        cur = await db.fetch_one("select kind from items where id = %s", (item_id,))
        if cur:
            fields["stage"] = item_stage(cur["kind"], int(fields["stage"]))
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
    # The project changed too: the interface reloads a stage's items when the project's timestamp moves.
    await db.execute("update projects set updated_at = now() where id = %s", (row["project_id"],))
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


async def create_conversation(project_id: str, title: str = "New conversation",
                              backend: str | None = None) -> dict:
    if backend is None:
        from .config import get_settings
        backend = get_settings().strategist_backend
    return _clean(await db.fetch_one(
        "insert into conversations (project_id, title, backend) values (%s, %s, %s) returning *",
        (project_id, title, backend)))


async def set_agent_session(conversation_id: str, session_id: str | None) -> None:
    await db.execute("update conversations set agent_session_id = %s where id = %s", (session_id, conversation_id))


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


# ---------- files ----------

FILE_COLUMNS = "id, project_id, name, mime, size_bytes, created_at"


async def add_file(project_id: str, name: str, mime: str, content: bytes) -> dict:
    return _clean(await db.fetch_one(
        f"insert into project_files (project_id, name, mime, size_bytes, content) values (%s, %s, %s, %s, %s) "
        f"returning {FILE_COLUMNS}", (project_id, name, mime, len(content), content)))


async def list_files(project_id: str) -> list[dict]:
    return _clean_all(await db.fetch_all(
        f"select {FILE_COLUMNS} from project_files where project_id = %s order by created_at desc", (project_id,)))


async def get_file(file_id: str, project_id: str) -> dict | None:
    """The file with its content, only if it belongs to the project."""
    try:
        UUID(str(file_id))
    except ValueError:
        return None
    row = await db.fetch_one(f"select {FILE_COLUMNS}, content from project_files where id = %s and project_id = %s",
                             (file_id, project_id))
    if row is None:
        return None
    content = bytes(row.pop("content"))
    out = _clean(row)
    out["content"] = content
    return out


async def delete_file(file_id: str, project_id: str) -> None:
    try:
        UUID(str(file_id))
    except ValueError:
        return
    await db.execute("delete from project_files where id = %s and project_id = %s", (file_id, project_id))


# ---------- growth plan ----------

async def growth_plan(project_id: str) -> dict:
    """The project's growth plan, part by part, from its open opportunity items."""
    rows = _clean_all(await db.fetch_all(
        """select * from items where project_id = %s and kind = 'opportunity'
           and data ? 'plan_part' and status not in ('dropped', 'superseded')
           order by created_at""", (project_id,)))
    parts = [{"key": k, "title": t, "items": [r for r in rows if r["data"].get("plan_part") == k]}
             for k, t in PLAN_PARTS.items()]
    missing = [p["key"] for p in parts if not p["items"]]
    return {"parts": parts, "missing": missing, "complete": not missing,
            "updated_at": max((r["updated_at"] for r in rows), default=None)}
