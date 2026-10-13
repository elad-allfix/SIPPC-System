"""Display turns built from stored messages: short narration before a tool call is not the answer."""
from allfix.api.routes import render_messages


def _row(role, content):
    return {"role": role, "content": content, "created_at": "2026-10-13T00:00:00Z", "model": None, "mode": None}


def test_short_text_before_a_tool_becomes_a_note():
    answer = "Run both channels. " + "Reasoning. " * 60
    rows = [
        _row("user", [{"type": "text", "text": "Plan month 1"}]),
        _row("assistant", [{"type": "text", "text": "Economics done. Now saving the plan."},
                           {"type": "tool_use", "id": "t1", "name": "save_item", "input": {"title": "Plan"}}]),
        _row("user", [{"type": "tool_result", "tool_use_id": "t1", "content": "ok"}]),
        _row("assistant", [{"type": "text", "text": answer}]),
    ]
    turn = render_messages(rows)[1]
    assert turn["text"] == answer
    assert [a["name"] for a in turn["activity"]] == ["note", "save_item"]
    assert turn["activity"][0]["summary"] == "Economics done. Now saving the plan."


def test_long_text_before_a_tool_stays_in_the_answer():
    long = "Full answer. " * 50
    rows = [
        _row("user", [{"type": "text", "text": "Plan"}]),
        _row("assistant", [{"type": "text", "text": long},
                           {"type": "tool_use", "id": "t1", "name": "save_item", "input": {}}]),
        _row("assistant", [{"type": "text", "text": "Saved."}]),
    ]
    turn = render_messages(rows)[1]
    assert turn["text"].startswith("Full answer.") and turn["text"].endswith("Saved.")
    assert [a["name"] for a in turn["activity"]] == ["save_item"]
