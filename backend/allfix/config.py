"""Settings, read from the environment (and a .env file at the repo root)."""

from functools import lru_cache
from typing import Literal
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=REPO_ROOT / ".env", env_file_encoding="utf-8", extra="ignore"
    )

    database_url: str = "postgresql://allfix@localhost:5432/allfix"

    # How the strategist reaches Claude:
    #   subscription: the Claude Agent SDK, signed in with your own Claude plan (`claude login`).
    #                 For your own single-user use only; it refuses to serve other machines.
    #   api:          the Claude API with ANTHROPIC_API_KEY (pay as you go; the deployable option).
    strategist_backend: Literal["subscription", "api"] = "subscription"
    anthropic_api_key: str | None = None
    # Optional path to a specific `claude` executable; by default the SDK's bundled one is used.
    claude_cli_path: str | None = None
    # Allow the subscription backend while serving beyond this machine (you alone, behind a password).
    allfix_single_user: bool = False

    # Strategist models. Each mode is one line so it can be changed without code.
    model_standard: str = "claude-opus-5-5"
    model_deep: str = "claude-fable-5-1"
    effort_standard: str = "high"
    effort_deep: str = "high"
    max_tool_calls_per_turn: int = 40

    knowledge_dir: Path = REPO_ROOT / "knowledge"
    frontend_dist: Path = REPO_ROOT / "frontend" / "dist"
    # Working folder for the agent process (holds no project data; transcripts go to the database).
    agent_workdir: Path = REPO_ROOT / ".allfix-agent"

    host: str = "127.0.0.1"
    port: int = 8000
    # Required when the app is reachable from outside this machine.
    allfix_password: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
