"""Tools the strategist can call, and their handlers.

Server tools (web search and fetch) run on Anthropic's side; everything else
runs here against the project database and the knowledge base.
"""

from __future__ import annotations

from datetime import date

import logging
import re
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable

from .. import store
from ..intelligence import economics, website
from ..knowledge import search as kb
from .models import ModelSpec

log = logging.getLogger(__name__)

LABEL_ENUM = list(store.LABELS)

_SOURCES = {
    "type": "array",
    "description": "Where this came from: URLs you opened, knowledge entry ids, or 'user' for things the user said.",
    "items": {
        "type": "object",
        "properties": {
            "url": {"type": "string"},
            "title": {"type": "string"},
            "kb": {"type": "string", "description": "knowledge entry id, e.g. PLT-AUC-009"},
            "note": {"type": "string"},
        },
    },
}

_RANGE = {
    "description": "A number, or [low, high] for a range.",
    "anyOf": [{"type": "number"}, {"type": "array", "items": {"type": "number"}, "minItems": 2, "maxItems": 2}],
}

CLIENT_TOOLS: list[dict] = [
    {
        "name": "search_knowledge",
        "description": "Search the AllFix expert knowledge base (Google Ads mechanics, bidding, matching, "
                       "Quality Score, automation, measurement, economics, market research, copy, expert "
                       "diagnosis, playbooks). Returns entry ids, titles, claims, evidence type and confidence. "
                       "Search before stating how Google Ads behaves.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Words describing what you need, or entry ids."},
                "area": {"type": "string", "enum": ["platform", "practice", "measurement", "market"]},
                "limit": {"type": "integer", "minimum": 1, "maximum": 20},
            },
            "required": ["query"],
        },
    },
    {
        "name": "read_knowledge",
        "description": "Read the full text of knowledge entries (by id, e.g. PLT-BID-007) or documents "
                       "(by slug: playbooks/diagnostic, playbooks/strategic, relationships/metric-relationships, "
                       "demo/us-car-insurance-market-research, READINESS, research-gaps).",
        "input_schema": {
            "type": "object",
            "properties": {"ids": {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": 12}},
            "required": ["ids"],
        },
    },
    {
        "name": "get_project",
        "description": "Get the project profile, business facts and saved items. Filter items by stage (1-7) or kind.",
        "input_schema": {
            "type": "object",
            "properties": {
                "stage": {"type": "integer", "minimum": 1, "maximum": 7},
                "kind": {"type": "string", "enum": list(store.KINDS)},
                "include_superseded": {"type": "boolean"},
            },
        },
    },
    {
        "name": "update_project",
        "description": "Update the project profile and/or record business facts. Every fact needs a label and a "
                       "source (e.g. 'user said', a URL, or 'assumption for planning').",
        "input_schema": {
            "type": "object",
            "properties": {
                "profile": {
                    "type": "object",
                    "properties": {
                        "objective": {"type": "string"},
                        "objective_type": {"type": "string", "enum": list(store.OBJECTIVE_TYPES)},
                        "country": {"type": "string"},
                        "region": {"type": "string"},
                        "language": {"type": "string"},
                        "website_url": {"type": "string"},
                        "notes": {"type": "string"},
                    },
                },
                "facts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "key": {"type": "string", "description": "Use these keys where they fit: business_model, conversion_definition, "
                                                                    "value_per_customer, contribution_margin, close_rate, conversion_rate, "
                                                                    "capacity_per_week; add ' (segment)' for one part of the business, e.g. "
                                                                    "'value_per_customer (garage doors)'. To correct a fact, reuse its exact key."},
                            "value": {"type": "string"},
                            "label": {"type": "string", "enum": LABEL_ENUM},
                            "source": {"type": "string"},
                        },
                        "required": ["key", "value", "label"],
                    },
                },
            },
        },
    },
    {
        "name": "save_item",
        "description": "Save something worth keeping to the project's memory. Kinds: finding, intent_cluster, "
                       "competitor, economics, website_issue, opportunity, risk, decision, forecast, experiment, "
                       "question. Stages: 2 business understanding (also tracking and measurement), 3 market research, "
                       "4 campaign/website intelligence, 5 strategy and actions, 6 learning (decisions, forecasts, "
                       "experiments); stages 1 and 7 hold no items. Use data for "
                       "structure: intent_cluster {situation, example_queries, searcher_wants, value, competition}; "
                       "competitor {domain, angles, offers, proof, landing_pages}; decision {decision, reasoning, "
                       "alternatives}; forecast {prediction, metric, expected_range, review_after (YYYY-MM-DD), would_change_if}; "
                       "experiment {hypothesis, design, success_metric, minimum_volume, review_after (YYYY-MM-DD)}; "
                       "a growth plan move is an opportunity with data.plan_part, one of keywords_add, keywords_cut, "
                       "bids_budgets, settings, ads, website.",
        "input_schema": {
            "type": "object",
            "properties": {
                "kind": {"type": "string", "enum": list(store.KINDS)},
                "stage": {"type": "integer", "minimum": 1, "maximum": 7},
                "title": {"type": "string", "description": "Short and specific."},
                "body": {"type": "string", "description": "Markdown: the content, reasoning and caveats."},
                "data": {"type": "object"},
                "label": {"type": "string", "enum": LABEL_ENUM},
                "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                "sources": _SOURCES,
            },
            "required": ["kind", "title", "body", "label", "confidence"],
        },
    },
    {
        "name": "update_item",
        "description": "Update a saved item: change status (confirmed, refuted, done, dropped), label or "
                       "confidence, append a note, merge data (e.g. a forecast's outcome), add sources, or "
                       "supersede it with a newer item id.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "status": {"type": "string", "enum": ["open", "confirmed", "refuted", "done", "dropped"]},
                "label": {"type": "string", "enum": LABEL_ENUM},
                "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                "append_note": {"type": "string"},
                "data": {"type": "object", "description": "Fields merged into the item's data, e.g. "
                         "{\"outcome\": {...}} when scoring a forecast."},
                "sources": _SOURCES,
                "superseded_by": {"type": "string"},
            },
            "required": ["id"],
        },
    },
    {
        "name": "calculate_economics",
        "description": "Advertising economics with ranges: value per click, maximum affordable CPC, break-even "
                       "ROAS, and which assumption is widest (pinning it down narrows the answer most). Shares are 0-1 (0.08 = 8%). Optionally pass "
                       "a CPC (range) to compare against. The inputs are saved to the project's business facts "
                       "(Stage 2) so the user can see and correct them; name the segment when a business has "
                       "several (service line, city), and give each input's label. If the result lists conflicts, "
                       "a saved fact the user gave differs from what you passed: rerun with the saved value.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversion_rate": {**_RANGE, "description": "Share of clicks that take the tracked action."},
                "close_rate": {**_RANGE, "description": "Share of actions that become customers (omit or 1 if the action is the sale)."},
                "value_per_customer": {**_RANGE, "description": "Revenue or lifetime value per customer."},
                "contribution_margin": {**_RANGE, "description": "Share of that value left after variable costs."},
                "acquisition_share": {**_RANGE, "description": "Share of contribution the business will spend to acquire a customer (1 = break-even)."},
                "cpc": {**_RANGE, "description": "Observed or estimated CPC to compare."},
                "cpc_scenarios": {"type": "array", "items": {"type": "number"},
                                  "description": "Several possible CPCs (up to 8) to price a test before real "
                                                 "CPCs are known: spend, expected customers and cost per customer "
                                                 "at each."},
                "clicks": {"type": "number", "description": "Clicks in the planned test (default 100)."},
                "segment": {"type": "string", "description": "Which part of the business these numbers describe, "
                                                             "e.g. 'garage door repair, Calgary'. Omit for the whole business."},
                "currency": {"type": "string", "description": "Currency of value_per_customer, e.g. CAD."},
                "labels": {"type": "object", "description": "Label per input name (verified, observed, estimate, "
                                                            "assumption); inputs not listed are saved as assumption.",
                           "additionalProperties": {"type": "string", "enum": LABEL_ENUM}},
            },
            "required": ["conversion_rate", "value_per_customer", "contribution_margin"],
        },
    },
    {
        "name": "audit_page",
        "description": "Audit one landing page or website page and return what is observably on it: title, "
                       "headings, opening text, calls to action, phone links, forms and their fields, prices, "
                       "trust-signal snippets, schema types, measurement tags (GTM, Google tag, Google Ads "
                       "conversion, call tracking, consent mode) with a visibility note, speed and size, and "
                       "notable internal links. Pass the search intent and, if known, the ad headline to check "
                       "message match. Facts come from raw HTML without JavaScript: read the 'limits' and "
                       "'measurement.visibility' fields before concluding anything is missing.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "intent": {"type": "string", "description": "The searcher's need, e.g. 'mobile dog grooming austin'."},
                "ad_headline": {"type": "string", "description": "Ad headline to check message match against."},
            },
            "required": ["url"],
        },
    },
    {
        "name": "account_snapshot",
        "description": "The latest imported Google Ads account snapshot for this project: totals, campaigns by "
                       "spend, search terms without conversions, conversion actions. Pass kind to get rows of one "
                       "table (campaigns, ad_groups, keywords, search_terms, conversion_actions, daily). Returns "
                       "a note if nothing has been imported yet.",
        "input_schema": {
            "type": "object",
            "properties": {
                "kind": {"type": "string", "enum": ["campaigns", "ad_groups", "keywords", "search_terms",
                                                    "conversion_actions", "daily", "customer"]},
                "limit": {"type": "integer", "minimum": 1, "maximum": 500},
            },
        },
    },
    {
        "name": "ads_query",
        "description": "Run one read-only GAQL SELECT against the project's Google Ads account, live. Only runs "
                       "when Stage 01 verifies the secure route; otherwise it is refused and says why. Prefer "
                       "account_snapshot for anything the import already has. Costs come back in micros.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}, "limit": {"type": "integer", "minimum": 1, "maximum": 500}},
            "required": ["query"],
        },
    },
    {
        "name": "read_file",
        "description": "Read a file the user uploaded to this project (listed in the project state). Tables "
                       "(Google Ads report exports, CRM or job lists as CSV/TSV) come back as columns, the "
                       "preamble lines above the header (the export's title and date range), totals of the "
                       "additive columns for the matching rows, the file's own Total rows, and a page of rows. "
                       "Known Google Ads reports also come with how_to_read (what to check first) and a warning "
                       "when rows do not add up to the file's own total. Filter with contains and where "
                       "(numbers), group with group_by (sums per value, e.g. cost per Campaign), order with "
                       "sort_by (e.g. 'Cost'), page with offset. Big exports are reduced on upload: the "
                       "preamble says which rows were left out. Screenshots come back as the image itself.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_id": {"type": "string"},
                "contains": {"type": "string", "description": "Keep rows where any cell contains this text (case-insensitive)."},
                "where": {"type": "array", "items": {"type": "string"},
                          "description": "Filters, all must hold: numbers ('Cost > 50', 'Conversions = 0') or exact "
                          "text with = or != ('Added/Excluded = None', 'Campaign type != Display')."},
                "group_by": {"type": "string", "description": "Column to group by; returns one row per value with "
                             "the row count and sums of additive columns, ordered by sort_by (default Cost)."},
                "sort_by": {"type": "string", "description": "Column name to order by (numbers sort numerically)."},
                "descending": {"type": "boolean", "description": "Default true."},
                "columns": {"type": "array", "items": {"type": "string"}, "description": "Only these columns in the rows."},
                "offset": {"type": "integer", "minimum": 0},
                "limit": {"type": "integer", "minimum": 1, "maximum": 200, "description": "Rows to return (default 50)."},
            },
            "required": ["file_id"],
        },
    },
    {
        "name": "keyword_gaps",
        "description": "Find searches that already bring clicks but are not keywords yet, from an uploaded search "
                       "terms report (and the keywords report, when there is one). Returns the gap search terms "
                       "with clicks, CTR, cost, average CPC and conversions, and the words and word pairs that "
                       "bring clicks but appear in no keyword (themes the account does not target). Use it for "
                       "keyword expansion and for a traffic plan; judge each gap by intent before adding it.",
        "input_schema": {
            "type": "object",
            "properties": {
                "search_terms_file_id": {"type": "string"},
                "keywords_file_id": {"type": "string", "description": "The keywords report, to compare against."},
                "contains": {"type": "string", "description": "Only search terms whose text or campaign contains this, e.g. a city or a service."},
                "min_clicks": {"type": "number", "description": "Minimum clicks for a gap term (default 3)."},
                "limit": {"type": "integer", "minimum": 1, "maximum": 200, "description": "Gap terms to return (default 40)."},
            },
            "required": ["search_terms_file_id"],
        },
    },
    {
        "name": "record_lesson",
        "description": "Record a correction or lesson so future reasoning sees it. Use when a conclusion, a "
                       "recommendation or a knowledge entry turned out to be wrong. shared=true makes it apply "
                       "to all projects.",
        "input_schema": {
            "type": "object",
            "properties": {
                "what_was_wrong": {"type": "string"},
                "correction": {"type": "string"},
                "applies_to": {"type": "string"},
                "kb_entry_ids": {"type": "array", "items": {"type": "string"}},
                "shared": {"type": "boolean"},
            },
            "required": ["what_was_wrong", "correction"],
        },
    },
]


