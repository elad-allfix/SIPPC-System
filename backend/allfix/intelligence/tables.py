"""Read report exports the user uploads (Google Ads UI CSV/TSV, CRM lists) into rows.

Google Ads exports put a title and the date range above the header and "Total: ..." rows at the
bottom; the "Excel CSV" variant is UTF-16 and tab-separated. Hebrew-language exports use Hebrew
column names. Empty cells show as "--". Cells can hold line breaks (asset text, change history).
Large files are condensed on upload (see condense) and stored gzip-compressed. Nothing here
guesses: what cannot be parsed stays text.
"""

from __future__ import annotations

import csv
import gzip
import io
import itertools
import re
from dataclasses import dataclass, field
from typing import Any

csv.field_size_limit(10_000_000)

MAX_LIMIT = 200
EMPTY = {"", "--", "-", "—", "n/a", "N/A", " --"}
TOTAL_PREFIXES = ("total", "סה\"כ", "סה״כ", "סך הכל", "סיכום")
# Columns whose numbers are rates, averages, bids or ratios: summing them is meaningless.
NON_ADDITIVE = re.compile(
    r"avg|average|rate|ctr|cpc|cpm|cpa|roas|share|%|/|per |position|score|ratio|bid|quality|"
    r"ממוצע|שיעור|נתח|אחוז|ציון|יחס|עלות ל|הצעת מחיר", re.I)
# "CA$12.30", "US$5", "₪12", "12.30 CAD", "EUR 4": symbols, prefixes and ISO codes are dropped.
_CURRENCY = re.compile(r"[A-Z]{0,3}[$€£¥₪]|[\s  ]|^[A-Z]{3}|[A-Z]{3}$")
# Activity columns used to decide which rows of a big export carry information. Impressions are left
# out on purpose: nearly every search term has some, and rows that never cost anything are not waste.
ACTIVITY = re.compile(r"^(cost|clicks|conversions|עלות|קליקים|המרות)$", re.I)
CONDENSED_NOTE = "AllFix condensed this upload"

# Google Ads report titles (first preamble line) and what to look at first in each.
REPORT_GUIDE: dict[str, str] = {
    "search terms report": "What people actually typed. Group by Search term or Campaign; look for spend on "
        "irrelevant intent (jobs, DIY, parts, for sale, competitors), terms that convert, and how much sits in "
        "'Total: Other search terms' (hidden queries).",
    "search keyword report": "Your keywords. Weight Quality Score parts (Exp. CTR, Ad relevance, Landing page exp.) "
        "by Cost, split cost by Match type, and find keywords with spend but no conversions.",
    "ad group report": "Structure. Count ad groups with and without spend; very many thin ad groups means too "
        "little data per group to learn from.",
    "campaign report": "Where the money goes: cost, clicks and conversions per campaign, bidding strategy and "
        "budget limits.",
    "ad report": "Ad copy. Count headlines and descriptions per spending ad (15 and 4 allowed), Ad strength, "
        "pinning, and the Final URL each ad sends people to.",
    "change history report": "What was changed and when. Group by month and by change type, look for bursts of "
        "bid changes, and line them up with the time series before blaming or crediting a change.",
    "negative keyword report": "Blocked searches. Look for duplicates copied campaign by campaign instead of shared "
        "lists, and negatives that block searches you want.",
    "device report": "Rows can repeat the same spend at campaign and ad group level: filter by Level before adding. "
        "Compare cost and conversions by device.",
    "landing page report": "Spend and clicks per page and per website. Mobile speed score and mobile-friendly "
        "click rate show page problems.",
    "auction insights report": "Who you compete with: impression share, overlap and outranking share per domain. "
        "Percentages: never add them.",
    "asset association report": "Sitelinks, callouts and other assets. The same spend repeats for every asset and "
        "level shown, so never add Cost or Clicks across rows.",
}


@dataclass
class Table:
    columns: list[str]
    rows: list[list[str]]
    preamble: list[str] = field(default_factory=list)
    footer: list[list[str]] = field(default_factory=list)
    delimiter: str = ","


def decode(data: bytes) -> str:
    if data.startswith(b"\x1f\x8b"):  # stored compressed (big uploads)
        data = gzip.decompress(data)
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


def _layout(text: str) -> tuple[int, int, str]:
    """(columns, header record index, delimiter) from the first records only."""
    best: tuple[int, int, str] | None = None
    for delim in ("\t", ",", ";"):
        rows = list(itertools.islice(csv.reader(io.StringIO(text, newline=""), delimiter=delim), 40))
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


