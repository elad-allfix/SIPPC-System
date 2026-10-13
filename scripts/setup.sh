#!/usr/bin/env bash
# AllFix setup for macOS/Linux and cloud machines.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m venv .venv
.venv/bin/pip install -q --upgrade pip
.venv/bin/pip install -q -e "./backend[dev]"
(cd frontend && npm install --no-fund --no-audit && npm run build)
[ -f .env ] || { cp .env.example .env; echo "Created .env: set ANTHROPIC_API_KEY and DATABASE_URL."; }
if grep -qE '^DATABASE_URL=.*(localhost|127\.0\.0\.1)' .env && command -v docker >/dev/null; then
  docker compose up -d db && sleep 5 || echo "Could not start the Docker database; make sure Postgres is running."
fi
.venv/bin/python -m allfix load-knowledge
echo "Setup done. Start with: scripts/run.sh"