def tool_list(spec: ModelSpec) -> list[dict]:
    """Deterministic tool list (stable order keeps the prompt cache valid)."""
    return [
        {"type": spec.web_search, "name": "web_search", "max_uses": 12},
        {"type": spec.web_fetch, "name": "web_fetch", "max_uses": 12},
        *CLIENT_TOOLS,
    ]


@dataclass
class ToolContext:
    project_id: str
    conversation_id: str
    saved_items: list[dict] = field(default_factory=list)


class ToolError(Exception):
    pass


async def _search_knowledge(ctx: ToolContext, args: dict) -> Any:
    return await kb.search(args["query"], int(args.get("limit") or 8), args.get("area"))


async def _read_knowledge(ctx: ToolContext, args: dict) -> Any:
    return await kb.read(list(args["ids"]), include_evals=False)


async def _get_project(ctx: ToolContext, args: dict) -> Any:
    p = await store.get_project(ctx.project_id)
    items = await store.list_items(ctx.project_id, args.get("stage"), args.get("kind"),
                                   bool(args.get("include_superseded")))
    return {"project": p, "items": items}


async def _update_project(ctx: ToolContext, args: dict) -> Any:
    out: dict[str, Any] = {}
    if args.get("profile"):
        out["profile"] = await store.update_project(ctx.project_id, args["profile"])
    facts = []
    for f in args.get("facts") or []:
        facts.append(await store.set_fact(ctx.project_id, f["key"], f["value"], f["label"], f.get("source", "")))
    if facts:
        out["facts"] = facts
    if not out:
        raise ToolError("nothing to update: pass profile and/or facts")
    return out


