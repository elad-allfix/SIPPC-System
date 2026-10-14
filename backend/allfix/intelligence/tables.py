"""Read report exports the user uploads (Google Ads UI CSV/TSV, CRM lists) into rows.

Google Ads exports put a title and the date range above the header and "Total: ..." rows at the
bottom; the "Excel CSV" variant is UTF-16 and tab-separated. Hebrew-language exports use Hebrew
column names. Empty cells show as "--". Nothing here guesses: what cannot be parsed stays text.
"""

from __future__ import annotations

import csv
import io
import math
import re
from dataclasses import dataclass, field
from typing import Any

MAX_LIMIT = 200
csv.field_size_limit(16 * 1024 * 1024)  # long ad text and change-history cells
EMPTY = {"", "--", "-", "—", "n/a", "N/A", " --"}
TOTAL_PREFIXES = ("total", "סה\"כ", "סה״כ", "סך הכל", "סיכום")
# Columns whose numbers are rates, averages or ratios: summing them is meaningless.
NON_ADDITIVE = re.compile(
    r"avg|average|rate|ctr|cpc|cpm|cpa|roas|share|%|/|per |position|score|ratio|"
    r"ממוצע|שיעור|נתח|אחוז|ציון|יחס|עלות ל", re.I)
_CURRENCY = re.compile(r"[A-Z]{0,3}[₪$€£¥]|\b(?:ILS|USD|EUR|GBP|CAD|AUD|NZD|CHF|JPY|INR|BRL|MXN|ZAR)\b|[\s ]")


@dataclass
class Table:
    columns: list[str]
    rows: list[list[str]]
    preamble: list[str] = field(default_factory=list)
    footer: list[list[str]] = field(default_factory=list)
    delimiter: str = ","


def decode(data: bytes) -> str:
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        return data.decode("utf-16")
    if data.startswith(b"\xef\xbb\xbf"):
        return data[3:].decode("utf-8", errors="replace")
    head = data[:2000]
    if head and head.count(b"\x00") > len(head) // 4:  # UTF-16 without a byte-order mark
        return data.decode("utf-16-le" if head[1:2] == b"\x00" else "utf-16-be", errors="replace")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("cp1255", errors="replace")  # older Hebrew Windows exports


def _is_total(row: list[str]) -> bool:
    first = next((c.strip() for c in row if c.strip()), "")
    return first.lower().startswith(TOTAL_PREFIXES)


def _rows(text: str, delim: str) -> list[list[str]]:
    # csv over the whole text, so quoted cells that hold line breaks (ad text, change history)
    # keep them instead of being glued to the next line.
    return list(csv.reader(io.StringIO(text), delimiter=delim))


def _find_header(text: str) -> tuple[int, int, str]:
    """(columns, header row index, delimiter), judged on the start of the file."""
    sample = text[:200_000]
    best: tuple[int, int, str] | None = None
    for delim in ("\t", ",", ";"):
        rows = _rows(sample, delim)
        for i, r in enumerate(rows[:15]):
            n = len(r)
            if n < 2 or not any(c.strip() for c in r):
                continue
            nxt = next((x for x in rows[i + 1:] if any(c.strip() for c in x)), None)
            if nxt is None or len(nxt) == n:
                if best is None or n > best[0]:
                    best = (n, i, delim)
                break
    if best is None:
        raise ValueError("no table found: the file has no header row with two or more columns")
    return best


def _text(data: bytes) -> str:
    return decode(data).replace("\r\n", "\n").replace("\r", "\n")


def parse(data: bytes) -> Table:
    text = _text(data)
    n, h, delim = _find_header(text)
    rows = _rows(text, delim)
    columns, seen = [], {}
    for c in rows[h]:
        name = c.strip() or f"column {len(columns) + 1}"
        if name in seen:
            seen[name] += 1
            name = f"{name} ({seen[name]})"
        else:
            seen[name] = 1
        columns.append(name)
    body, footer = [], []
    for r in rows[h + 1:]:
        if not any(c.strip() for c in r):
            continue
        r = (r + [""] * n)[:n]
        (footer if _is_total(r) else body).append(r)
    preamble = [" ".join(c.strip() for c in r if c.strip()) for r in rows[:h] if any(c.strip() for c in r)]
    return Table(columns=columns, rows=body, preamble=preamble, footer=footer, delimiter=delim)


