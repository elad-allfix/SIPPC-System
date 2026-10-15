"""Keyword gaps: searches that already bring clicks but are not keywords yet.

Reads an uploaded search terms report and, when given, the keywords report. A search term counts as
covered when its text, lowercased and stripped of match-type symbols, equals a keyword's text or the
report marks it Added. Everything here is observed from the user's own exports; nothing is estimated.
"""

from __future__ import annotations

import re
from typing import Any

from .tables import CLICKS, CONVERSIONS, COST, EMPTY, IMPRESSIONS, Table, _find, number

TERM = ("search term", "מונח חיפוש")
KEYWORD = ("keyword", "search keyword", "מילת מפתח")
ADDED = ("added/excluded", "נוסף/הוחרג")
CAMPAIGN = ("campaign", "קמפיין")
MATCH = ("match type", "סוג התאמה")
STOP = {"a", "an", "the", "in", "for", "of", "to", "my", "and", "or", "is", "on", "at", "with", "by", "from",
        "your", "you", "i", "me", "near"}
_SYMBOLS = re.compile(r'[\[\]"+]')


def normalise(text: str) -> str:
    return " ".join(_SYMBOLS.sub(" ", text).lower().split())


def _col(table: Table, names: tuple[str, ...], required: bool = False) -> int | None:
    i = _find(table.columns, names)
    if i is None and required:
        raise ValueError(f"no {names[0]!r} column in this file; its columns are {table.columns}")
    return i


def _num(row: list[str], i: int | None) -> float:
    if i is None or row[i].strip() in EMPTY:
        return 0.0
    return number(row[i]) or 0.0


def _rate(a: float, b: float) -> float | None:
    return round(a / b, 4) if b else None


def keyword_gaps(terms: Table, keywords: Table | None = None, min_clicks: float = 3, limit: int = 40,
                 contains: str | None = None) -> dict[str, Any]:
    t = _col(terms, TERM, required=True)
    clicks, impr = _col(terms, CLICKS), _col(terms, IMPRESSIONS)
    cost, conv = _col(terms, COST), _col(terms, CONVERSIONS)
    added, camp, match = _col(terms, ADDED), _col(terms, CAMPAIGN), _col(terms, MATCH)

    covered: set[str] = set()
    vocab: set[str] = set()
    if keywords is not None:
        k = _col(keywords, KEYWORD, required=True)
        for r in keywords.rows:
            text = normalise(r[k])
            if text:
                covered.add(text)
                vocab.update(text.split())

    needle = contains.lower() if contains else None
    by_term: dict[str, dict[str, Any]] = {}
    all_clicks = covered_clicks = 0.0
    for r in terms.rows:
        status = r[added].strip().lower() if added is not None else ""
        if status.startswith("excluded"):
            continue
        text = normalise(r[t])
        where = text + " " + (r[camp].lower() if camp is not None else "")
        if not text or (needle and needle not in where):
            continue
        c = _num(r, clicks)
        all_clicks += c
        if text in covered or status.startswith("added"):
            covered_clicks += c
            continue
        d = by_term.setdefault(text, {"clicks": 0.0, "impressions": 0.0, "cost": 0.0, "conversions": 0.0,
                                      "campaigns": set(), "match_types": set()})
        d["clicks"] += c
        d["impressions"] += _num(r, impr)
        d["cost"] += _num(r, cost)
        d["conversions"] += _num(r, conv)
        if camp is not None:
            d["campaigns"].add(r[camp].strip())
        if match is not None:
            d["match_types"].add(r[match].strip())

    gaps = [(term, d) for term, d in by_term.items() if d["clicks"] >= min_clicks]
    gaps.sort(key=lambda kv: (kv[1]["clicks"], kv[1]["conversions"]), reverse=True)
    limit = max(1, min(int(limit), 200))

    # Words and word pairs that bring clicks but appear in no keyword: themes the account does not target.
    themes: dict[str, dict[str, float]] = {}
    for term, d in by_term.items():
        words = term.split()
        grams = {w for w in words if w not in STOP and len(w) > 2}
        grams |= {f"{a} {b}" for a, b in zip(words, words[1:]) if not (a in STOP and b in STOP)}
        for g in grams:
            if keywords is not None and all(w in vocab for w in g.split()):
                continue
            s = themes.setdefault(g, {"clicks": 0.0, "cost": 0.0, "conversions": 0.0, "terms": 0})
            s["clicks"] += d["clicks"]
            s["cost"] += d["cost"]
            s["conversions"] += d["conversions"]
            s["terms"] += 1
    top_themes = sorted(themes.items(), key=lambda kv: kv[1]["clicks"], reverse=True)[:25]

    def row(term: str, d: dict[str, Any]) -> dict[str, Any]:
        return {"search term": term, "clicks": round(d["clicks"]), "impressions": round(d["impressions"]),
                "ctr": _rate(d["clicks"], d["impressions"]), "cost": round(d["cost"], 2),
                "avg_cpc": _rate(d["cost"], d["clicks"]), "conversions": round(d["conversions"], 2),
                "campaigns": len(d["campaigns"]), "matched_as": sorted(d["match_types"])[:3]}

    return {
        "label": "observed: from the user's exports; conversions are only as good as the account's tracking",
        "preamble": terms.preamble,
        "compared_with_keywords": keywords is not None,
        "how_matched": "a search term is covered when its text, lowercased without match-type symbols, equals a "
                       "keyword's text or the report marks it Added; close variants of a keyword still show here",
        "filter": contains or None,
        "clicks_read": round(all_clicks),
        "clicks_from_terms_already_keywords": round(covered_clicks),
        "gap_terms_total": len(gaps),
        "gap_terms": [row(term, d) for term, d in gaps[:limit]],
        "themes_not_in_any_keyword" if keywords is not None else "themes": [
            {"words": g, "clicks": round(s["clicks"]), "cost": round(s["cost"], 2),
             "conversions": round(s["conversions"], 2), "search_terms": s["terms"]} for g, s in top_themes],
    }
