from allfix import db
from allfix.knowledge import search


async def test_all_entries_loaded(database):
    n = await db.fetch_one("select count(*) as n from kb_entries")
    assert n["n"] == 394
    docs = {d["slug"] for d in await search.list_documents()}
    assert {"playbooks/diagnostic", "playbooks/strategic", "relationships/metric-relationships"} <= docs


async def test_every_entry_has_evidence_and_confidence(database):
    rows = await db.fetch_all("select id from kb_entries where evidence_type is null or confidence is null or claim = ''")
    assert rows == []


async def test_search_finds_quality_score_entry(database):
    r = await search.search("is quality score used in the auction", 5)
    assert "PLT-AUC-009" in [e["id"] for e in r["entries"]]


async def test_search_by_id_comes_first(database):
    r = await search.search("PLT-BID-007 budget", 5)
    assert r["entries"][0]["id"] == "PLT-BID-007"


async def test_read_entry_and_document(database):
    rows = await search.read(["PLT-AUC-009", "playbooks/diagnostic", "NOPE-XX-001"])
    ids = [r["id"] for r in rows]
    assert "PLT-AUC-009" in ids and "playbooks/diagnostic" in ids
    assert any(r.get("error") == "not found" for r in rows)


async def test_loading_twice_is_idempotent(database):
    from allfix.config import get_settings
    from allfix.knowledge import loader
    await loader.load(get_settings().knowledge_dir)
    n = await db.fetch_one("select count(*) as n from kb_entries")
    assert n["n"] == 394