def number(cell: str) -> float | None:
    """'1,234.56' -> 1234.56, 'CA$12.30' -> 12.3, '1.234,50' -> 1234.5, '8.57%' -> 8.57;
    '--' or text -> None. A lone '1.000' reads as one: Google Ads exports in English and Hebrew
    use dots for decimals, and a single cell cannot tell which convention a file uses."""
    s = cell.strip()
    if s in EMPTY or s.startswith(("<", ">")):
        return None
    s = _CURRENCY.sub("", s).rstrip("%")
    neg = s.startswith("(") and s.endswith(")") or s.startswith("-")
    s = s.strip("()").lstrip("-")
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif s.count(".") > 1:  # 1.234.567: dots as thousands separators
        s = s.replace(".", "")
    elif "," in s:
        # 1,234 or 1,234,567 are thousands; 12,5 or 1234,56 are decimal commas
        s = s.replace(",", "") if re.fullmatch(r"\d{1,3}(,\d{3})+", s) else s.replace(",", ".")
    try:
        v = float(s)
    except ValueError:
        return None
    if not math.isfinite(v):
        return None
    return -v if neg else v


def _column(table: Table, name: str) -> int:
    want = name.strip().lower()
    for i, c in enumerate(table.columns):
        if c.lower() == want:
            return i
    matches = [i for i, c in enumerate(table.columns) if c.lower().startswith(want)]
    if len(matches) == 1:
        return matches[0]
    raise ValueError(f"no single column called {name!r}; columns are {table.columns}")


def additive_columns(table: Table, rows: list[list[str]]) -> list[int]:
    out = []
    for i, c in enumerate(table.columns):
        if NON_ADDITIVE.search(c):
            continue
        cells = [r[i].strip() for r in rows if r[i].strip() not in EMPTY]
        if not cells or any(x.endswith("%") for x in cells[:50]):
            continue
        if sum(number(x) is not None for x in cells) >= 0.9 * len(cells):
            out.append(i)
    return out


REDUCED_MARK = "AllFix reduced this file on arrival"
# (report type, columns that identify it). Checked in order; the first match wins.
REPORT_TYPES: list[tuple[str, tuple[str, ...]]] = [  # (report type, column names that identify it)
    ("change history", ("changes", "שינויים")),
    ("search terms", ("search term", "מונח חיפוש")),
    ("auction insights", ("overlap rate", "שיעור חפיפה")),
    ("conversion actions", ("conversion action", "פעולת המרה")),
    ("ads and assets", ("headline", "asset", "כותרת", "נכס")),
    ("keywords", ("keyword", "מילת מפתח")),
    ("ad groups", ("ad group", "קבוצת מודעות")),
    ("campaigns", ("campaign", "קמפיין")),
]


def report_type(table: Table) -> str | None:
    """Checked in order, the first match wins: most exports also carry Campaign and Ad group."""
    cols = [c.lower() for c in table.columns]
    for name, names in REPORT_TYPES:
        if any(c.startswith(n) for c in cols for n in names):
            return name
    return None


def _find(columns: list[str], names: tuple[str, ...]) -> int | None:
    low = [c.lower().strip() for c in columns]
    for n in names:
        if n in low:
            return low.index(n)
    for n in names:
        hits = [i for i, c in enumerate(low) if c.startswith(n) and not NON_ADDITIVE.search(c)]
        if hits:
            return hits[0]
    return None


COST = ("cost", "עלות")
CONVERSIONS = ("conversions", "conv.", "המרות")
CLICKS = ("clicks", "קליקים")
IMPRESSIONS = ("impr.", "impressions", "חשיפות")
LEVEL = ("level", "asset level", "רמה")


def _account_total(footer: list[list[str]]) -> list[str] | None:
    """The account-wide Total row: 'Total: Account' when there are several, else the only one."""
    if not footer:
        return None
    for r in footer:
        first = next((c.strip().lower() for c in r if c.strip()), "")
        if "account" in first or "חשבון" in first:
            return r
    return footer[0] if len(footer) == 1 else None