def _names(header: list[str]) -> list[str]:
    columns, seen = [], {}
    for c in header:
        name = c.strip() or f"column {len(columns) + 1}"
        if name in seen:
            seen[name] += 1
            name = f"{name} ({seen[name]})"
        else:
            seen[name] = 1
        columns.append(name)
    return columns


def parse(data: bytes) -> Table:
    text = decode(data)
    n, h, delim = _layout(text)
    reader = csv.reader(io.StringIO(text, newline=""), delimiter=delim)
    preamble = [" ".join(c.strip() for c in r).strip() for r in itertools.islice(reader, h)]
    columns = _names(next(reader))
    body, footer = [], []
    for r in reader:
        if not any(c.strip() for c in r):
            continue
        r = [c.replace("\r\n", "\n") for c in (r + [""] * n)[:n]]
        (footer if _is_total(r) else body).append(r)
    return Table(columns=columns, rows=body, preamble=[p for p in preamble if p], footer=footer, delimiter=delim)


def condense(data: bytes) -> tuple[bytes, str]:
    """Shrink a big export for storage: drop rows with no activity (cost, clicks and conversions all
    zero or empty) when the table has such columns, keep the preamble and the file's
    own Total rows, add a note saying what was left out, and gzip the result (UTF-8 CSV)."""
    text = decode(data)
    n, h, delim = _layout(text)
    reader = csv.reader(io.StringIO(text, newline=""), delimiter=delim)
    preamble = [" ".join(c.strip() for c in r).strip() for r in itertools.islice(reader, h)]
    header = next(reader)
    active = [i for i, c in enumerate(header) if ACTIVITY.match(c.strip())]
    out = io.StringIO()
    w = csv.writer(out, lineterminator="\n")
    kept = dropped = 0
    rows_out: list[list[str]] = []
    for r in reader:
        if not any(c.strip() for c in r):
            continue
        r = (r + [""] * n)[:n]
        if active and not _is_total(r) and not any(number(r[i]) for i in active):
            dropped += 1
            continue
        kept += not _is_total(r)
        rows_out.append(r)
    note = (f"{CONDENSED_NOTE}: kept {kept:,} of {kept + dropped:,} rows; {dropped:,} rows with no cost, clicks or "
            f"conversions were left out (impressions in the kept rows only). The file's own Total rows still describe the full export."
            if dropped else f"{CONDENSED_NOTE}: all {kept:,} rows kept, stored compressed.")
    for p in [p for p in preamble if p] + [note]:
        w.writerow([p])
    w.writerow(header)
    w.writerows(rows_out)
    return gzip.compress(out.getvalue().encode("utf-8"), compresslevel=6), note


def number(cell: str) -> float | None:
    """'1,234.56' -> 1234.56, '₪12.30' / 'CA$12.30' / '12.30 CAD' -> 12.3, '8.57%' -> 8.57; '--' or text -> None."""
    s = cell.strip()
    if s in EMPTY or s.startswith(("<", ">")):
        return None
    neg = s.startswith("(") and s.endswith(")")
    s = _CURRENCY.sub("", s.strip("()")).rstrip("%").replace(",", "")
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
        cells = [r[i].strip() for r in rows[:5000] if r[i].strip() not in EMPTY]
        if not cells or any(x.endswith("%") for x in cells[:50]):
            continue
        if sum(number(x) is not None for x in cells) >= 0.9 * len(cells):
            out.append(i)
    return out


_WHERE = re.compile(r"^\s*(.+?)\s*(>=|<=|!=|=|>|<)\s*(-?[\d.,]+)\s*$")
_OPS = {">": float.__gt__, "<": float.__lt__, ">=": float.__ge__, "<=": float.__le__,
        "=": lambda a, b: abs(a - b) < 1e-9, "!=": lambda a, b: abs(a - b) >= 1e-9}


def _filters(table: Table, where: list[str]) -> list[tuple[int, Any, float]]:
    out = []
    for w in where:
        m = _WHERE.match(w)
        if not m:
            raise ValueError(f"cannot read the filter {w!r}; write it like 'Cost > 50' or 'Conversions = 0'")
        out.append((_column(table, m.group(1)), _OPS[m.group(2)], float(m.group(3).replace(",", ""))))
    return out


