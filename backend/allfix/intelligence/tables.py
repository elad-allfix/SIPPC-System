"""Read report exports the user uploads (Google Ads UI CSV/TSV, CRM lists) into rows.

Google Ads exports put a title and the date range above the header and "Total: ..." rows at the
bottom; the "Excel CSV" variant is UTF-16 and tab-separated. Hebrew-language exports use Hebrew
column names. Empty cells show as "--". Nothing here guesses: what cannot be parsed stays text.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from typing import Any

MAX_LIMIT = 200
EMPTY = {"", "--", "-", "—", "n/a", "N/A", " --"}
TOTAL_PREFIXES = ("total", "סה\"כ", "סה״כ", "סך הכל", "סיכום")
# Columns whose numbers are rates, averages or ratios: summing them is meaningless.
NON_ADDITIVE = re.compile(
    r"avg|average|rate|ctr|cpc|cpm|cpa|roas|share|%|/|per |position|score|ratio|"
    r"ממוצע|שיעור|נתח|אחוז|ציון|יחס|עלות ל", re.I)
_CURRENCY = re.compile(r"[₪$€£¥\s ]|ILS|USD|EUR|GBP")


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


def parse(data: bytes) -> Table:
    text = decode(data).replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    best: tuple[int, int, str, list[list[str]]] | None = None  # (columns, header index, delimiter, rows)
    for delim in ("\t", ",", ";"):
        rows = list(csv.reader(lines, delimiter=delim))
        for i, r in enumerate(rows[:15]):
            n = len(r)
            if n < 2 or not any(c.strip() for c in r):
                continue
            nxt = next((x for x in rows[i + 1:] if any(c.strip() for c in x)), None)
            if nxt is None or len(nxt) == n:
                if best is None or n > best[0]:
                    best = (n, i, delim, rows)
                break
    if best is None:
        raise ValueError("no table found: the file has no header row with two or more columns")
    n, h, delim, rows = best
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
    preamble = [ln.strip() for ln in lines[:h] if ln.strip()]
    return Table(columns=columns, rows=body, preamble=preamble, footer=footer, delimiter=delim)


def number(cell: str) -> float | None:
    """'1,234.56' -> 1234.56, '₪12.30' -> 12.3, '8.57%' -> 8.57; '--' or text -> None."""
    s = cell.strip()
    if s in EMPTY or s.startswith(("<", ">")):
        return None
    s = _CURRENCY.sub("", s).rstrip("%")
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()").replace(",", "")
    try:
        v = float(s)
    except ValueError:
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
    if table.footer:
        out["total_rows_in_file"] = [dict(zip(table.columns, r)) for r in table.footer]
    if offset + limit < len(rows):
        out["more"] = f"{len(rows) - offset - limit} more rows; pass offset={offset + limit}"
    return out
