"""Stage views: a short visual summary of one stage, written by the model from what is saved there.

The stage panel used to list every saved item as a card of text. A stage view keeps only what
the owner needs to know and says it in pictures that match the subject: an ad looks like an ad,
a landing page like a browser window, searches like search bars, money with a money icon.

The model picks from a fixed set of block types and icons (VIEW_SPEC) and may only use numbers
that appear in the saved items. The view is stored with a fingerprint of the items it was written
from; when the stage changes, the next visit writes a new one in the background while the old one
stays on screen.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import re
import sys
import threading
import time
from typing import Any, Awaitable, Callable

from .. import db, store
from ..config import get_settings

log = logging.getLogger(__name__)

VERSION = "1"  # bump when the prompt or the block set changes, so stored views are rewritten
VIEW_STAGES = {2, 3, 4, 5, 6}
CLOSED = {"superseded", "dropped", "done", "refuted"}

ICONS = ["money", "click", "call", "eye_off", "page", "filter", "search", "ad", "mobile", "grid", "calendar",
         "clock", "pin", "users", "trophy", "trend_up", "trend_down", "target", "alert", "question", "check",
         "bulb", "flask", "chart", "store", "globe", "link", "star", "bolt", "tag", "pause", "scale"]
TONES = ["good", "bad", "neutral"]
EVIDENCE = ["verified", "observed", "estimate", "assumption", "hypothesis", "unknown"]

STAGE_FOCUS = {
    2: ("Business", "Read it like a company profile: what the business sells, how it earns (the business model), "
        "what a conversion is and what it is worth, season and capacity. Use a 'profile' block for these facts. "
        "Unanswered questions for the owner go in one 'list' block with the question icon; risks in another."),
    3: ("Market", "Read it like a market map: where demand is ('places'), who competes ('competitors'), how "
        "people search ('searches' with the search clusters or terms), and when demand peaks ('timeline')."),
    4: ("Website & ads", "Read it like the account and its pages: what searchers see ('ad', with the real "
        "headline), the landing page ('page', with its score and problems), what people searched ('searches'), "
        "how the account is built ('bars' or 'list'), and recent changes ('timeline')."),
    5: ("Growth", "Read it like a growth plan: the biggest opportunities ranked ('bars' by size when sizes are "
        "known, else 'list'), the order of moves ('timeline' with Now / Next / Later style steps), and risks."),
    6: ("Learning", "Read it like a scoreboard: forecasts and when they are checked ('timeline' with due dates), "
        "decisions taken ('list'), experiments running ('list' with the flask icon), lessons learned."),
}

VIEW_SPEC = """Return one JSON object and nothing else:
{
  "verdict": "the one sentence that matters most in this stage, max 110 characters",
  "kpis": [ up to 5 of {"icon": ICON, "value": "CA$1.25M" (max 9 characters: CA$1.25M, not CA$1,246,860), "unit": "clicks" (optional), "label": "max 4 words",
            "tone": TONE, "evidence": EVIDENCE, "item_id": "id it comes from"} ],
  "blocks": [ up to 6 blocks; every block has "type", "title" (max 4 words), "icon": ICON, optional "note"
              (one plain sentence, may wrap the key words in **bold**), optional "item_ids": [ids] ]
}
Block types and their extra fields:
- "ad":          "url", "headline", optional "highlight" (the words in the headline that are the problem),
                 optional "description", "flags": [{"text": max 6 words, "tone": TONE}]
- "page":        "url", "heading" (the page's H1), optional "score": {"value": 0-100, "label": "Mobile-friendly",
                 "compare": "Toronto pages: 87-92%"}, optional "cta_after_words": number, "flags": [...]
- "searches":    optional "share": [{"label": "Hidden by Google", "pct": 34.5, "tone": TONE}],
                 "rows": [{"query": "garage door opener remote", "bold": "remote", "value": "CA$50.8k"}]
