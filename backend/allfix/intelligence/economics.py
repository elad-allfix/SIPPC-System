"""Advertising economics: deterministic arithmetic the strategist calls as a tool.

Every input is a range (low, high) so uncertainty flows through to the result.
A single number is treated as low == high. The result shows the formula, the
low / mid / high outcome, and which input moves the answer most, so the
strategist can say what the client must pin down first.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

INPUTS = {
    "conversion_rate": "share of clicks that take the tracked action (lead, call, purchase)",
    "close_rate": "share of those actions that become paying customers (1 if the action is the sale)",
    "value_per_customer": "revenue (or lifetime value) per customer, in currency",
    "contribution_margin": "share of that value left after COGS and variable costs",
    "acquisition_share": "share of the contribution the business will spend to acquire a customer (1 = break-even)",
}


@dataclass
class Range:
    low: float
    high: float

    @property
    def mid(self) -> float:
        return (self.low + self.high) / 2

    @classmethod
    def parse(cls, name: str, raw) -> "Range":
        if isinstance(raw, (int, float)):
            lo = hi = float(raw)
        elif isinstance(raw, dict):
            lo = float(raw.get("low", raw.get("value")))
            hi = float(raw.get("high", raw.get("value", lo)))
        elif isinstance(raw, (list, tuple)) and len(raw) == 2:
            lo, hi = float(raw[0]), float(raw[1])
        else:
            raise ValueError(f"{name}: give a number, [low, high] or {{low, high}}")
        if lo > hi:
            lo, hi = hi, lo
        if lo < 0:
            raise ValueError(f"{name}: must not be negative")
        if name in ("conversion_rate", "close_rate", "contribution_margin") and hi > 1:
            raise ValueError(f"{name}: give a share between 0 and 1 (e.g. 0.08 for 8%)")
        return cls(lo, hi)


def _value_per_click(v: dict[str, float]) -> float:
    return (v["conversion_rate"] * v["close_rate"] * v["value_per_customer"]
            * v["contribution_margin"])


def _r(x: float) -> float:
    return round(x, 4) if abs(x) < 10 else round(x, 2)


def calculate(inputs: dict, cpc: dict | list | float | None = None) -> dict:
    ranges = {}
    for name in INPUTS:
        if name == "close_rate" and name not in inputs:
            ranges[name] = Range(1.0, 1.0)
        elif name == "acquisition_share" and name not in inputs:
            ranges[name] = Range(1.0, 1.0)
        elif name not in inputs:
            raise ValueError(f"missing input: {name} ({INPUTS[name]})")
        else:
            ranges[name] = Range.parse(name, inputs[name])

    names = list(INPUTS)
    # Extremes over every corner of the input box (the function is monotone,
    # so corners bound the result).
    corners = []
    for combo in product(*[(ranges[n].low, ranges[n].high) for n in names]):
        corners.append(dict(zip(names, combo)))
    mids = {n: ranges[n].mid for n in names}

    vpc = [_value_per_click(c) for c in corners]
    vpc_mid = _value_per_click(mids)
    max_cpc = [_value_per_click(c) * c["acquisition_share"] for c in corners]
    max_cpc_mid = vpc_mid * mids["acquisition_share"]

    # Sensitivity: swing in max affordable CPC when one input moves low -> high
    # with the others at their midpoints.
    sensitivity = []
    for n in names:
        if ranges[n].low == ranges[n].high:
            continue
        lo = dict(mids, **{n: ranges[n].low})
        hi = dict(mids, **{n: ranges[n].high})
        swing = _value_per_click(hi) * hi["acquisition_share"] - _value_per_click(lo) * lo["acquisition_share"]
        sensitivity.append({"input": n, "swing_in_max_cpc": _r(swing)})
    sensitivity.sort(key=lambda s: -abs(s["swing_in_max_cpc"]))

    customer_value_mid = mids["value_per_customer"] * mids["contribution_margin"]
    result = {
        "formula": "value per click = conversion_rate x close_rate x value_per_customer x contribution_margin; "
                   "max affordable CPC = value per click x acquisition_share",
        "inputs": {n: {"low": ranges[n].low, "high": ranges[n].high} for n in names},
        "value_per_click": {"low": _r(min(vpc)), "mid": _r(vpc_mid), "high": _r(max(vpc))},
        "max_affordable_cpc": {"low": _r(min(max_cpc)), "mid": _r(max_cpc_mid), "high": _r(max(max_cpc))},
        "contribution_per_customer_mid": _r(customer_value_mid),
        "break_even_roas_on_revenue": {
            "low": _r(1 / ranges["contribution_margin"].high) if ranges["contribution_margin"].high else None,
            "high": _r(1 / ranges["contribution_margin"].low) if ranges["contribution_margin"].low else None,
            "note": "1 / contribution margin; valid only when reported conversion value is revenue on the same base",
        },
        "most_sensitive_inputs": sensitivity,
    }

    if cpc is not None:
        c = Range.parse("cpc", cpc)
        mid_rate = mids["conversion_rate"] * mids["close_rate"]
        result["at_given_cpc"] = {
            "cpc": {"low": c.low, "high": c.high},
            "cost_per_customer_mid": _r(c.mid / mid_rate) if mid_rate else None,
            "contribution_per_click_after_cost_mid": _r(vpc_mid - c.mid),
            "verdict_mid": ("affordable" if c.mid <= max_cpc_mid else "above the affordable CPC")
                           + " at mid-point inputs",
            "covered_in_all_cases": max(c.high, 0) <= min(max_cpc),
            "fails_in_all_cases": c.low > max(max_cpc),
        }
    return result
