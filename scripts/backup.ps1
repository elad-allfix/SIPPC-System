# Back up the AllFix database to backups\ (keeps the newest 30).
#   scripts\backup.ps1            run a backup now
#   scripts\backup.ps1 -Register  also schedule it every night at 02:00 (Windows Task Scheduler)
# Uses pg_dump (on PATH or in the standard PostgreSQL install folder), or Docker with the
# compose database running.
param([switch]$Register)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if ($Register) {
  $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -WorkingDirectory $Root
  $trigger = New-ScheduledTaskTrigger -Daily -At 2am
  $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable
  Register-ScheduledTask -TaskName "AllFix nightly backup" -Action $action -Trigger $trigger -Settings $settings -Force | Out-Null
  Write-Host "Scheduled: AllFix nightly backup at 02:00"
}

$dbUrl = (Get-Content .env | Where-Object { $_ -match '^DATABASE_URL=' }) -replace '^DATABASE_URL=', ''
New-Item -ItemType Directory -Force -Path backups | Out-Null
$name = "allfix-$(Get-Date -Format 'yyyyMMdd-HHmm').dump"
$file = Join-Path "backups" $name

$pgDump = (Get-Command pg_dump -ErrorAction SilentlyContinue).Source
if (-not $pgDump) {
  $pgDump = Get-ChildItem "C:\Program Files\PostgreSQL\*\bin\pg_dump.exe" -ErrorAction SilentlyContinue |
    Sort-Object FullName -Descending | Select-Object -First 1 -ExpandProperty FullName
}

# Native tools write notices to stderr; from Task Scheduler that would abort the script under
# "Stop". The exit code is checked instead.
$ErrorActionPreference = "Continue"
if ($pgDump) {
  & $pgDump --format=custom --no-owner --file=$file $dbUrl
} elseif ((Get-Command docker -ErrorAction SilentlyContinue) -and ($dbUrl -match 'localhost|127\.0\.0\.1')) {
  # Write inside the container and copy the file out: piping a binary dump through PowerShell
  # would corrupt it.
  docker compose exec -T db pg_dump -U allfix --format=custom --no-owner --file=/tmp/$name allfix
  if ($LASTEXITCODE -eq 0) { docker compose cp "db:/tmp/$name" $file }
  docker compose exec -T db rm -f /tmp/$name | Out-Null
} else {
  Write-Host "pg_dump not found. Install PostgreSQL client tools: winget install PostgreSQL.PostgreSQL.17" -ForegroundColor Red; exit 1
}
if ($LASTEXITCODE -ne 0 -or -not (Test-Path $file)) { Write-Host "Backup failed" -ForegroundColor Red; exit 1 }
$ErrorActionPreference = "Stop"
Write-Host "Backup written: $file"
Get-ChildItem backups\allfix-*.dump | Sort-Object Name -Descending | Select-Object -Skip 30 | Remove-Item