- "timeline":    "steps": 2 to 5 of [{"date": "Oct 2" or "Next", "symbol": "1-3 characters like ½ ↑ ×2 ⏸", "label": max 3 words,
                 "tone": TONE}]
- "bars":        "rows": [{"label": max 5 words, "value": number, "display": "64%", "tone": TONE}]
- "profile":     "rows": [{"icon": ICON, "label": "Business model", "value": "Sells the calls", "evidence": EVIDENCE}]
- "list":        "rows": [{"text": max 14 words, "tone": TONE, "evidence": EVIDENCE, "item_id": id}]
- "places":      "rows": [{"place": "Edmonton", "value": "CA$64k", "note": max 6 words}]
- "competitors": "rows": [{"name": "Lock Surgeon", "note": max 8 words}]
ICON is one of: """ + ", ".join(ICONS) + """
TONE is one of: good, bad, neutral. EVIDENCE is one of: """ + ", ".join(EVIDENCE) + "."

RULES = """Rules:
- Show only what the owner needs to know to act. Leave out background, method and anything repeated.
- Use only numbers, names, URLs and headlines that appear in the input. Never invent or round a number into
  a new claim. If a block's fields are not in the input, choose another block type or leave it out.
- Prefer a picture to a sentence: a real ad headline as an "ad" block, a real page as a "page" block, real
  search terms as "searches", dated changes as a "timeline". Plain words, no jargon, no acronyms the owner
  would not use.
- Keep each fact's evidence label from its item. A KPI or row from an estimate says "estimate".
- Pick icons by meaning so the owner knows what a number is before reading: clicks -> click, money -> money,
  calls -> call, a page -> page, searches -> search, an ad -> ad, a date -> calendar, a risk -> alert,
  a question -> question, a place -> pin.
