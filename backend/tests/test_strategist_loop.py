from allfix import store
from allfix.strategist.loop import build_history, run_turn

from fakes import FakeModelClient, text, tool


async def _project():
    p = await store.create_project({"name": "Mobile pet grooming", "objective": "booked grooming jobs",
                                    "objective_type": "leads", "country": "US"})
    c = await store.create_conversation(p["id"])
    return p, c


async def _run(client, p, c, msg, mode="standard"):
    return [ev async for ev in run_turn(client, p["id"], c["id"], msg, mode)]


def _assert_valid_history(messages):
    assert messages[0]["role"] == "user"
    for i, m in enumerate(messages):
        if m["role"] == "system":
            assert messages[i - 1]["role"] == "user"
            assert i == len(messages) - 1 or messages[i + 1]["role"] == "assistant"


async def test_tool_round_trip_saves_item_and_persists_history(database):
    p, c = await _project()
    client = FakeModelClient([
        ([text("Let me check the knowledge base."),
          tool("t1", "search_knowledge", {"query": "good traffic definition"}),
          tool("t2", "save_item", {"kind": "intent_cluster", "title": "At-home dog grooming near me",
                                   "body": "Owners who want grooming without travel.", "label": "hypothesis",
                                   "confidence": "medium", "data": {"situation": "busy owner"},
                                   "sources": [{"kb": "MKT-NICHE-012"}]})], "tool_use"),
        ([text("Saved one intent cluster [hypothesis].",
               citations=[{"type": "web_search_result_location", "url": "https://example.org/a", "title": "A"}])],
         "end_turn"),
    ])
    events = await _run(client, p, c, "Research this niche")
    types = [e["type"] for e in events]
    assert types[0] == "turn_start" and types[-1] == "done"
    assert any(e["type"] == "item_saved" and e["item"]["kind"] == "intent_cluster" for e in events)
    assert any(e["type"] == "sources" and e["sources"][0]["url"] == "https://example.org/a" for e in events)

    items = await store.list_items(p["id"])
    assert len(items) == 1 and items[0]["stage"] == 3 and items[0]["conversation_id"] == c["id"]

    rows = await store.load_messages(c["id"])
    assert [r["role"] for r in rows] == ["user", "system", "assistant", "user", "assistant"]
    tool_results = rows[3]["content"]
    assert {r["tool_use_id"] for r in tool_results} == {"t1", "t2"}
    assert not any(r.get("is_error") for r in tool_results)
    for req in client.requests:
        _assert_valid_history(req["messages"])
    # The project brief reaches the model as a system message after the user's text.
    assert "Mobile pet grooming" in client.requests[0]["messages"][1]["content"][0]["text"]


async def test_second_turn_sees_saved_items_in_brief(database):
    p, c = await _project()
    await store.create_item(p["id"], {"kind": "decision", "title": "Start with two suburbs", "label": "assumption"})
    client = FakeModelClient([([text("ok")], "end_turn")])
    await _run(client, p, c, "What did we decide?")
    brief = client.requests[0]["messages"][1]["content"][0]["text"]
    assert "Start with two suburbs" in brief


async def test_tool_error_is_returned_to_model_not_raised(database):
    p, c = await _project()
    client = FakeModelClient([
        ([tool("t1", "save_item", {"kind": "nonsense", "title": "x", "body": "", "label": "hypothesis",
                                   "confidence": "low"})], "tool_use"),
        ([text("That failed; continuing.")], "end_turn"),
    ])
    events = await _run(client, p, c, "save something")
    assert any(e["type"] == "tool_end" and not e["ok"] for e in events)
    rows = await store.load_messages(c["id"])
    assert rows[3]["content"][0]["is_error"] is True


async def test_failed_request_leaves_history_usable(database):
    p, c = await _project()
    client = FakeModelClient([RuntimeError("network down")])
    events = await _run(client, p, c, "first try")
    assert events[-1]["type"] == "error"
    client2 = FakeModelClient([([text("second try works")], "end_turn")])
    await _run(client2, p, c, "second try")
    msgs = client2.requests[0]["messages"]
    _assert_valid_history(msgs)
    # The orphaned system brief from the failed turn is skipped.
    assert [m["role"] for m in msgs] == ["user", "user", "system"]


async def test_pause_turn_resumes_without_new_user_message(database):
    p, c = await _project()
    paused = [{"type": "server_tool_use", "id": "s1", "name": "web_search", "input": {"query": "mobile groomers"}}]
    client = FakeModelClient([
        (paused, "pause_turn"),
        ([{"type": "web_search_tool_result", "tool_use_id": "s1", "content": []}, text("Found nothing useful.")],
         "end_turn"),
    ])
    events = await _run(client, p, c, "search")
    assert events[-1]["type"] == "done"
    assert client.requests[1]["messages"][-1]["role"] == "assistant"


async def test_deep_mode_uses_deep_model(database):
    p, c = await _project()
    client = FakeModelClient([([text("deep answer")], "end_turn")])
    await _run(client, p, c, "think hard", mode="deep")
    assert client.requests[0]["model"] == "claude-fable-5-1"
    rows = await store.load_messages(c["id"])
    assert rows[-1]["mode"] == "deep"


async def test_refusal_is_reported_and_not_stored(database):
    p, c = await _project()
    client = FakeModelClient([([], "refusal")])
    events = await _run(client, p, c, "something")
    assert events[-1]["type"] == "error"
    assert [r["role"] for r in await store.load_messages(c["id"])] == ["user", "system"]


def test_build_history_keeps_trailing_system():
    rows = [{"role": "user", "content": [1]}, {"role": "system", "content": [2]}]
    assert [m["role"] for m in build_history(rows)] == ["user", "system"]
