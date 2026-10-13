# AllFix

An AI campaign strategist for Google Ads. One central strategist you talk to, backed by an expert
knowledge base, live web research, and a project memory that keeps findings, decisions and
forecasts with their evidence labels.

The same code runs on your PC and in the cloud. Code lives in GitHub, data in Postgres (local or
Supabase, used as plain Postgres), and Google Ads account access will only ever run on the PC,
behind the PIA + Dolphin checks of Stage 01.

- Specification: [docs/SPEC.md](docs/SPEC.md)
- Roadmap and status: [docs/ROADMAP.md](docs/ROADMAP.md)

## Set up on Windows

You need Python 3.12+, Node.js 20+, and Postgres (Docker Desktop, a native install, or Supabase).

```powershell
cd "C:\Users\Itzhak\AI-Projects\SIPPC System"
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
```

Then open `.env`, set `ANTHROPIC_API_KEY`, and start it:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run.ps1
```

AllFix opens at http://127.0.0.1:8000.

### Database choices

- **Local (default):** `docker compose up -d db` starts Postgres 17 on this PC. `setup.ps1` does this
  for you when Docker is installed.
- **Supabase:** put the "Session pooler" connection string in `DATABASE_URL` (see `.env.example`).
  AllFix creates its own tables on start. No Supabase-only features are used, so you can move to any
  Postgres with `pg_dump` / `pg_restore`.

### Backups

`scripts\backup.ps1` writes a `pg_dump` file to `backups\` and keeps the newest 30.
`scripts\backup.ps1 -Register` also schedules it nightly at 02:00.

## Set up on macOS, Linux or a cloud machine

```bash
scripts/setup.sh && scripts/run.sh
```

## Commands

```
python -m allfix serve            start the app
python -m allfix migrate          create or update tables
python -m allfix load-knowledge   (re)load the knowledge/ folder into the database
```

Edit files in `knowledge/` and run `load-knowledge` (or restart) to update what the strategist knows.

## Tests

```bash
cd backend && ../.venv/bin/python -m pytest -q     # needs a Postgres database named allfix_test
```

Point the tests at another database with `ALLFIX_TEST_DATABASE_URL`. Tests never touch the real database.

## Layout

```
backend/allfix/
  api/            HTTP API and the chat stream
  strategist/     model client (replaceable), system prompt, tools, the turn loop
  knowledge/      loader and search over knowledge/
  intelligence/   analytical tools (economics today)
  migrations/     plain SQL, applied in order
  store.py        projects, facts, items, conversations, lessons
frontend/         React interface (built to frontend/dist, served by the backend)
knowledge/        the expert knowledge base (markdown, the source of truth)
scripts/          setup, run, backup
```
