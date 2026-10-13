"""Daily account check: deterministic comparisons, no model.

It reads a small set of read-only queries, compares them with the previous check and with a
trailing baseline, and lists what changed or looks broken. "Nothing changed" is the normal result.
Recent days are incomplete (conversion lag), so the baseline ends three days before the check.
"""

from __future__ import annotations

import json
import math
from datetime import date, timedelta
from typing import Any

from .. import db
from .client import AdsClient, AdsNotConfigured

KIND = "account_check"
RECENT_DAYS = 3          # the newest complete days, compared with the baseline
BASELINE_DAYS = 28       # the baseline window, ending before the recent days
TERM_DAYS = 7


def _n(v: Any) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def queries(today: date) -> dict[str, str]:
    y = today - timedelta(days=1)
    start = y - timedelta(days=RECENT_DAYS + BASELINE_DAYS - 1)
    t_start = y - timedelta(days=TERM_DAYS - 1)
    return {
        "customer": "SELECT customer.id, customer.descriptive_name, customer.currency_code, "
                    "customer.auto_tagging_enabled FROM customer",
        "settings": "SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type, "
                    "campaign_budget.amount_micros FROM campaign WHERE campaign.status != 'REMOVED'",
        "conversion_actions": "SELECT conversion_action.id, conversion_action.name, conversion_action.status, "
                              "conversion_action.primary_for_goal, conversion_action.counting_type, "
                              "conversion_action.category FROM conversion_action "
                              "WHERE conversion_action.status != 'REMOVED'",
        "daily": "SELECT campaign.id, campaign.name, segments.date, metrics.cost_micros, metrics.conversions, "
                 "metrics.impressions, metrics.search_impression_share FROM campaign "
                 f"WHERE segments.date BETWEEN '{start}' AND '{y}' AND campaign.status != 'REMOVED'",
        "terms": "SELECT search_term_view.search_term, search_term_view.status, metrics.cost_micros, "
                 "metrics.clicks, metrics.conversions FROM search_term_view "
                 f"WHERE segments.date BETWEEN '{t_start}' AND '{y}' ORDER BY metrics.cost_micros DESC LIMIT 300",
    }


def state_of(data: dict[str, list[dict]]) -> dict:
    """The parts of the account that the next check compares against."""
    cust = (data.get("customer") or [{}])[0]
    return {
        "auto_tagging": cust.get("customer.autoTaggingEnabled"),
        "currency": cust.get("customer.currencyCode"),
        "campaigns": {str(r.get("campaign.id")): {
            "name": r.get("campaign.name"), "status": r.get("campaign.status"),
            "bidding": r.get("campaign.biddingStrategyType"),
            "budget": round(_n(r.get("campaignBudget.amountMicros")) / 1e6, 2)} for r in data.get("settings", [])},
        "conversion_actions": {str(r.get("conversionAction.id")): {
            "name": r.get("conversionAction.name"), "status": r.get("conversionAction.status"),
            "primary": r.get("conversionAction.primaryForGoal"),
            "counting": r.get("conversionAction.countingType")} for r in data.get("conversion_actions", [])},
        "terms": sorted({r.get("searchTermView.searchTerm") for r in data.get("terms", []) if r.get("searchTermView.searchTerm")}),
    }


def _finding(check: str, severity: str, title: str, detail: str, label: str = "observed") -> dict:
    return {"check": check, "severity": severity, "title": title, "detail": detail, "label": label}


def _diff(kind: str, before: dict, after: dict, fields: tuple[str, ...], what: str, severity: str) -> list[dict]:
    out = []
    for key in sorted(set(before) | set(after)):
        b, a = before.get(key), after.get(key)
        name = (a or b or {}).get("name") or key
        if b is None:
            out.append(_finding(kind, severity, f"New {what}: {name}", json.dumps({f: a.get(f) for f in fields})))
        elif a is None:
            out.append(_finding(kind, severity, f"{what.capitalize()} gone: {name}", "no longer returned (removed)"))
        else:
            changed = [f"{f}: {b.get(f)} -> {a.get(f)}" for f in fields if b.get(f) != a.get(f)]
            if changed:
                out.append(_finding(kind, severity, f"{what.capitalize()} changed: {name}", "; ".join(changed)))
    return out


