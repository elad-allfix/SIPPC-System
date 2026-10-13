# AllFix

An AI campaign strategist for Google Ads. One central strategist you talk to, backed by an expert
knowledge base, live web research, and a project memory that keeps findings, decisions and
forecasts with their evidence labels.

The same code runs on your PC and in the cloud. Code lives in GitHub, data in Postgres (local or
Supabase, used as plain Postgres), and Google Ads account access only runs on the PC,
behind the PIA route check of Stage 01.

- Specification: [docs/SPEC.md](docs/SPEC.md)
- Roadmap and status: [docs/ROADMAP.md](docs/ROADMAP.md)
- Progress log: [docs/PROGRESS.md](docs/PROGRESS.md)

## Set up on Windows

You need Python 3.12 or 3.13, Node.js 20+, Git for Windows, Claude Code, and Postgres (Docker
Desktop, a native install, or Supabase). Get the code with git (don't copy a folder from another
machine: `node_modules` and `.env` differ per machine):

```powershell
cd "C:\Users\Itzhak\AI-Projects"
git clone https://github.com/elad-allfix/SIPPC-System "SIPPC System"
cd "SIPPC System"
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
```

If the `SIPPC System` folder already exists and is empty, run `git clone ... .` inside it instead.

Or, without typing anything: double-click **Setup AllFix.cmd** in the folder, then **Start AllFix.cmd**. If the folder was filled from a zip, setup also links it to GitHub so `git pull` brings updates.

The strategist uses your own Claude subscription through Claude Code's sign-in, so there is no API
key to set. If you have never signed in on this PC, install Claude Code and run `claude` once to log
in. Then start AllFix:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run.ps1
```

AllFix opens at http://127.0.0.1:8000. The footer of the left rail shows "Claude subscription" and
how much of the current 5-hour usage window is used.

To use the paid Claude API instead (for example on a shared server), set `STRATEGIST_BACKEND=api`
and `ANTHROPIC_API_KEY` in `.env`. The subscription backend only answers requests from this PC.

### Google Ads (read-only)

See [docs/GOOGLE_ADS_SETUP.md](docs/GOOGLE_ADS_SETUP.md). In short: PIA with the kill switch on, a
Google Cloud project with Explorer access, a Desktop OAuth client, then
`python -m allfix ads-login --country US`. Every Google request is refused unless the Stage 01 route
check passes, and only read endpoints are allowed.

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
python -m allfix ads-login --country US   sign in to Google Ads (through the PIA check)
python -m allfix check-accounts   run today's account checks in the running app
```

`scripts\schedule.ps1` schedules `check-accounts` every morning at 07:30. The check is plain
comparisons (settings and conversion actions changed since yesterday, spend and conversions against
a 28-day baseline, impression share, new costly search terms), so it uses no Claude usage. Results
appear in Stage 07, and the strategist sees them in its project state.

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
  strategist/     both backends (subscription via the Claude Agent SDK, or the API), prompt, tools
  knowledge/      loader and search over knowledge/
  intelligence/   analytical tools (economics, website audit)
  connectivity/   Stage 01: PIA route guard, guarded network transport, connection profiles
  ads/            read-only Google Ads client, GAQL allowlist, snapshot import, ads-login
  migrations/     plain SQL, applied in order
  store.py        projects, facts, items, conversations, lessons
frontend/         React interface (built to frontend/dist, served by the backend)
knowledge/        the expert knowledge base (markdown, the source of truth)
scripts/          setup, run, backup
```
