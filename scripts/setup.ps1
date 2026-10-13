# AllFix setup for Windows (PowerShell). Run from the repository folder:
#   powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

function Need($cmd, $hint) {
  if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) { Write-Host "Missing: $cmd. $hint" -ForegroundColor Red; exit 1 }
}

# 1. Python 3.12+ (prefer 3.13 or 3.12 through the py launcher: every dependency has wheels for them)
$py = $null
if (Get-Command py -ErrorAction SilentlyContinue) {
  foreach ($v in "3.13", "3.12") {
    $ok = $false
    try { & py "-$v" -c "" 2>$null; $ok = ($LASTEXITCODE -eq 0) } catch { $ok = $false }
    if ($ok) { $py = "py -$v"; break }
  }
  if (-not $py) { $py = "py -3" }
}
elseif (Get-Command python -ErrorAction SilentlyContinue) { $py = "python" }
if (-not $py -or (Invoke-Expression "$py -c `"import sys; print(sys.version_info >= (3, 12))`"") -ne "True") {
  Write-Host "Install Python 3.12 or newer: winget install Python.Python.3.12" -ForegroundColor Red; exit 1
}
Need node "Install Node.js 20 or newer: winget install OpenJS.NodeJS.LTS"
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  Write-Host "Git for Windows is not installed. Claude Code needs it on Windows: winget install Git.Git" -ForegroundColor Yellow
}

# 2. Python environment and backend
if (-not (Test-Path ".venv")) { Invoke-Expression "$py -m venv .venv" }
& .\.venv\Scripts\python.exe -m pip install --upgrade pip | Out-Null
& .\.venv\Scripts\python.exe -m pip install -e ".\backend[dev]"

# 3. Interface
Push-Location frontend
npm install --no-fund --no-audit
npm run build
Pop-Location

# 4. Settings
if (-not (Test-Path ".env")) {
  Copy-Item .env.example .env
  Write-Host "Created .env. The defaults use your Claude subscription and a local database; change DATABASE_URL for Supabase." -ForegroundColor Yellow
}

# 4b. Claude sign-in: the strategist uses your own Claude plan through Claude Code's login
if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
  Write-Host "Claude Code is not installed. Install it (https://code.claude.com) and run 'claude' once to sign in with your Claude account." -ForegroundColor Yellow
} else {
  Write-Host "Claude Code found. If you have not signed in on this PC yet, run 'claude' once and log in." -ForegroundColor Green
}

# 5. Database: start the local Postgres container if Docker is available and .env points at localhost
$dbUrl = (Get-Content .env | Where-Object { $_ -match '^DATABASE_URL=' }) -replace '^DATABASE_URL=', ''
if ($dbUrl -match 'localhost|127\.0\.0\.1') {
  if (Get-Command docker -ErrorAction SilentlyContinue) {
    docker compose up -d db
    Start-Sleep -Seconds 5
  } else {
    $psql = Get-ChildItem "C:\Program Files\PostgreSQL\*\bin\psql.exe" -ErrorAction SilentlyContinue |
      Sort-Object FullName -Descending | Select-Object -First 1 -ExpandProperty FullName
    if ($psql) {
      # A native PostgreSQL install only has the "postgres" user. Create AllFix's user and database
      # (it asks for the postgres password chosen during install; "already exists" is fine).
      Write-Host "Creating the allfix database in your PostgreSQL. Enter the postgres password if asked." -ForegroundColor Yellow
      $ErrorActionPreference = "Continue"
      & $psql -U postgres -h localhost -c "create user allfix password 'allfix'"
      & $psql -U postgres -h localhost -c "create database allfix owner allfix"
      $ErrorActionPreference = "Stop"
    } else {
      Write-Host "DATABASE_URL points at this PC but no Postgres was found. Install Docker Desktop, or: winget install PostgreSQL.PostgreSQL.17, then run setup again." -ForegroundColor Yellow
    }
  }
}

# 6. Create tables and load the knowledge base
& .\.venv\Scripts\python.exe -m allfix load-knowledge
Write-Host "Setup done. Start AllFix with: scripts\run.ps1" -ForegroundColor Green