def evaluate(data: dict[str, list[dict]], previous_state: dict | None, today: date) -> dict:
    state = state_of(data)
    cur = state.get("currency") or ""
    findings: list[dict] = []

    # 1. Changes since the last check (verified: both sides come from the API).
    if previous_state:
        if previous_state.get("auto_tagging") != state["auto_tagging"]:
            findings.append(_finding("auto_tagging", "high", "Auto-tagging changed",
                                     f"{previous_state.get('auto_tagging')} -> {state['auto_tagging']}", "verified"))
        findings += [dict(f, label="verified") for f in _diff(
            "conversion_actions", previous_state.get("conversion_actions", {}), state["conversion_actions"],
            ("status", "primary", "counting"), "conversion action", "high")]
        findings += [dict(f, label="verified") for f in _diff(
            "campaigns", previous_state.get("campaigns", {}), state["campaigns"],
            ("status", "bidding", "budget"), "campaign", "medium")]
    elif state["auto_tagging"] is False:
        findings.append(_finding("auto_tagging", "medium", "Auto-tagging is off",
                                 "GCLIDs are not added to ad clicks, which weakens conversion measurement.", "verified"))
    if not any(a.get("status") == "ENABLED" and a.get("primary") for a in state["conversion_actions"].values()):
        findings.append(_finding("conversion_actions", "high", "No enabled primary conversion action",
                                 "Bidding and reporting have no primary goal to count.", "verified"))

    # 2. Recent days against the baseline (account level).
    y = today - timedelta(days=1)
    recent_from = y - timedelta(days=RECENT_DAYS - 1)
    base_to = recent_from - timedelta(days=1)
    days: dict[str, dict] = {}
    camp_days: dict[str, dict[str, dict]] = {}
    for r in data.get("daily", []):
        d = r.get("segments.date")
        if not d:
            continue
        day = days.setdefault(d, {"cost": 0.0, "conv": 0.0})
        day["cost"] += _n(r.get("metrics.costMicros")) / 1e6
        day["conv"] += _n(r.get("metrics.conversions"))
        cd = camp_days.setdefault(str(r.get("campaign.id")), {})
        cd[d] = {"name": r.get("campaign.name"), "cost": _n(r.get("metrics.costMicros")) / 1e6,
                 "is": r.get("metrics.searchImpressionShare")}
    recent = [v for d, v in days.items() if d >= str(recent_from)]
    base = [v for d, v in days.items() if d <= str(base_to)]
    metrics: dict[str, Any] = {"recent_days": f"{recent_from}..{y}"}
    base_start = base_to - timedelta(days=BASELINE_DAYS - 1)
    first = min((date.fromisoformat(d) for d in days), default=None)
    # Days missing inside the window had no traffic; days before the account's first traffic don't count.
    base_len = (base_to - max(first, base_start)).days + 1 if first and first <= base_to else 0
    if base_len >= 14:
        base_cost = sum(v["cost"] for v in base) / base_len
        base_conv = sum(v["conv"] for v in base) / base_len
        rec_cost = sum(v["cost"] for v in recent) / RECENT_DAYS
        rec_conv = sum(v["conv"] for v in recent)
        metrics.update(baseline_days=base_len, baseline_cost_per_day=round(base_cost, 2), recent_cost_per_day=round(rec_cost, 2),
                       baseline_conv_per_day=round(base_conv, 2), recent_conversions=round(rec_conv, 2))
        if base_cost > 0 and abs(rec_cost - base_cost) / base_cost > 0.3:
            findings.append(_finding("spend", "medium",
                                     f"Spend {'up' if rec_cost > base_cost else 'down'} {abs(rec_cost / base_cost - 1):.0%}",
                                     f"{rec_cost:.2f} {cur}/day over the last {RECENT_DAYS} days vs {base_cost:.2f} baseline"))
        expected = base_conv * RECENT_DAYS
        # Zero conversions where the baseline expects at least 4 has under a 2% chance (Poisson) if
        # nothing changed. Conversion lag can still explain part of it, so it is flagged, not concluded.
        if rec_conv == 0 and expected >= 4:
            findings.append(_finding("conversions", "high", "No conversions in the last 3 days",
                                     f"baseline expects about {expected:.1f} (chance of zero by luck ≈ "
                                     f"{math.exp(-expected):.1%}). Check tracking first; conversion lag can delay "
                                     "reporting by a few days."))
    else:
        metrics["note"] = "under 14 baseline days of history; spend and conversion checks skipped"

    # 3. Impression share drops per campaign (last 7 days vs baseline), only where it matters.
    for cid, per_day in camp_days.items():
        name = next(iter(per_day.values()))["name"]
        def avg_is(rows):
            vals = [_n(v["is"]) for v in rows if v.get("is") not in (None, "")]
            return sum(vals) / len(vals) if len(vals) >= 3 else None
        last7 = [v for d, v in per_day.items() if d > str(y - timedelta(days=7))]
        older = [v for d, v in per_day.items() if d <= str(base_to)]
        a, b = avg_is(last7), avg_is(older)
        spend = sum(v["cost"] for v in last7)
        if a is not None and b is not None and b - a > 0.10 and spend > 0:
            findings.append(_finding("impression_share", "medium", f"Impression share down in {name}",
                                     f"{a:.0%} over the last 7 days vs {b:.0%} before"))

    # 4. New costly search terms without conversions (vs the terms seen at the last check).
    if previous_state:
        seen = set(previous_state.get("terms", []))
        new = [r for r in data.get("terms", []) if r.get("searchTermView.searchTerm") not in seen
               and _n(r.get("metrics.conversions")) == 0 and _n(r.get("metrics.costMicros")) > 0
               and r.get("searchTermView.status") not in ("EXCLUDED", "ADDED_EXCLUDED")][:5]
        if new:
            findings.append(_finding("search_terms", "low", f"{len(new)} new costly search terms without conversions",
                                     "; ".join(f"{r['searchTermView.searchTerm']} ({_n(r.get('metrics.costMicros')) / 1e6:.2f} {cur})"
                                               for r in new) + ". Not proof of waste: check volume and lag first."))

    order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: order[f["severity"]])
    return {"state": state, "metrics": metrics, "findings": findings,
            "attention": any(f["severity"] in ("high", "medium") for f in findings),
            "first_check": previous_state is None}


