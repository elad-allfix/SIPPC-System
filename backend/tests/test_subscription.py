"""Offline tests for the subscription backend's plumbing (no model calls)."""
import asyncio

from allfix import store
from allfix.config import get_settings
from allfix.strategist import subscription as sub
from allfix.strategist.models import spec_for
from allfix.strategist.tools import ToolContext


def test_display_names():
    assert sub.display_name("mcp__allfix__save_item") == "save_item"
    assert sub.display_name("WebSearch") == "web_search" and sub.display_name("WebFetch") == "web_fetch"


def test_guard_refuses_non_local_host(monkeypatch):
    s = get_settings()
    monkeypatch.setattr(s, "host", "0.0.0.0")
    monkeypatch.setattr(s, "allfix_single_user", False)
    assert "only serves this computer" in sub.guard_error()
    monkeypatch.setattr(s, "allfix_single_user", True)
    assert sub.guard_error() is None
    monkeypatch.setattr(s, "host", "127.0.0.1")
    monkeypatch.setattr(s, "allfix_single_user", False)
    assert sub.guard_error() is None


async def test_options_isolate_tools_and_blank_the_api_key():
    turn = sub._Turn(main=asyncio.get_running_loop(), queue=asyncio.Queue())
    opts = sub.build_options(sub.SubscriptionStrategist(), turn, ToolContext("p", "c"), spec_for("deep"), None)
    assert opts.tools == ["WebSearch", "WebFetch"]
    assert "mcp__allfix__save_item" in opts.allowed_tools and "Bash" not in opts.allowed_tools
    assert opts.strict_mcp_config and opts.setting_sources == [] and opts.permission_mode == "dontAsk"
    assert opts.env["ANTHROPIC_API_KEY"] == "" and opts.model == "claude-fable-5-1"


async def test_budget_stops_research_early_but_lets_saving_through(monkeypatch):
    monkeypatch.setattr(get_settings(), "max_tool_calls_per_turn", 10)
    turn = sub._Turn(main=asyncio.get_running_loop(), queue=asyncio.Queue())
    opts = sub.build_options(sub.SubscriptionStrategist(), turn, ToolContext("p", "c"), spec_for("standard"), None)
    hook = opts.hooks["PreToolUse"][0].hooks[0]
    decisions = []
    for _ in range(6):
        decisions.append(await hook({"tool_name": "WebSearch"}, None, None))
    assert all(d == {} for d in decisions[:5]) and decisions[5]["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert await hook({"tool_name": "mcp__allfix__save_item"}, None, None) == {}


def test_prompt_puts_brief_first_and_recap_when_given():
    p = sub._compose_prompt("BRIEF", "hello", "")
    assert p.startswith("<project_brief>\nBRIEF") and p.endswith("hello") and "earlier_conversation" not in p
    assert "earlier_conversation" in sub._compose_prompt("B", "x", "User: hi")


async def test_pg_session_store_round_trip(database):
    st = sub.PgSessionStore(lambda coro: coro)
    key = {"project_key": "k", "session_id": "s1"}
    await st.append(key, [{"type": "user", "uuid": "u1", "message": {"x": 1}}, {"type": "title", "t": "a"}])
    await st.append(key, [{"type": "user", "uuid": "u1", "message": {"x": 1}}])   # duplicate uuid ignored
    assert [e["type"] for e in await st.load(key)] == ["user", "title"]
    assert await st.load({"project_key": "k", "session_id": "missing"}) is None


async def test_history_seed_is_plain_text(database):
    p = await store.create_project({"name": "x"})
    c = await store.create_conversation(p["id"], backend="subscription")
    await store.append_message(c["id"], "user", [{"type": "text", "text": "What CPC?"}])
    await store.append_message(c["id"], "assistant", [{"type": "text", "text": "About $3 [estimate]."}])
    seed = await sub.history_seed(c["id"])
    assert seed == "User: What CPC?\n\nStrategist: About $3 [estimate]."
