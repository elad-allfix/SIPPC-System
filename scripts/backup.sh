#!/usr/bin/env bash
# Back up the AllFix database to backups/ (keeps the newest 30). Schedule with cron if wanted.
set -euo pipefail
cd "$(dirname "$0")/.."
url=$(grep -E '^DATABASE_URL=' .env | cut -d= -f2-)
mkdir -p backups
file="backups/allfix-$(date +%Y%m%d-%H%M).dump"
pg_dump --format=custom --no-owner --file="$file" "$url"
echo "Backup written: $file"
ls -1 backups/allfix-*.dump | sort -r | tail -n +31 | xargs -r rm --