- If the stage holds nothing worth showing, return {"verdict": "", "kpis": [], "blocks": []}."""


def _item_line(it: dict) -> dict:
    return {"id": it["id"], "kind": it["kind"], "label": it.get("label"), "status": it.get("status"),
            "title": it["title"], "body": (it.get("body") or "")[:1800], "data": it.get("data") or {}}


async def gather(project_id: str, stage: int) -> dict:
    project = await store.get_project(project_id)
    if project is None:
        raise LookupError("project")
    items = [i for i in await store.list_items(project_id, stage) if i.get("status") not in CLOSED]
    facts = (project.get("facts") or []) if stage == 2 else []
    return {"project": project, "items": items, "facts": facts}


def fingerprint(stage: int, ctx: dict) -> str:
    p = ctx["project"]
    parts = [VERSION, str(stage), p.get("name") or "", p.get("objective") or "", p.get("country") or "",
             p.get("region") or "", p.get("website_url") or ""]
    parts += sorted(f"{i['id']}|{i.get('updated_at')}|{i.get('status')}" for i in ctx["items"])
    parts += sorted(f"{f['key']}|{f['value']}|{f['label']}" for f in ctx["facts"])
    return hashlib.sha1("\n".join(parts).encode()).hexdigest()


def build_prompt(stage: int, ctx: dict) -> str:
    name, focus = STAGE_FOCUS[stage]
    p = ctx["project"]
    about = {k: p.get(k) for k in ("name", "entry_path", "objective", "objective_type", "country", "region",
                                   "language", "website_url")}
    data = {"project": about, "items": [_item_line(i) for i in ctx["items"]]}
    if ctx["facts"]:
        data["business_facts"] = [{k: f[k] for k in ("key", "value", "label")} for f in ctx["facts"]]
    return (f"You design the '{name}' page of AllFix, a Google Ads strategist, for a busy business owner. "
            f"{focus}\n\n{VIEW_SPEC}\n\n{RULES}\n\n<stage_data>\n"
            f"{json.dumps(data, ensure_ascii=False, default=str)}\n</stage_data>")


# ---------- cleaning the model's answer ----------

def _s(v: Any, n: int) -> str:
    return re.sub(r"\s+", " ", str(v or "")).strip()[:n]


def _pick(v: Any, allowed: list[str], default: str) -> str:
    return v if v in allowed else default


def _num(v: Any) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _rows(v: Any, n: int) -> list[dict]:
    return [r for r in (v if isinstance(v, list) else []) if isinstance(r, dict)][:n]


def _flags(v: Any) -> list[dict]:
    return [{"text": _s(f.get("text"), 60), "tone": _pick(f.get("tone"), TONES, "neutral")}
            for f in _rows(v, 4) if f.get("text")]


def _block(b: dict, ids: set[str]) -> dict | None:
    t = b.get("type")
    out: dict[str, Any] = {"type": t, "title": _s(b.get("title"), 40), "icon": _pick(b.get("icon"), ICONS, "chart"),
                           "note": _s(b.get("note"), 240),
                           "item_ids": [i for i in (b.get("item_ids") or []) if i in ids][:8]}
    if t == "ad":
        if not b.get("headline"):
            return None
        out.update(url=_s(b.get("url"), 80), headline=_s(b.get("headline"), 90),
                   highlight=_s(b.get("highlight"), 40), description=_s(b.get("description"), 160),
                   flags=_flags(b.get("flags")))
    elif t == "page":
        if not (b.get("url") or b.get("heading")):
            return None
        sc = b.get("score") if isinstance(b.get("score"), dict) else None
        score = None
        if sc and _num(sc.get("value")) is not None:
            score = {"value": max(0.0, min(100.0, _num(sc["value"]))), "label": _s(sc.get("label"), 30),
                     "compare": _s(sc.get("compare"), 40)}
        out.update(url=_s(b.get("url"), 80), heading=_s(b.get("heading"), 80), score=score,
                   cta_after_words=int(_num(b.get("cta_after_words")) or 0) or None, flags=_flags(b.get("flags")))
    elif t == "searches":
        share = [{"label": _s(r.get("label"), 30), "pct": max(0.0, min(100.0, _num(r.get("pct")) or 0)),
                  "tone": _pick(r.get("tone"), TONES, "neutral")} for r in _rows(b.get("share"), 4)
                 if _num(r.get("pct")) is not None]
        rows = [{"query": _s(r.get("query"), 70), "bold": _s(r.get("bold"), 30), "value": _s(r.get("value"), 16)}
                for r in _rows(b.get("rows"), 5) if r.get("query")]
        if not rows and not share:
            return None
        out.update(share=share, rows=rows)
    elif t == "timeline":
        steps = [{"date": _s(r.get("date"), 14), "symbol": _s(r.get("symbol"), 3), "label": _s(r.get("label"), 32),
                  "tone": _pick(r.get("tone"), TONES, "neutral")} for r in _rows(b.get("steps"), 5) if r.get("label")]
        if len(steps) < 2:
            return None
        out.update(steps=steps)
    elif t == "bars":
        rows = [{"label": _s(r.get("label"), 40), "value": _num(r.get("value")), "display": _s(r.get("display"), 14),
                 "tone": _pick(r.get("tone"), TONES, "neutral")} for r in _rows(b.get("rows"), 6)
                if r.get("label") and _num(r.get("value")) is not None]
        if not rows:
            return None
        out.update(rows=rows)
    elif t == "profile":
        rows = [{"icon": _pick(r.get("icon"), ICONS, "check"), "label": _s(r.get("label"), 30),
                 "value": _s(r.get("value"), 120), "evidence": _pick(r.get("evidence"), EVIDENCE, "unknown")}
                for r in _rows(b.get("rows"), 8) if r.get("label") and r.get("value")]
        if not rows:
            return None
        out.update(rows=rows)
    elif t == "list":
        rows = [{"text": _s(r.get("text"), 140), "tone": _pick(r.get("tone"), TONES, "neutral"),
                 "evidence": _pick(r.get("evidence"), EVIDENCE, "unknown"),
                 "item_id": r.get("item_id") if r.get("item_id") in ids else None}
                for r in _rows(b.get("rows"), 7) if r.get("text")]
        if not rows:
            return None
        out.update(rows=rows)
    elif t == "places":
        rows = [{"place": _s(r.get("place"), 30), "value": _s(r.get("value"), 16), "note": _s(r.get("note"), 50)}
                for r in _rows(b.get("rows"), 8) if r.get("place")]
        if not rows:
            return None
        out.update(rows=rows)
    elif t == "competitors":
        rows = [{"name": _s(r.get("name"), 40), "note": _s(r.get("note"), 70)} for r in _rows(b.get("rows"), 6)
                if r.get("name")]
        if not rows:
            return None
        out.update(rows=rows)
    else:
        return None
    return out


def clean(raw: Any, ids: set[str]) -> dict:
    raw = raw if isinstance(raw, dict) else {}
    kpis = [{"icon": _pick(k.get("icon"), ICONS, "chart"), "value": _s(k.get("value"), 14), "unit": _s(k.get("unit"), 12),
             "label": _s(k.get("label"), 32), "tone": _pick(k.get("tone"), TONES, "neutral"),
             "evidence": _pick(k.get("evidence"), EVIDENCE, "unknown"),
             "item_id": k.get("item_id") if k.get("item_id") in ids else None}
            for k in _rows(raw.get("kpis"), 5) if k.get("value") and k.get("label")]
    blocks = [b for b in (_block(x, ids) for x in _rows(raw.get("blocks"), 6)) if b]
    return {"verdict": _s(raw.get("verdict"), 160), "kpis": kpis, "blocks": blocks}


def parse(text: str) -> Any:
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("the model did not return a view")
    return json.loads(text[start:end + 1])


# ---------- writing a view with the model ----------

Writer = Callable[[str], Awaitable[tuple[str, str]]]  # prompt -> (text, model)


async def write_with_subscription(prompt: str) -> tuple[str, str]:
    """One question to Claude on the owner's plan, no tools. Runs on its own thread (see subscription.py)."""
    from ..strategist.subscription import AGENT_ENV, guard_error
    problem = guard_error()
    if problem:
        raise RuntimeError(problem)
    s = get_settings()
    out: dict[str, Any] = {}

    async def ask() -> None:
        from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ResultMessage, TextBlock, query
        s.agent_workdir.mkdir(parents=True, exist_ok=True)
        opts = ClaudeAgentOptions(system_prompt="You turn saved findings into a compact visual page. Answer with JSON only.",
                                  model=s.model_standard, effort="low", tools=[], allowed_tools=[],
                                  setting_sources=[], skills=[], permission_mode="dontAsk", max_turns=1,
                                  cwd=str(s.agent_workdir), env=dict(AGENT_ENV), cli_path=s.claude_cli_path)
        text = []
        async for msg in query(prompt=prompt, options=opts):
            if isinstance(msg, AssistantMessage):
                out["model"] = msg.model
                text += [b.text for b in msg.content if isinstance(b, TextBlock)]
            elif isinstance(msg, ResultMessage) and msg.is_error:
                out["error"] = str(getattr(msg, "result", "") or "the model returned an error")[:300]
        out["text"] = "".join(text)

    def run() -> None:
        factory = asyncio.ProactorEventLoop if sys.platform == "win32" else asyncio.SelectorEventLoop
        try:
            asyncio.run(ask(), loop_factory=factory)
        except Exception as e:  # reported below
            out["error"] = f"{type(e).__name__}: {str(e)[:300]}"

    thread = threading.Thread(target=run, name="allfix-stage-view", daemon=True)
    thread.start()
    await asyncio.to_thread(thread.join, TIMEOUT + 10)
    if out.get("error") and not out.get("text"):
        raise RuntimeError(out["error"])
    return out.get("text", ""), out.get("model") or s.model_standard