def _check_review_fields(args: dict) -> None:
    """Forecasts and experiments must say when they will be reviewed, or they never come due."""
    kind, data = args.get("kind"), args.get("data") or {}
    if kind not in ("forecast", "experiment"):
        return
    need = ["review_after"] + (["prediction", "metric"] if kind == "forecast" else ["hypothesis", "success_metric"])
    missing = [k for k in need if not data.get(k)]
    if missing:
        raise ToolError(f"a {kind} needs data.{', data.'.join(missing)}")
    try:
        date.fromisoformat(str(data["review_after"]))
    except ValueError as e:
        raise ToolError("data.review_after must be a date, YYYY-MM-DD") from e


_BUNDLED = re.compile(r"\?.+\?|,\s*(?:and|or)\s+(?:what|which|how|when|where|who|why|is|are|do|does|did|can|could|will|would|should|has|have)\b", re.I)


def _check_single_question(args: dict) -> None:
    """A question item holds one question, so the user can answer and close it on its own."""
    if args.get("kind") == "question" and _BUNDLED.search(str(args.get("title", ""))):
        raise ToolError("a question item holds one question: save each question as its own item")


def _check_plan_part(args: dict) -> None:
    part = (args.get("data") or {}).get("plan_part")
    if part is None:
        return
    if part not in store.PLAN_PARTS:
        raise ToolError(f"data.plan_part must be one of {list(store.PLAN_PARTS)}")
    if args.get("kind") != "opportunity":
        raise ToolError("only an opportunity item carries data.plan_part")


