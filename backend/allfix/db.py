"""Database access: a psycopg connection pool and a small SQL migration runner.

The schema lives in numbered .sql files under migrations/, so any Postgres
(local, Docker or Supabase) can be rebuilt from the repository.
"""

from __future__ import annotations

from importlib import resources

from psycopg.rows import dict_row
from psycopg.conninfo import conninfo_to_dict
from psycopg_pool import AsyncConnectionPool, PoolTimeout

from .config import get_settings

_pool: AsyncConnectionPool | None = None


async def open_pool(dsn: str | None = None) -> AsyncConnectionPool:
    global _pool
    if _pool is None:
        _pool = AsyncConnectionPool(
            dsn or get_settings().database_url,
            min_size=1,
            max_size=10,
            # prepare_threshold=None: no server-side prepared statements, so the same code
            # works through connection poolers (e.g. Supabase's transaction pooler).
            kwargs={"row_factory": dict_row, "autocommit": True, "prepare_threshold": None},
            open=False,
        )
        try:
            # Waits (retrying) while the database starts, e.g. Docker right after boot.
            await _pool.open(wait=True, timeout=60)
        except PoolTimeout as e:
            pool, _pool = _pool, None
            await pool.close()
            host = conninfo_to_dict(dsn or get_settings().database_url).get("host", "?")
            raise RuntimeError(f"Could not connect to the database at {host} within 60 seconds. Is Postgres "
                               "running, and is DATABASE_URL in .env right?") from e
    return _pool


async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


def pool() -> AsyncConnectionPool:
    if _pool is None:
        raise RuntimeError("database pool is not open")
    return _pool


async def fetch_all(sql: str, params: tuple | dict | None = None) -> list[dict]:
    async with pool().connection() as conn:
        cur = await conn.execute(sql, params)
        return await cur.fetchall()


async def fetch_one(sql: str, params: tuple | dict | None = None) -> dict | None:
    async with pool().connection() as conn:
        cur = await conn.execute(sql, params)
        return await cur.fetchone()


async def execute(sql: str, params: tuple | dict | None = None) -> None:
    async with pool().connection() as conn:
        await conn.execute(sql, params)


def _migration_files() -> list[tuple[str, str]]:
    folder = resources.files("allfix") / "migrations"
    files = sorted(p for p in folder.iterdir() if p.name.endswith(".sql"))
    return [(p.name, p.read_text(encoding="utf-8")) for p in files]


async def migrate() -> list[str]:
    """Apply any migrations not yet recorded. Returns the names applied."""
    applied: list[str] = []
    async with pool().connection() as conn:
        await conn.execute(
            "create table if not exists schema_migrations ("
            " name text primary key, applied_at timestamptz not null default now())"
        )
        cur = await conn.execute("select name from schema_migrations")
        done = {r["name"] for r in await cur.fetchall()}
        for name, sql in _migration_files():
            if name in done:
                continue
            async with conn.transaction():
                await conn.execute(sql)
                await conn.execute("insert into schema_migrations (name) values (%s)", (name,))
            applied.append(name)
    return applied
