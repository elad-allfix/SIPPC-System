"""Load the markdown knowledge base into Postgres.

Entry files (platform/, practice/, measurement/, market/) hold numbered entries:

    ### PLT-AUC-009 · The 1-10 Quality Score is not used in the auction
    - **Claim:** ...
    - **Evidence type:** documented
    - **Confidence:** high
    ...

Everything else (playbooks, the relationship map, the demo, readiness notes)
is loaded whole as a document. Loading is idempotent: rows that no longer
exist in the files are removed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .. import db

ENTRY_DIRS = ("platform", "practice", "measurement", "market")
DOCUMENT_GLOBS = {
    "playbook": "playbooks/*.md",
    "relationships": "relationships/*.md",
    "demo": "demo/*.md",
    "eval": "evals/*.md",
    "reference": "*.md",
}

_ENTRY_HEAD = re.compile(r"^### ([A-Z]{2,5}-[A-Z]{2,6}-\d{3}) · (.+)$", re.M)
_FIELD = r"^- \*\*{name}:\*\*\s*(.+)$"


@dataclass
class Entry:
    id: str
    file: str
    area: str
    title: str
    claim: str
    body: str
    evidence_type: str | None
    confidence: str | None
    changed: bool


@dataclass
class Document:
    slug: str
    title: str
    kind: str
    body: str


def _field(block: str, name: str) -> str | None:
    m = re.search(_FIELD.format(name=re.escape(name)), block, re.M)
    return m.group(1).strip() if m else None


def parse_entries(path: Path, root: Path) -> list[Entry]:
    text = path.read_text(encoding="utf-8")
    heads = list(_ENTRY_HEAD.finditer(text))
    entries: list[Entry] = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        block = text[m.start():end]
        # Stop at the file's closing sections ("## Common mistakes ...").
        block = re.split(r"^## ", block, maxsplit=1, flags=re.M)[0].strip()
        evidence = _field(block, "Evidence type")
        confidence = _field(block, "Confidence")
        entries.append(
            Entry(
                id=m.group(1),
                file=str(path.relative_to(root)).replace("\\", "/"),
                area=path.parent.name,
                title=m.group(2).strip(),
                claim=_field(block, "Claim") or "",
                body=block,
                evidence_type=evidence.split()[0].strip(",;") if evidence else None,
                confidence=confidence.split()[0].strip(",;") if confidence else None,
                changed=bool(re.search(r"\(changed \d{4}", block)),
            )
        )
    return entries


def _title_of(text: str, fallback: str) -> str:
    m = re.search(r"^# (.+)$", text, re.M)
    return m.group(1).strip() if m else fallback


def collect(root: Path) -> tuple[list[Entry], list[Document]]:
    entries: list[Entry] = []
    for d in ENTRY_DIRS:
        for path in sorted((root / d).glob("*.md")):
            entries.extend(parse_entries(path, root))
    documents: list[Document] = []
    seen: set[str] = set()
    for kind, pattern in DOCUMENT_GLOBS.items():
        for path in sorted(root.glob(pattern)):
            slug = str(path.relative_to(root).with_suffix("")).replace("\\", "/")
            if slug in seen:
                continue
            seen.add(slug)
            text = path.read_text(encoding="utf-8")
            documents.append(Document(slug=slug, title=_title_of(text, slug), kind=kind, body=text))
    return entries, documents


async def load(root: Path) -> dict[str, int]:
    entries, documents = collect(root)
    ids = [e.id for e in entries]
    if len(ids) != len(set(ids)):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        raise ValueError(f"duplicate knowledge entry ids: {dupes}")
    async with db.pool().connection() as conn:
        async with conn.transaction():
            for e in entries:
                await conn.execute(
                    """insert into kb_entries
                         (id, file, area, title, claim, body, evidence_type, confidence, changed)
                       values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                       on conflict (id) do update set
                         file = excluded.file, area = excluded.area, title = excluded.title,
                         claim = excluded.claim, body = excluded.body,
                         evidence_type = excluded.evidence_type,
                         confidence = excluded.confidence, changed = excluded.changed""",
                    (e.id, e.file, e.area, e.title, e.claim, e.body,
                     e.evidence_type, e.confidence, e.changed),
                )
            await conn.execute("delete from kb_entries where not (id = any(%s))", (ids,))
            slugs = [d.slug for d in documents]
            for d in documents:
                await conn.execute(
                    """insert into kb_documents (slug, title, kind, body) values (%s, %s, %s, %s)
                       on conflict (slug) do update set
                         title = excluded.title, kind = excluded.kind, body = excluded.body""",
                    (d.slug, d.title, d.kind, d.body),
                )
            await conn.execute("delete from kb_documents where not (slug = any(%s))", (slugs,))
    return {"entries": len(entries), "documents": len(documents)}
