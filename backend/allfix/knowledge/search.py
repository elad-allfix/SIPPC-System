"""Retrieval over the knowledge base (Postgres full-text search)."""

from __future__ import annotations

import re

from .. import db

_ID = re.compile(r"\b[A-Z]{2,5}-[A-Z]{2,6}-\d{3}\b")


async def search(query: str, limit: int = 8, area: str | None = None) -> dict:
    """Return the best-matching entries and documents for a query.

    Entry ids mentioned in the query are always returned first. Results are
    summaries (claim, evidence type, confidence); full text comes from read().
    """
    limit = max(1, min(limit, 20))
    exact_ids = _ID.findall(query.upper())
    entries: list[dict] = []
    if exact_ids:
        entries = await db.fetch_all(
            "select id, title, claim, evidence_type, confidence, changed, file "
            "from kb_entries where id = any(%s)",
            (exact_ids,),
        )
    text = _ID.sub(" ", query).strip()
    if text:
        # Match on any word (OR), ranked so entries matching more words come first.
        rows = await db.fetch_all(
            """with q as (
                 select to_tsquery('english', string_agg(lexeme, ' | ')) as tsq
                 from unnest(tsvector_to_array(to_tsvector('english', %(text)s))) as lexeme
               )
               select id, title, claim, evidence_type, confidence, changed, file,
                      ts_rank_cd(search, q.tsq) as rank
               from kb_entries, q
               where q.tsq is not null and search @@ q.tsq
                 and (%(area)s::text is null or area = %(area)s)
               order by rank desc, id
               limit %(limit)s""",
            {"text": text, "area": area, "limit": limit},
        )
        have = {e["id"] for e in entries}
        entries += [r for r in rows if r["id"] not in have]
        docs = await db.fetch_all(
            """with q as (
                 select to_tsquery('english', string_agg(lexeme, ' | ')) as tsq
                 from unnest(tsvector_to_array(to_tsvector('english', %(text)s))) as lexeme
               )
               select slug, title, kind, ts_rank_cd(search, q.tsq) as rank
               from kb_documents, q
               where q.tsq is not null and search @@ q.tsq and kind in ('playbook', 'relationships')
               order by rank desc limit 3""",
            {"text": text},
        )
    else:
        docs = []
    for e in entries:
        e.pop("rank", None)
    for d in docs:
        d.pop("rank", None)
    return {"entries": entries[:limit], "documents": docs}


async def read(ids: list[str]) -> list[dict]:
    """Full text of entries (by id) or documents (by slug)."""
    ids = [i.strip() for i in ids if i and i.strip()][:12]
    entries = await db.fetch_all(
        "select id, title, body, evidence_type, confidence, file from kb_entries where id = any(%s)",
        ([i.upper() for i in ids],),
    )
    docs = await db.fetch_all(
        "select slug as id, title, body, kind from kb_documents where slug = any(%s)", (ids,)
    )
    found = {r["id"] for r in entries} | {r["id"] for r in docs}
    missing = [{"id": i, "error": "not found"} for i in ids if i not in found and i.upper() not in found]
    return entries + docs + missing


async def list_documents() -> list[dict]:
    return await db.fetch_all("select slug, title, kind from kb_documents order by kind, slug")
