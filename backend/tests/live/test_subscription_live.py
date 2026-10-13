import asyncio
import os
import shutil
from pathlib import Path

from allfix import db, store
from allfix.config import get_settings
from allfix.strategist.subscription import STATUS, SubscriptionStrategist


async def _project(name="Live test: mobile pet grooming"):
    p = await store.create_project({"name": name, "objective": "booked grooming jobs",
                                    "objective_type": "leads", "country": "United States", "region": "Austin, TX"})
    c = await store.create_conversation(p["id"], backend="subscription")
    return p, c


async def _turn(s, p, c, text, mode="standard"):
    return [ev async for ev in s.run_turn(p["id"], c["id"], text, mode)]


def _errors(events):
    return [e["message"] for e in events if e["type"] == "error"]


async def test_turn_uses_subscription_saves_item_and_persists(database):
    p, c = await _project()
    s = SubscriptionStrategist()
    events = await _turn(s, p, c,
        "Test of your tools, no research needed. Call save_item once: kind 'question', stage 2, title "
        "'What is the average job value?', body 'Needed for economics.', label 'unknown', confidence 'high'. "
        "Then reply with one short sentence.")
    assert not _errors(events), _errors(events)
    types = [e["type"] for e in events]
    assert types[0] == "turn_start" and types[-1] == "done"
    assert "item_saved" in types and "text" in types
    assert STATUS["auth"] == "none"            # subscription, not an API key
    items = await store.list_items(p["id"])
    assert [i["title"] for i in items] == ["What is the average job value?"]
    conv = await store.get_conversation(c["id"])
    assert conv["agent_session_id"]
    rows = await store.load_messages(c["id"])
    assert rows[0]["role"] == "user" and any(r["role"] == "assistant" for r in rows)
    n = await db.fetch_one("select count(*) as n from agent_transcripts where session_id = %s",
                           (conv["agent_session_id"],))
    assert n["n"] > 0                          # transcript mirrored to Postgres


async def test_resume_works_after_local_transcript_is_deleted(database):
    p, c = await _project()
    s = SubscriptionStrategist()
    ev1 = await _turn(s, p, c, "Remember the code word PELICAN-47. Reply only 'ok'.")
    assert not _errors(ev1), _errors(ev1)
    sid = (await store.get_conversation(c["id"]))["agent_session_id"]
    # Simulate another machine: remove the local transcript so resume must come from Postgres.
    home = Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude")) / "projects"
    for f in home.rglob(f"{sid}.jsonl"):
        f.unlink()
    ev2 = await _turn(s, p, c, "What was the code word? Reply with just the word.")
    assert not _errors(ev2), _errors(ev2)
    answer = "".join(e["text"] for e in ev2 if e["type"] == "text")
    assert "PELICAN-47" in answer


async def test_refuses_when_claude_code_would_use_an_api_key(database, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-not-a-real-key")
    p, c = await _project()
    s = SubscriptionStrategist(options_hook=lambda o: o.env.pop("ANTHROPIC_API_KEY", None))
    events = await _turn(s, p, c, "Reply 'ok'.")
    errs = _errors(events)
    assert errs and "API key" in errs[0]
    assert not await store.list_items(p["id"])


async def test_second_message_while_busy_is_rejected(database):
    p, c = await _project()
    s = SubscriptionStrategist()
    first = asyncio.create_task(_turn(s, p, c, "Reply with the word 'ok' and nothing else."))
    await asyncio.sleep(0.2)
    second = await _turn(s, p, c, "Reply 'ok'.")
    assert _errors(second) and "still working" in _errors(second)[0]
    assert not _errors(await first)


async def test_stop_interrupts_and_conversation_stays_usable(database):
    p, c = await _project()
    s = SubscriptionStrategist()
    gen = s.run_turn(p["id"], c["id"], "Write a 600-word essay about search intent.", "standard")
    async for ev in gen:
        if ev["type"] == "text":
            break
    await gen.aclose()                         # what happens when the user presses Stop
    events = await _turn(s, p, c, "Reply with the single word 'ready'.")
    assert not _errors(events), _errors(events)
    assert "ready" in "".join(e["text"] for e in events if e["type"] == "text").lower()
