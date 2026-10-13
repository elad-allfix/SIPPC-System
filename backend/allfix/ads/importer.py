"""Import a read-only snapshot of a Google Ads account into AllFix."""

from __future__ import annotations

import json
import logging
from datetime import date, timedelta
from typing import Any

from .. import db
from .client import AdsClient

log = logging.getLogger(__name__)

METRICS = ("metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions, "
           "metrics.conversions_value, metrics.all_conversions")


def queries(start: str, end: str) -> dict[str, str]:
    during = f"segments.date BETWEEN '{start}' AND '{end}'"
    return {
        "customer": "SELECT customer.id, customer.descriptive_name, customer.currency_code, customer.time_zone, "
                    "customer.auto_tagging_enabled, customer.manager FROM customer",
        "campaigns": "SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, "
                     "campaign.bidding_strategy_type, campaign_budget.amount_micros, "
                     f"metrics.search_impression_share, metrics.search_budget_lost_impression_share, "
                     f"metrics.search_rank_lost_impression_share, {METRICS} FROM campaign WHERE {during}",
        "ad_groups": f"SELECT campaign.name, ad_group.id, ad_group.name, ad_group.status, {METRICS} "
                     f"FROM ad_group WHERE {during} AND metrics.impressions > 0",
        "keywords": "SELECT campaign.name, ad_group.name, ad_group_criterion.keyword.text, "
                    "ad_group_criterion.keyword.match_type, ad_group_criterion.status, "
                    "ad_group_criterion.quality_info.quality_score, "
                    f"{METRICS} FROM keyword_view WHERE {during} ORDER BY metrics.cost_micros DESC LIMIT 2000",
        "search_terms": "SELECT search_term_view.search_term, search_term_view.status, campaign.name, ad_group.name, "
                        f"{METRICS} FROM search_term_view WHERE {during} ORDER BY metrics.cost_micros DESC LIMIT 2000",
        "conversion_actions": "SELECT conversion_action.name, conversion_action.category, conversion_action.status, "
                              "conversion_action.type, conversion_action.primary_for_goal, "
                              "conversion_action.counting_type FROM conversion_action",
        "daily": f"SELECT segments.date, {METRICS} FROM customer WHERE {during}",
    }


def _num(v: Any) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def summarise(data: dict[str, list[dict]]) -> dict:
    """Plain totals and the obvious places to look. No judgements: the strategist does that."""
    cust = (data.get("customer") or [{}])[0]
    camps = data.get("campaigns", [])
    cost = sum(_num(r.get("metrics.costMicros")) for r in camps) / 1e6
    clicks = sum(_num(r.get("metrics.clicks")) for r in camps)
    conv = sum(_num(r.get("metrics.conversions")) for r in camps)
    value = sum(_num(r.get("metrics.conversionsValue")) for r in camps)
    terms = data.get("search_terms", [])
    no_conv = [r for r in terms if _num(r.get("metrics.conversions")) == 0 and _num(r.get("metrics.costMicros")) > 0]
    no_conv_cost = sum(_num(r.get("metrics.costMicros")) for r in no_conv) / 1e6
    actions = data.get("conversion_actions", [])
    return {
        "account": cust.get("customer.descriptiveName"),
        "currency": cust.get("customer.currencyCode"),
        "auto_tagging": cust.get("customer.autoTaggingEnabled"),
        "cost": round(cost, 2), "clicks": int(clicks), "conversions": round(conv, 2),
        "conversion_value": round(value, 2),
        "cost_per_conversion": round(cost / conv, 2) if conv else None,
        "campaigns": len(camps),
        "campaigns_by_spend": [
            {"name": r.get("campaign.name"), "type": r.get("campaign.advertisingChannelType"),
             "bidding": r.get("campaign.biddingStrategyType"),
             "cost": round(_num(r.get("metrics.costMicros")) / 1e6, 2), "conversions": _num(r.get("metrics.conversions")),
             "impression_share": r.get("metrics.searchImpressionShare")}
            for r in sorted(camps, key=lambda r: -_num(r.get("metrics.costMicros")))[:10]],
        "search_terms_without_conversions": {
            "count": len(no_conv), "cost": round(no_conv_cost, 2),
            "share_of_term_cost": round(no_conv_cost / (sum(_num(r.get("metrics.costMicros")) for r in terms) / 1e6), 3)
            if terms and any(_num(r.get("metrics.costMicros")) for r in terms) else None,
            "top": [{"term": r.get("searchTermView.searchTerm"), "cost": round(_num(r.get("metrics.costMicros")) / 1e6, 2),
                     "clicks": int(_num(r.get("metrics.clicks")))} for r in no_conv[:20]],
            "note": "Zero conversions in the window is not proof of waste: check conversion lag, volume and tracking.",
        },
        "conversion_actions": [
            {"name": r.get("conversionAction.name"), "category": r.get("conversionAction.category"),
             "primary": r.get("conversionAction.primaryForGoal"), "status": r.get("conversionAction.status"),
             "counting": r.get("conversionAction.countingType")} for r in actions],
    }


async def run_import(project_id: str, client: AdsClient, days: int = 90, today: date | None = None) -> dict:
    end = (today or date.today()) - timedelta(days=1)
    start = end - timedelta(days=days - 1)
    snap = await db.fetch_one(
        "insert into ads_snapshots (project_id, customer_id, date_range) values (%s, %s, %s) returning id",
        (project_id, client.profile.ads_customer_id, f"{start}..{end}"))
    sid = str(snap["id"])
    data: dict[str, list[dict]] = {}
    try:
        for kind, q in queries(str(start), str(end)).items():
            data[kind] = await client.search(q, validate=False)
            await db.execute("insert into ads_snapshot_rows (snapshot_id, kind, rows) values (%s, %s, %s::jsonb)",
                             (sid, kind, json.dumps(data[kind])))
        summary = summarise(data)
        await db.execute("update ads_snapshots set status = 'done', summary = %s::jsonb where id = %s",
                         (json.dumps(summary), sid))
        return {"snapshot_id": sid, "status": "done", "date_range": f"{start}..{end}", "summary": summary}
    except Exception as e:
        await db.execute("update ads_snapshots set status = 'failed', error = %s where id = %s", (str(e)[:500], sid))
        raise


async def latest_snapshot(project_id: str) -> dict | None:
    row = await db.fetch_one(
        "select id, customer_id, taken_at, date_range, status, error, summary from ads_snapshots "
        "where project_id = %s order by taken_at desc limit 1", (project_id,))
    if row:
        row["id"] = str(row["id"])
        row["taken_at"] = row["taken_at"].isoformat()
    return row


async def snapshot_rows(snapshot_id: str, kind: str, limit: int = 100) -> list[dict]:
    row = await db.fetch_one("select rows from ads_snapshot_rows where snapshot_id = %s and kind = %s",
                             (snapshot_id, kind))
    return (row["rows"] if row else [])[:limit]