def check_totals(table: Table, sums: dict[str, float]) -> dict[str, Any]:
    """Compare row sums with the file's own Total row, so a report that lists the same money at
    several levels, or a filtered or reduced file, is caught instead of trusted."""
    if any(REDUCED_MARK in p for p in table.preamble):
        return {"totals_note": "This file was reduced on arrival (see the preamble). Row sums cover only "
                               "the kept rows; the Total rows and the full-file sums in the preamble are the "
                               "whole file's. Use those for account totals."}
    total = _account_total(table.footer)
    if total is None:
        note = ("The file has no Total row, so these sums cannot be checked against it." if not table.footer
                else "The file has several Total rows and none is account-wide; compare sums with care.")
        return {"totals_note": note}
    off = {}
    for name, got in sums.items():
        want = number(total[table.columns.index(name)])
        if want is None:
            continue
        if abs(got - want) > max(0.01 * abs(want), 1):
            off[name] = {"rows_add_up_to": got, "file_total_says": want}
    if not off:
        return {"totals_check": "row sums match the file's own Total row"}
    if report_type(table) == "search terms" and all(v["rows_add_up_to"] < v["file_total_says"] for v in off.values()):
        return {"totals_note": "Rows add up to less than the file's Total row. In a search terms report that is "
                               "expected: Google's total includes searches it does not list, so the gap is the "
                               "traffic on hidden searches (or the file is filtered). Use the Total row for totals.",
                "totals_mismatch": off}
    return {"totals_warning": "Row sums do not match the file's own Total row. The report may list the same "
                              "money at several levels (see totals_by_level if present), or the file is "
                              "filtered or edited. Use the Total row for totals, not these sums.",
            "totals_mismatch": off}


def query(table: Table, contains: str | None = None, sort_by: str | None = None,
          descending: bool = True, offset: int = 0, limit: int = 50,
          columns: list[str] | None = None) -> dict[str, Any]:
    rows = table.rows
    if contains:
        needle = contains.lower()
        rows = [r for r in rows if any(needle in c.lower() for c in r)]
    if sort_by:
        k = _column(table, sort_by)
        present = [r for r in rows if number(r[k]) is not None]
        absent = [r for r in rows if number(r[k]) is None]
        if present and len(present) >= len(absent):
            rows = sorted(present, key=lambda r: number(r[k]), reverse=descending) + absent
        else:  # a text column
            rows = sorted(rows, key=lambda r: r[k].lower(), reverse=descending)
    keep = [_column(table, c) for c in columns] if columns else list(range(len(table.columns)))
    limit = max(1, min(int(limit), MAX_LIMIT))
    offset = max(0, int(offset))
    page = rows[offset:offset + limit]
    totals = {table.columns[i]: round(sum(number(r[i]) or 0 for r in rows), 2)
              for i in additive_columns(table, rows)}
    out: dict[str, Any] = {
        "preamble": table.preamble,
        "columns": table.columns,
        "rows_in_file": len(table.rows),
        "rows_matching": len(rows),
        "totals_of_matching_rows": totals,
        "offset": offset,
        "rows": [{table.columns[i]: r[i] for i in keep} for r in page],
    }
    kind = report_type(table)
    if kind:
        out["report_type"] = kind
    level = _find(table.columns, LEVEL)
    if level is not None:
        by: dict[str, dict[str, float]] = {}
        summed = additive_columns(table, rows)
        for r in rows:
            d = by.setdefault(r[level].strip() or "(blank)", {})
            for i in summed:
                d[table.columns[i]] = round(d.get(table.columns[i], 0) + (number(r[i]) or 0), 2)
        out["totals_by_level"] = by
    if table.footer:
        out["total_rows_in_file"] = [dict(zip(table.columns, r)) for r in table.footer]
    if not contains:
        out.update(check_totals(table, totals))
    if offset + limit < len(rows):
        out["more"] = f"{len(rows) - offset - limit} more rows; pass offset={offset + limit}"
    return out


