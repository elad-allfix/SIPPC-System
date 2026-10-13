"""The strategist: one central AI that reasons, researches and keeps the project's memory.

Two interchangeable backends produce the same stream of UI events:
- SubscriptionStrategist: the Claude Agent SDK on the user's own Claude plan (local default).
- ApiStrategist: the Claude API with an API key, using AllFix's own tool loop.
"""

from __future__ import annotations

from typing import AsyncIterator, Callable, Protocol


class Strategist(Protocol):
    backend: str

    def run_turn(self, project_id: str, conversation_id: str, user_text: str,
                 mode: str = "standard") -> AsyncIterator[dict]: ...


class ApiStrategist:
    backend = "api"

    def __init__(self, client_factory: Callable | None = None):
        from .models import AnthropicModelClient
        self.client_factory = client_factory or AnthropicModelClient

    async def run_turn(self, project_id, conversation_id, user_text, mode="standard"):
        from .loop import run_turn
        try:
            client = self.client_factory()
        except Exception as e:  # e.g. no API key configured
            yield {"type": "error", "message": f"The API backend is not configured: {str(e)[:200]}. "
                                               "Set ANTHROPIC_API_KEY."}
            return
        async for ev in run_turn(client, project_id, conversation_id, user_text, mode):
            yield ev


def make_strategist(backend: str | None = None) -> Strategist:
    from ..config import get_settings
    backend = backend or get_settings().strategist_backend
    if backend == "api":
        return ApiStrategist()
    from .subscription import SubscriptionStrategist
    s = SubscriptionStrategist()
    s.backend = "subscription"
    return s
