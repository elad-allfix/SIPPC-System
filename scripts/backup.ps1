# Back up the AllFix database to backups\ (keeps the newest 30).
#   scripts\backup.ps1            run a backup now
#   scripts\backup.ps1 -Register  also schedule it every night at 02:00 (Windows Task Scheduler)
# Needs pg_dump on PATH (installed with PostgreSQL), or Docker with the compose database running.
param([switch]$Register)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if ($Register) {
  $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$PSCommandPath`"" -WorkingDirectory $Root
  $trigger = New-ScheduledTaskTrigger -Daily -At 2am
  Register-ScheduledTask -TaskName "AllFix nightly backup" -Action $action -Trigger $trigger -Force | Out-Null
  Write-Host "Scheduled: AllFix nightly backup at 02:00"
}

$dbUrl = (Get-Content .env | Where-Object { $_ -match '^DATABASE_URL=' }) -replace '^DATABASE_URL=', ''
New-Item -ItemType Directory -Force -Path backups | Out-Null
$file = "backups\allfix-$(Get-Date -Format 'yyyyMMdd-HHmm').dump"

if (Get-Command pg_dump -ErrorAction SilentlyContinue) {
  pg_dump --format=custom --no-owner --file=$file $dbUrl
} elseif ((Get-Command docker -ErrorAction SilentlyContinue) -and ($dbUrl -match 'localhost|127\.0\.0\.1')) {
  docker compose exec -T db pg_dump -U allfix --format=custom --no-owner allfix > $file
} else {
  Write-Host "pg_dump not found. Install PostgreSQL client tools: winget install PostgreSQL.PostgreSQL.17" -ForegroundColor Red; exit 1
}
if ($LASTEXITCODE -ne 0) { Write-Host "Backup failed" -ForegroundColor Red; exit 1 }
Write-Host "Backup written: $file"
Get-ChildItem backups\allfix-*.dump | Sort-Object Name -Descending | Select-Object -Skip 30 | Remove-Item