async def previous_state(project_id: str, today: date) -> dict | None:
    row = await db.fetch_one(
        "select data from runs where project_id = %s and kind = %s and status = 'done' and run_date < %s "
        "order by run_date desc limit 1", (project_id, KIND, today))
    return (row["data"] or {}).get("state") if row else None


async def run(project_id: str, client: AdsClient, today: date | None = None, force: bool = False) -> dict:
    """Run today's check for one project (once per day unless forced)."""
    today = today or date.today()
    if not client.profile.ads_customer_id:
        raise AdsNotConfigured("the connection profile has no Google Ads customer id")
    existing = await db.fetch_one(
        "select id, status, started_at < now() - interval '1 hour' as stale from runs "
        "where project_id = %s and kind = %s and run_date = %s", (project_id, KIND, today))
    if existing and not force and (existing["status"] == "done" or (existing["status"] == "running" and not existing["stale"])):
        return {"run_id": str(existing["id"]), "status": "skipped", "reason": f"already {existing['status']} today"}
    if existing:
        await db.execute("delete from runs where id = %s", (existing["id"],))
    row = await db.fetch_one("insert into runs (project_id, kind, run_date) values (%s, %s, %s) returning id",
                             (project_id, KIND, today))
    rid = str(row["id"])
    try:
        data = {k: await client.search(q, validate=False) for k, q in queries(today).items()}
        result = evaluate(data, await previous_state(project_id, today), today)
        n = len(result["findings"])
        summary = "Nothing needs attention." if not result["attention"] else \
            f"{sum(f['severity'] != 'low' for f in result['findings'])} thing(s) need attention."
        if result["first_check"]:
            summary += " First check: changes are tracked from now on."
        await db.execute(
            "update runs set status = 'done', finished_at = now(), attention = %s, summary = %s, data = %s::jsonb "
            "where id = %s", (result["attention"], summary, json.dumps(result), rid))
        return {"run_id": rid, "status": "done", "summary": summary, "findings": n, **result}
    except Exception as e:
        await db.execute("update runs set status = 'failed', finished_at = now(), error = %s where id = %s",
                         (str(e)[:500], rid))
        raise


async def recent(project_id: str, limit: int = 10) -> list[dict]:
    rows = await db.fetch_all(
        "select id, kind, run_date, status, attention, summary, error, started_at, finished_at, "
        "data->'findings' as findings, data->'metrics' as metrics from runs where project_id = %s "
        "order by started_at desc limit %s", (project_id, limit))
    for r in rows:
        r["id"] = str(r["id"])
        for k in ("run_date", "started_at", "finished_at"):
            if r.get(k) is not None:
                r[k] = r[k].isoformat()
    return rows