def _guide(table: Table) -> dict[str, Any]:
    title = (table.preamble[0] if table.preamble else "").strip().strip('"').lower()
    out: dict[str, Any] = {}
    if title in REPORT_GUIDE:
        out["report"] = table.preamble[0]
        out["how_to_read"] = REPORT_GUIDE[title]
    return out


def _check_against_file_totals(table: Table, sums: dict[str, float]) -> str | None:
    """Rows that add up to more (or less) than the file's own account total mean repeated levels or a
    filtered export; say so instead of letting the sum be taken as spend."""
    # Google Ads puts the total of the listed rows first ("Total: Search terms", "Total: Ad groups"),
    # then wider ones ("Total: Account").
    acct = table.footer[0] if table.footer else None
    for col in ("Cost", "Clicks", "עלות", "קליקים"):
        if col in sums and acct is not None:
            v = number(acct[table.columns.index(col)])
            if v and abs(sums[col] - v) > max(1.0, 0.01 * v):
                return (f"The rows add up to {sums[col]:,.2f} {col} but the file's own total is {v:,.2f}. "
                        "The rows repeat spend at several levels, or the export is filtered or condensed: "
                        "quote the file's Total rows for totals.")
    if "Level" in table.columns and sums:
        k = table.columns.index("Level")
        if len({r[k] for r in table.rows[:20000]}) > 1:
            return "Rows are at more than one Level: filter by one Level before adding numbers."
    return None


def query(table: Table, contains: str | None = None, sort_by: str | None = None,
          descending: bool = True, offset: int = 0, limit: int = 50,
          columns: list[str] | None = None, where: list[str] | None = None,
          group_by: str | None = None) -> dict[str, Any]:
    rows = table.rows
    if contains:
        needle = contains.lower()
        rows = [r for r in rows if any(needle in c.lower() for c in r)]
    for k, op, v in _filters(table, where or []):
        rows = [r for r in rows if (x := number(r[k])) is not None and op(x, v)]
    add = additive_columns(table, rows)
    totals = {table.columns[i]: round(sum(number(r[i]) or 0 for r in rows), 2) for i in add}
    limit = max(1, min(int(limit), MAX_LIMIT))
    offset = max(0, int(offset))
    out: dict[str, Any] = {
        **_guide(table),
        "preamble": table.preamble,
        "columns": table.columns,
        "rows_in_file": len(table.rows),
        "rows_matching": len(rows),
        "totals_of_matching_rows": totals,
        "offset": offset,
    }
    if group_by:
        g = _column(table, group_by)
        groups: dict[str, list[float]] = {}
        for r in rows:
            acc = groups.setdefault(r[g], [0.0] * (len(add) + 1))
            acc[0] += 1
            for j, i in enumerate(add, 1):
                acc[j] += number(r[i]) or 0
        names = ["rows"] + [table.columns[i] for i in add]
        want = ("rows" if sort_by.strip().lower() == "rows" else table.columns[_column(table, sort_by)]) if sort_by \
            else ("Cost" if "Cost" in names else None)
        key = names.index(want) if want in names else min(1, len(names) - 1)
        ordered = sorted(groups.items(), key=lambda kv: kv[1][key], reverse=descending)
        out["groups_total"] = len(ordered)
        out["groups"] = [{table.columns[g]: name, **{c: round(v, 2) for c, v in zip(names, acc)}}
                         for name, acc in ordered[offset:offset + limit]]
        if offset + limit < len(ordered):
            out["more"] = f"{len(ordered) - offset - limit} more groups; pass offset={offset + limit}"
    else:
        if sort_by:
            k = _column(table, sort_by)
            present = [r for r in rows if number(r[k]) is not None]
            absent = [r for r in rows if number(r[k]) is None]
            if present and len(present) >= len(absent):
                rows = sorted(present, key=lambda r: number(r[k]), reverse=descending) + absent
            else:  # a text column
                rows = sorted(rows, key=lambda r: r[k].lower(), reverse=descending)
        keep = [_column(table, c) for c in columns] if columns else list(range(len(table.columns)))
        out["rows"] = [{table.columns[i]: r[i] for i in keep} for r in rows[offset:offset + limit]]
        if offset + limit < len(rows):
            out["more"] = f"{len(rows) - offset - limit} more rows; pass offset={offset + limit}"
    if table.footer:
        out["total_rows_in_file"] = [dict(zip(table.columns, r)) for r in table.footer]
    if not contains and not where:
        warn = _check_against_file_totals(table, totals)
        if warn:
            out["warning"] = warn
    return out
