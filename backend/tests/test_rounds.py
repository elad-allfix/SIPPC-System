"""Phase 6: the daily account check (deterministic) and the forecast ledger in the project brief."""
from datetime import date, timedelta

import httpx

from allfix import store
from allfix.ads import checks
from allfix.ads.client import AdsClient
from allfix.strategist.prompt import project_brief
from test_connectivity import PROFILE, ads_settings, google, make_guard  # noqa: F401 (fixture)

TODAY = date(2026, 10, 13)


def daily(days: int, cost: float, conv: float, last_days_conv: float | None = None, is_=0.6, last_is=None):
    rows = []
    y = TODAY - timedelta(days=1)
    for i in range(days):
        d = y - timedelta(days=i)
        recent = i < 3
        rows.append({"campaign.id": "1", "campaign.name": "Search", "segments.date": str(d),
                     "metrics.costMicros": str(int(cost * 1e6)),
                     "metrics.conversions": last_days_conv if (recent and last_days_conv is not None) else conv,
                     "metrics.searchImpressionShare": last_is if (i < 7 and last_is is not None) else is_})
    return rows


def data(**kw):
    base = {
        "customer": [{"customer.autoTaggingEnabled": True, "customer.currencyCode": "ILS"}],
        "settings": [{"campaign.id": "1", "campaign.name": "Search", "campaign.status": "ENABLED",
                      "campaign.biddingStrategyType": "MANUAL_CPC", "campaignBudget.amountMicros": "100000000"}],
        "conversion_actions": [{"conversionAction.id": "9", "conversionAction.name": "Calls 60s",
                                "conversionAction.status": "ENABLED", "conversionAction.primaryForGoal": True,
                                "conversionAction.countingType": "ONE_PER_CLICK"}],
        "daily": daily(31, 100, 2),
        "terms": [{"searchTermView.searchTerm": "locksmith tel aviv", "metrics.costMicros": "50000000",
                   "metrics.conversions": 3}],
    }
    base.update(kw)
    return base


def test_quiet_account_needs_nothing():
    first = checks.evaluate(data(), None, TODAY)
    assert first["first_check"] and not first["attention"]
    again = checks.evaluate(data(), first["state"], TODAY)
    assert again["findings"] == [] and again["metrics"]["baseline_days"] == 28


def test_changes_since_last_check_are_verified():
    prev = checks.evaluate(data(), None, TODAY)["state"]
    changed = data(customer=[{"customer.autoTaggingEnabled": False}],
                   conversion_actions=[{"conversionAction.id": "9", "conversionAction.name": "Calls 60s",
                                        "conversionAction.status": "ENABLED", "conversionAction.primaryForGoal": False,
                                        "conversionAction.countingType": "ONE_PER_CLICK"}],
                   settings=[{"campaign.id": "1", "campaign.name": "Search", "campaign.status": "ENABLED",
                              "campaign.biddingStrategyType": "MAXIMIZE_CONVERSIONS",
                              "campaignBudget.amountMicros": "100000000"}])
    out = checks.evaluate(changed, prev, TODAY)
    titles = [f["title"] for f in out["findings"]]
    assert "Auto-tagging changed" in titles
    assert "No enabled primary conversion action" in titles
    assert any("primary: True -> False" in f["detail"] for f in out["findings"])
    assert any("bidding: MANUAL_CPC -> MAXIMIZE_CONVERSIONS" in f["detail"] for f in out["findings"])
    assert all(f["label"] == "verified" for f in out["findings"]) and out["findings"][0]["severity"] == "high"


def test_conversion_drop_needs_enough_expected_volume():
    out = checks.evaluate(data(daily=daily(31, 100, 2, last_days_conv=0)), None, TODAY)
    assert any(f["check"] == "conversions" for f in out["findings"])          # expected 6, got 0
    low = checks.evaluate(data(daily=daily(31, 100, 0.5, last_days_conv=0)), None, TODAY)
    assert not any(f["check"] == "conversions" for f in low["findings"])      # expected 1.5: could be luck


def test_spend_jump_and_impression_share_drop():
    rows = daily(31, 100, 2, last_is=0.3)
    for r in rows[:3]:
        r["metrics.costMicros"] = str(int(200e6))
    out = checks.evaluate(data(daily=rows), None, TODAY)
    checks_seen = {f["check"] for f in out["findings"]}
    assert {"spend", "impression_share"} <= checks_seen


def test_young_account_skips_baseline_checks():
    out = checks.evaluate(data(daily=daily(10, 100, 2, last_days_conv=0)), None, TODAY)
    assert "note" in out["metrics"] and not any(f["check"] in ("spend", "conversions") for f in out["findings"])