def _fmt(v: float) -> str:
    return f"{v:,.0f}" if abs(v) >= 100 or v == int(v) else f"{v:,.2f}"


def reduce(data: bytes, cap: int) -> tuple[bytes, str]:
    """Shrink a large report export to at most about `cap` bytes before it is stored, and say
    exactly what was kept. Rows that never cost money or converted are dropped first (a search
    terms report is mostly those); if that is not enough, the highest-cost rows are kept. Change
    history keeps its first rows (Google Ads lists the newest first). Full-file sums go into the
    preamble so totals stay true after the cut. Returns (CSV bytes, one-line summary)."""
    text = _text(data)
    n, h, delim = _find_header(text)
    reader = csv.reader(io.StringIO(text), delimiter=delim)
    preamble: list[str] = []
    for _ in range(h):
        r = next(reader)
        if any(c.strip() for c in r):
            preamble.append(" ".join(c.strip() for c in r if c.strip()))
    columns = next(reader)
    probe = Table(columns=[c.strip() for c in columns], rows=[])
    kind = report_type(probe)
    cost, conv = _find(probe.columns, COST), _find(probe.columns, CONVERSIONS)
    clicks, impr = _find(probe.columns, CLICKS), _find(probe.columns, IMPRESSIONS)
    watched = {name: i for name, i in (("cost", cost), ("conversions", conv), ("clicks", clicks),
                                       ("impressions", impr)) if i is not None}
    full = dict.fromkeys(watched, 0.0)
    dropped = dict.fromkeys(watched, 0.0)
    kept: list[list[str]] = []
    footer: list[list[str]] = []
    seen = n_dropped = 0
    by_value = kind != "change history" and (cost is not None or conv is not None)
    for r in reader:
        if not any(c.strip() for c in r):
            continue
        r = (r + [""] * n)[:n]
        if _is_total(r):
            footer.append(r)
            continue
        seen += 1
        vals = {k: number(r[i]) or 0.0 for k, i in watched.items()}
        for k, v in vals.items():
            full[k] += v
        if by_value and vals.get("cost", 0) <= 0 and vals.get("conversions", 0) <= 0:
            n_dropped += 1
            for k, v in vals.items():
                dropped[k] += v
            continue
        kept.append(r)
    why = "every row with cost or conversions above 0" if by_value else "the first rows in the file's order"
    def nbytes(r: list[str]) -> int:
        return len(",".join(r).encode()) + 2 * len(r) + 1  # utf-8 bytes, with room for quotes

    size = sum(nbytes(r) for r in kept)
    if size > cap:
        if by_value:
            k = cost if cost is not None else conv
            kept.sort(key=lambda r: number(r[k]) or 0, reverse=True)
            why = f"the highest-{'cost' if cost is not None else 'conversion'} rows"
        out, size = [], 0
        for r in kept:
            size += nbytes(r)
            if size > cap:
                break
            out.append(r)
        kept = out
    share = []
    for k in ("cost", "conversions"):
        if k in watched and full[k]:
            got = sum(number(r[watched[k]]) or 0 for r in kept)
            share.append(f"{100 * got / full[k]:.1f}% of its {k}")
    summary = (f"{REDUCED_MARK}: kept {len(kept):,} of {seen:,} rows ({why})"
               + (f", covering {' and '.join(share)}" if share else "") + ".")
    notes = [summary]
    if n_dropped:
        had = ", ".join(f"{_fmt(v)} {k}" for k, v in dropped.items() if k in ("impressions", "clicks"))
        notes.append(f"Dropped {n_dropped:,} rows with no cost and no conversions"
                     + (f"; together they had {had}." if had else "."))
    if full:
        notes.append("Full-file sums before reducing: " + ", ".join(f"{k} {_fmt(v)}" for k, v in full.items()) + ".")
    buf = io.StringIO()
    w = csv.writer(buf)
    for line in preamble + notes:
        w.writerow([line])
    w.writerow(columns)
    w.writerows(kept)
    w.writerows(footer)
    return buf.getvalue().encode("utf-8"), summary
