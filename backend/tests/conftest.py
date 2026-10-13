import os

TEST_DB = os.environ.get("ALLFIX_TEST_DATABASE_URL", "postgresql://allfix@localhost:5432/allfix_test")
os.environ["DATABASE_URL"] = TEST_DB
os.environ.pop("ANTHROPIC_API_KEY", None)

import psycopg  # noqa: E402
import pytest  # noqa: E402

from allfix import db  # noqa: E402
from allfix.config import get_settings  # noqa: E402
from allfix.knowledge import loader  # noqa: E402


def reset_schema() -> None:
    with psycopg.connect(TEST_DB, autocommit=True) as conn:
        conn.execute("drop schema public cascade")
        conn.execute("create schema public")


@pytest.fixture
async def database():
    reset_schema()
    await db.open_pool(TEST_DB)
    await db.migrate()
    await loader.load(get_settings().knowledge_dir)
    yield
    await db.close_pool()