async def _save_item(ctx: ToolContext, args: dict) -> Any:
    _check_review_fields(args)
    _check_plan_part(args)
    _check_single_question(args)
    item = await store.create_item(ctx.project_id, args, ctx.conversation_id)
    ctx.saved_items.append(item)
    out = {"saved": True, "id": item["id"], "stage": item["stage"], "kind": item["kind"]}
    if item["kind"] == "experiment":
        out["reminder"] = "Save a forecast item for each measurable prediction this experiment makes."
    return out


async def _update_item(ctx: ToolContext, args: dict) -> Any:
    existing = await store.get_item(args["id"])
    if existing is None or existing["project_id"] != ctx.project_id:
        raise ToolError("no item with that id in this project")
    _check_plan_part({"kind": existing["kind"], "data": args.get("data")})
    item = await store.update_item(args["id"], args)
    ctx.saved_items.append(item)
    return {"updated": True, "id": item["id"], "status": item["status"]}


async def _calculate_economics(ctx: ToolContext, args: dict) -> Any:
    inputs = {k: v for k, v in args.items() if k in economics.INPUTS}
    try:
        result = economics.calculate(inputs, args.get("cpc"), args.get("cpc_scenarios"), args.get("clicks"))
    except ValueError as e:
        raise ToolError(str(e)) from e
    facts = await _economics_facts(ctx.project_id, inputs, args)
    result["saved_as_facts"] = facts["saved"]
    if facts["conflicts"]:
        result["conflicts"] = facts["conflicts"]
        result["note"] = "These inputs differ from facts the user gave. Rerun with the saved values before using this result."
    return result


