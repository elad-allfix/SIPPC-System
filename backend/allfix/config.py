"""Settings, read from the environment (and a .env file at the repo root)."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=REPO_ROOT / ".env", env_file_encoding="utf-8", extra="ignore"
    )

    database_url: str = "postgresql://allfix@localhost:5432/allfix"
    anthropic_api_key: str | None = None

    # Strategist models. Each mode is one line so it can be changed without code.
    model_standard: str = "claude-opus-5-5"
    model_deep: str = "claude-fable-5-1"
    effort_standard: str = "high"
    effort_deep: str = "high"
    max_tool_calls_per_turn: int = 40

    knowledge_dir: Path = REPO_ROOT / "knowledge"
    frontend_dist: Path = REPO_ROOT / "frontend" / "dist"

    host: str = "127.0.0.1"
    port: int = 8000
    # Required when the app is reachable from outside this machine.
    allfix_password: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