async def write_with_api(prompt: str) -> tuple[str, str]:
    import anthropic
    s = get_settings()
    client = anthropic.AsyncAnthropic(api_key=s.anthropic_api_key) if s.anthropic_api_key else anthropic.AsyncAnthropic()
    msg = await client.messages.create(model=s.model_standard, max_tokens=8000,
                                       messages=[{"role": "user", "content": prompt}])
    return "".join(b.text for b in msg.content if getattr(b, "type", None) == "text"), msg.model


def default_writer() -> Writer:
    return write_with_api if get_settings().strategist_backend == "api" else write_with_subscription


# ---------- storage and background work ----------

TIMEOUT = 150  # seconds one page may take before it is given up and the saved items are shown
_running: dict[tuple[str, int], asyncio.Task] = {}
_started: dict[tuple[str, int], float] = {}
_errors: dict[tuple[str, int], str] = {}
_slots: dict[int, asyncio.Semaphore] = {}  # per event loop: at most two pages are written at once


async def load(project_id: str, stage: int) -> dict | None:
    row = await db.fetch_one("select fingerprint, view, model, created_at from stage_views "
                             "where project_id = %s and stage = %s", (project_id, stage))
    if row and isinstance(row.get("view"), str):
        row["view"] = json.loads(row["view"])
    return row