# Labels a saved fact can carry that an economics assumption must not overwrite.
_FIRM = ("verified", "observed")


def _fmt_input(name: str, v: Any, currency: str) -> str:
    lo, hi = (v if isinstance(v, (list, tuple)) else (v, v))
    if name == "value_per_customer":
        f = lambda x: f"{x:,.0f}" if x >= 100 else f"{x:,.2f}"  # noqa: E731
        txt = f(lo) if lo == hi else f"{f(lo)}-{f(hi)}"
        return f"{txt} {currency}".strip()
    p = lambda x: f"{x * 100:.3g}%"  # noqa: E731
    return p(lo) if lo == hi else f"{p(lo)}-{p(hi)}"


async def _economics_facts(project_id: str, inputs: dict, args: dict) -> list[str]:
    """Persist the economics inputs as business facts, so assumptions are visible, reused and
    correctable. A fact the user gave (verified or observed) is never overwritten by an assumption."""
    seg = str(args.get("segment") or "").strip()
    labels = args.get("labels") or {}
    existing = {f["key"]: f for f in await store.list_facts(project_id)}
    saved, conflicts = [], []
    for name, v in inputs.items():
        key = f"{name} ({seg})" if seg else name
        label = labels.get(name) if labels.get(name) in store.LABELS else "assumption"
        try:
            value = _fmt_input(name, v, str(args.get("currency") or ""))
        except (TypeError, ValueError):
            continue
        # A firm fact for this segment, or for the whole business, wins over an assumption.
        firm = next((existing[k] for k in (key, name) if k in existing and existing[k]["label"] in _FIRM), None)
        if firm and label not in _FIRM:
            if firm["value"] != value:
                conflicts.append({"input": name, "fact": f"{firm['key']}: {firm['value']} [{firm['label']}]", "used": value})
            continue
        await store.set_fact(project_id, key, value, label, f"used in economics, {date.today().isoformat()}")
        saved.append(key)
    return {"saved": saved, "conflicts": conflicts}


async def _audit_page(ctx: ToolContext, args: dict) -> Any:
    return await website.audit_page(str(args["url"]), args.get("intent"), args.get("ad_headline"))


async def _account_snapshot(ctx: ToolContext, args: dict) -> Any:
    from ..ads import importer
    snap = await importer.latest_snapshot(ctx.project_id)
    if snap is None:
        return {"note": "No Google Ads account has been imported for this project. Account access needs Stage 01 "
                        "(secure connectivity) and an import, which the user starts from Stage 01."}
    if args.get("kind"):
        return {"snapshot": {k: snap[k] for k in ("id", "taken_at", "date_range", "status")},
                "rows": await importer.snapshot_rows(snap["id"], args["kind"], int(args.get("limit") or 100))}
    return snap


