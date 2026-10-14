import pytest

from allfix.intelligence.economics import calculate


def test_point_values():
    r = calculate({"conversion_rate": 0.08, "close_rate": 0.1, "value_per_customer": 2200,
                   "contribution_margin": 0.12, "acquisition_share": 1 / 3})
    assert r["value_per_click"]["mid"] == pytest.approx(2.112, abs=1e-3)
    assert r["max_affordable_cpc"]["mid"] == pytest.approx(0.704, abs=1e-3)


def test_ranges_bound_the_result_and_rank_sensitivity():
    r = calculate({"conversion_rate": [0.05, 0.10], "close_rate": [0.10, 0.20],
                   "value_per_customer": 2000, "contribution_margin": 0.12})
    assert r["value_per_click"]["low"] == pytest.approx(0.05 * 0.10 * 2000 * 0.12)
    assert r["value_per_click"]["high"] == pytest.approx(0.10 * 0.20 * 2000 * 0.12)
    assert r["uncertainty_by_input"][0]["input"] in ("conversion_rate", "close_rate")
    assert r["break_even_roas_on_revenue"]["low"] == pytest.approx(1 / 0.12, rel=1e-3)


def test_compare_cpc():
    r = calculate({"conversion_rate": 0.1, "value_per_customer": 100, "contribution_margin": 0.5}, cpc=[2, 3])
    assert r["max_affordable_cpc"]["mid"] == pytest.approx(5)
    assert r["at_given_cpc"]["covered_in_all_cases"] is True
    assert r["at_given_cpc"]["cost_per_customer_mid"] == pytest.approx(25)


def test_rejects_percent_given_as_whole_number():
    with pytest.raises(ValueError, match="share between 0 and 1"):
        calculate({"conversion_rate": 8, "value_per_customer": 100, "contribution_margin": 0.5})


def test_missing_input():
    with pytest.raises(ValueError, match="missing input: contribution_margin"):
        calculate({"conversion_rate": 0.1, "value_per_customer": 100})


async def test_economics_reports_conflict_with_owner_fact(database):
    from allfix import store
    from allfix.strategist.tools import ToolContext, _calculate_economics
    p = await store.create_project({"name": "Doors"})
    await store.set_fact(p["id"], "value_per_customer", "400 CAD", "observed", "owner")
    r = await _calculate_economics(ToolContext(p["id"], "c"), {
        "conversion_rate": 0.08, "value_per_customer": [250, 600], "contribution_margin": 0.5,
        "segment": "garage doors", "currency": "CAD"})
    assert r["saved_as_facts"] == ["conversion_rate (garage doors)", "contribution_margin (garage doors)"]
    assert r["conflicts"] == [{"input": "value_per_customer", "fact": "value_per_customer: 400 CAD [observed]",
                               "used": "250-600 CAD"}]
