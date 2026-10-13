"""A small allowlist for GAQL queries the strategist may run."""

from __future__ import annotations

import re

ALLOWED_RESOURCES = {
    "customer", "campaign", "ad_group", "ad_group_ad", "ad_group_criterion", "keyword_view",
    "search_term_view", "campaign_budget", "bidding_strategy", "conversion_action", "geographic_view",
    "user_location_view", "landing_page_view", "expanded_landing_page_view", "asset", "campaign_asset",
    "ad_group_asset", "asset_group", "campaign_criterion", "shared_set", "shared_criterion",
    "campaign_search_term_insight", "age_range_view", "gender_view",
    "change_event", "recommendation", "customer_client", "label", "audience",
}
MAX_LIMIT = 1000


class GaqlError(ValueError):
    pass


def validate(query: str, default_limit: int = 200) -> str:
    """Return a safe version of the query or raise GaqlError."""
    q = " ".join(query.strip().split())
    if not q:
        raise GaqlError("empty query")
    if ";" in q:
        raise GaqlError("one query only, without ';'")
    if not re.match(r"(?i)^select\s", q):
        raise GaqlError("only SELECT queries are allowed")
    m = re.search(r"(?i)\sfrom\s+([a-z_]+)", q)
    if not m or m.group(1).lower() not in ALLOWED_RESOURCES:
        raise GaqlError(f"FROM must be one of: {', '.join(sorted(ALLOWED_RESOURCES))}")
    # GAQL puts LIMIT before an optional trailing PARAMETERS clause.
    params = ""
    pm = re.search(r"(?i)\sparameters\s.*$", q)
    if pm:
        q, params = q[: pm.start()], q[pm.start():]
    lim = re.search(r"(?i)\slimit\s+(\d+)\s*$", q)
    if lim:
        if int(lim.group(1)) > MAX_LIMIT:
            q = q[: lim.start()] + f" LIMIT {MAX_LIMIT}"
    else:
        q += f" LIMIT {min(default_limit, MAX_LIMIT)}"
    return q + params