async def generate(project_id: str, stage: int, writer: Writer) -> dict:
    ctx = await gather(project_id, stage)
    fp = fingerprint(stage, ctx)
    if not ctx["items"] and not ctx["facts"]:
        view = {"verdict": "", "kpis": [], "blocks": []}
        model = None
    else:
        try:
            text, model = await asyncio.wait_for(writer(build_prompt(stage, ctx)), TIMEOUT)
        except asyncio.TimeoutError:
            raise RuntimeError(f"Writing this page took longer than {TIMEOUT // 60} minutes") from None
        view = clean(parse(text), {i["id"] for i in ctx["items"]})
    await db.execute(
        """insert into stage_views (project_id, stage, fingerprint, view, model) values (%s, %s, %s, %s, %s)
           on conflict (project_id, stage) do update
             set fingerprint = excluded.fingerprint, view = excluded.view, model = excluded.model, created_at = now()""",
        (project_id, stage, fp, json.dumps(view, ensure_ascii=False), model))
    return view


async def status(project_id: str, stage: int) -> dict:
    """The stored view (possibly from older items), whether it is current, and whether a new one is being written."""
    ctx = await gather(project_id, stage)
    row = await load(project_id, stage)
    key = (project_id, stage)
    task = _running.get(key)
    empty = not ctx["items"] and not ctx["facts"]
    return {"view": row["view"] if row else None,
            "fresh": empty or bool(row and row["fingerprint"] == fingerprint(stage, ctx)),
            "empty": empty,
            "generating": bool(task and not task.done()),
            "elapsed": round(time.monotonic() - _started[key]) if task and not task.done() and key in _started else 0,
            "error": _errors.get(key)}


def start(project_id: str, stage: int, writer: Writer) -> None:
    key = (project_id, stage)
    task = _running.get(key)
    if task and not task.done():
        return
    _errors.pop(key, None)

    async def work() -> None:
        slots = _slots.setdefault(id(asyncio.get_running_loop()), asyncio.Semaphore(2))
        try:
            async with slots:
                _started[key] = time.monotonic()
                await generate(project_id, stage, writer)
        except Exception as e:
            log.warning("stage view %s/%s failed: %s", project_id, stage, e)
            _errors[key] = str(e)[:300]

    _running[key] = asyncio.create_task(work())


async def refresh_all(project_id: str, writer: Writer) -> list[int]:
    """Start a new page for every stage whose findings changed, so pages are ready before they are opened."""
    started = []
    for n in sorted(VIEW_STAGES):
        st = await status(project_id, n)
        if not st["fresh"] and not st["generating"]:
            start(project_id, n, writer)
            started.append(n)
    return started