def test_new_costly_terms_against_last_check():
    prev = checks.evaluate(data(), None, TODAY)["state"]
    terms = data()["terms"] + [
        {"searchTermView.searchTerm": "locksmith course", "metrics.costMicros": "40000000", "metrics.conversions": 0},
        {"searchTermView.searchTerm": "locksmith jobs", "searchTermView.status": "EXCLUDED",
         "metrics.costMicros": "30000000", "metrics.conversions": 0}]
    out = checks.evaluate(data(terms=terms), prev, TODAY)
    f = next(f for f in out["findings"] if f["check"] == "search_terms")
    assert "locksmith course" in f["detail"] and "locksmith jobs" not in f["detail"]


async def test_run_once_per_day_and_brief_shows_it(database, ads_settings):  # noqa: F811
    p = await store.create_project({"name": "Locksmith", "entry_path": "ads_account"})
    profile = PROFILE.__class__(**{**PROFILE.__dict__, "project_id": p["id"]})
    payload = data()

    def api(req: httpx.Request):
        q = __import__("json").loads(req.content)["query"]
        kind = next(k for k, text in checks.queries(TODAY).items() if text == q)
        return httpx.Response(200, json=[{"results": [_nest(r) for r in payload[kind]]}])

    async with AdsClient(profile, guard=make_guard(), inner_transport=google(api)) as c:
        first = await checks.run(p["id"], c, today=TODAY)
        again = await checks.run(p["id"], c, today=TODAY)
        forced = await checks.run(p["id"], c, today=TODAY, force=True)
    assert first["status"] == "done" and again["status"] == "skipped" and forced["status"] == "done"
    assert "First check" in first["summary"]
    runs = await checks.recent(p["id"])
    assert len(runs) == 1 and runs[0]["status"] == "done"

    await store.create_item(p["id"], {"stage": 6, "kind": "forecast", "title": "CPA falls below 120 ILS",
                                      "label": "hypothesis", "data": {"review_after": "2026-10-01"}})
    await store.create_item(p["id"], {"stage": 6, "kind": "forecast", "title": "Later one",
                                      "label": "hypothesis", "data": {"review_after": "2099-01-01"}})
    brief = await project_brief(p["id"])
    assert "due for review" in brief and "CPA falls below 120 ILS" in brief and "Later one (id" not in brief
    assert "Latest daily account check" in brief


def _nest(flat: dict) -> dict:
    """Turn {"a.b": 1} back into the API's nested shape."""
    out: dict = {}
    for k, v in flat.items():
        cur = out
        parts = k.split(".")
        for part in parts[:-1]:
            cur = cur.setdefault(part, {})
        cur[parts[-1]] = v
    return out


def test_forecasts_and_experiments_need_review_fields():
    import pytest
    from allfix.strategist.tools import ToolError, _check_review_fields
    with pytest.raises(ToolError, match="review_after"):
        _check_review_fields({"kind": "forecast", "data": {"prediction": "x", "metric": "CPA"}})
    with pytest.raises(ToolError, match="YYYY-MM-DD"):
        _check_review_fields({"kind": "experiment", "data": {"hypothesis": "h", "success_metric": "m",
                                                              "review_after": "in 4 weeks"}})
    _check_review_fields({"kind": "forecast", "data": {"prediction": "x", "metric": "CPA", "review_after": "2026-11-10"}})
    _check_review_fields({"kind": "finding", "data": {}})


def test_economics_cpc_scenarios():
    from allfix.intelligence import economics
    out = economics.calculate({"conversion_rate": [0.1, 0.2], "close_rate": 0.5, "value_per_customer": 400,
                               "contribution_margin": 0.5, "acquisition_share": 0.5},
                              cpc_scenarios=[30, 5, 15], clicks=150)
    rows = out["scenarios"]["rows"]
    assert [r["cpc"] for r in rows] == [5, 15, 30] and rows[0]["test_spend"] == 750
    assert rows[0]["customers"] == {"low": 7.5, "mid": 11.25, "high": 15}
    # max affordable CPC: low 5, mid 7.5, high 10
    assert [r["within_affordable_cpc"] for r in rows] == ["all cases", "no case", "no case"]


def test_question_item_holds_one_question():
    import pytest
    from allfix.strategist.tools import ToolError, _check_single_question
    _check_single_question({"kind": "question", "title": "What share of calls become signed cases?"})
    _check_single_question({"kind": "finding", "title": "Who pays? Who decides?"})
    for bundled in ("What is the website URL, and what event marks an activated trial?", "Close rate? Margin?"):
        with pytest.raises(ToolError, match="one question"):
            _check_single_question({"kind": "question", "title": bundled})