async def _ads_query(ctx: ToolContext, args: dict) -> Any:
    from ..ads.client import AdsApiError, AdsClient, AdsNotConfigured
    from ..ads.gaql import GaqlError, validate
    from ..connectivity import ConnectivityBlocked, profiles
    from ..connectivity.guard import Profile
    try:
        query = validate(str(args["query"]), default_limit=int(args.get("limit") or 200))
    except GaqlError as e:
        raise ToolError(f"query refused: {e}") from e
    row = await profiles.get(ctx.project_id)
    if row is None:
        raise ToolError("no connection profile for this project; the user sets it up in Stage 01")
    profile = Profile.from_row(row)
    try:
        async with AdsClient(profile) as client:
            rows = await client.search(query, validate=False, max_rows=int(args.get("limit") or 200))
    except ConnectivityBlocked as e:
        from ..connectivity import get_guard
        await profiles.record_last(get_guard(), profile)
        raise ToolError(f"blocked by Stage 01: {e}") from e
    except (AdsNotConfigured, AdsApiError) as e:
        raise ToolError(str(e)) from e
    return {"query": query, "rows": rows, "row_count": len(rows)}


@dataclass
class ToolImage:
    """A tool result the model should see as an image."""
    mime: str
    data: bytes
    note: dict


async def _read_file(ctx: ToolContext, args: dict) -> Any:
    from ..intelligence import uploads
    f = await store.get_file(str(args["file_id"]), ctx.project_id)
    if f is None:
        raise ToolError("no file with that id in this project; the project state lists the uploaded files")
    return uploads.read(f, args)


async def _keyword_gaps(ctx: ToolContext, args: dict) -> Any:
    from ..intelligence import gaps, uploads

    async def table(file_id: str):
        f = await store.get_file(str(file_id), ctx.project_id)
        if f is None:
            raise ToolError("no file with that id in this project; the project state lists the uploaded files")
        parsed = uploads._load(f)
        if isinstance(parsed, str):
            raise ToolError(f"{f['name']} is not a table")
        return parsed

    terms = await table(args["search_terms_file_id"])
    keywords = await table(args["keywords_file_id"]) if args.get("keywords_file_id") else None
    return gaps.keyword_gaps(terms, keywords, float(args.get("min_clicks") or 3), int(args.get("limit") or 40),
                             args.get("contains"))


async def _record_lesson(ctx: ToolContext, args: dict) -> Any:
    lesson = await store.create_lesson(None if args.get("shared") else ctx.project_id, args)
    return {"recorded": True, "id": lesson["id"]}


HANDLERS: dict[str, Callable[[ToolContext, dict], Awaitable[Any]]] = {
    "search_knowledge": _search_knowledge,
    "read_knowledge": _read_knowledge,
    "get_project": _get_project,
    "update_project": _update_project,
    "save_item": _save_item,
    "update_item": _update_item,
    "calculate_economics": _calculate_economics,
    "audit_page": _audit_page,
    "account_snapshot": _account_snapshot,
    "ads_query": _ads_query,
    "read_file": _read_file,
    "keyword_gaps": _keyword_gaps,
    "record_lesson": _record_lesson,
}


def _validate(name: str, args: Any) -> dict:
    if not isinstance(args, dict):
        raise ToolError("input must be an object")
    schema = next(t["input_schema"] for t in CLIENT_TOOLS if t["name"] == name)
    missing = [k for k in schema.get("required", []) if k not in args]
    if missing:
        raise ToolError(f"missing required fields: {missing}")
    return args


async def run_tool_blocks(ctx: ToolContext, name: str, args: Any) -> tuple[list[dict], bool]:
    """Run one client tool. Returns (MCP content blocks, is_error): text, plus an image when the
    tool returns one."""
    handler = HANDLERS.get(name)
    if handler is None:
        return [{"type": "text", "text": f"unknown tool: {name}"}], True
    try:
        result = await handler(ctx, _validate(name, args))
    except (ToolError, ValueError, KeyError) as e:
        return [{"type": "text", "text": f"error: {e}"}], True
    except Exception as e:  # keep the conversation valid; the error is logged by the caller
        log.exception("tool %s failed", name)
        return [{"type": "text", "text": f"internal error in {name}: {type(e).__name__}"}], True
    if isinstance(result, ToolImage):
        import base64
        return [{"type": "text", "text": store.to_json(result.note)},
                {"type": "image", "data": base64.b64encode(result.data).decode(), "mimeType": result.mime}], False
    return [{"type": "text", "text": store.to_json(result)}], False


async def run_tool(ctx: ToolContext, name: str, args: Any) -> tuple[str, bool]:
    """Run one client tool. Returns (result text, is_error); images are described, not shown."""
    blocks, is_error = await run_tool_blocks(ctx, name, args)
    return "\n".join(b["text"] if b["type"] == "text" else "[image]" for b in blocks), is_error
