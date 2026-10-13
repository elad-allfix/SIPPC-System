"""Tools the strategist can call, and their handlers.

Server tools (web search and fetch) run on Anthropic's side; everything else
runs here against the project database and the knowledge base.
"""

from __future__ import annotations

import logging
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
                            "key": {"type": "string", "description": "e.g. average_order_value, gross_margin, close_rate, capacity_per_week"},
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
                       "question. Stages: 2 business understanding, 3 market research, 4 campaign/website "
                       "intelligence, 5 strategy, 6 learning (decisions, forecasts, experiments). Use data for "
                       "structure: intent_cluster {situation, example_queries, searcher_wants, value, competition}; "
                       "competitor {domain, angles, offers, proof, landing_pages}; decision {decision, reasoning, "
                       "alternatives}; forecast {prediction, metric, expected_range, review_after (YYYY-MM-DD), would_change_if}; "
                       "experiment {hypothesis, design, success_metric, minimum_volume}.",
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
                       "a CPC (range) to compare against.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversion_rate": {**_RANGE, "description": "Share of clicks that take the tracked action."},
                "close_rate": {**_RANGE, "description": "Share of actions that become customers (omit or 1 if the action is the sale)."},
                "value_per_customer": {**_RANGE, "description": "Revenue or lifetime value per customer."},
                "contribution_margin": {**_RANGE, "description": "Share of that value left after variable costs."},
                "acquisition_share": {**_RANGE, "description": "Share of contribution the business will spend to acquire a customer (1 = break-even)."},
                "cpc": {**_RANGE, "description": "Observed or estimated CPC to compare."},
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
    return await kb.read(list(args["ids"]))


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


async def _save_item(ctx: ToolContext, args: dict) -> Any:
    item = await store.create_item(ctx.project_id, args, ctx.conversation_id)
    ctx.saved_items.append(item)
    return {"saved": True, "id": item["id"], "stage": item["stage"], "kind": item["kind"]}


async def _update_item(ctx: ToolContext, args: dict) -> Any:
    existing = await store.get_item(args["id"])
    if existing is None or existing["project_id"] != ctx.project_id:
        raise ToolError("no item with that id in this project")
    item = await store.update_item(args["id"], args)
    ctx.saved_items.append(item)
    return {"updated": True, "id": item["id"], "status": item["status"]}


async def _calculate_economics(ctx: ToolContext, args: dict) -> Any:
    inputs = {k: v for k, v in args.items() if k in economics.INPUTS}
    try:
        return economics.calculate(inputs, args.get("cpc"))
    except ValueError as e:
        raise ToolError(str(e)) from e


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


async def run_tool(ctx: ToolContext, name: str, args: Any) -> tuple[str, bool]:
    """Run one client tool. Returns (result text, is_error)."""
    handler = HANDLERS.get(name)
    if handler is None:
        return f"unknown tool: {name}", True
    try:
        result = await handler(ctx, _validate(name, args))
        return store.to_json(result), False
    except (ToolError, ValueError, KeyError) as e:
        return f"error: {e}", True
    except Exception as e:  # keep the conversation valid; the error is logged by the caller
        log.exception("tool %s failed", name)
        return f"internal error in {name}: {type(e).__name__}", True
