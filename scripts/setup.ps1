# AllFix setup for Windows (PowerShell). Run from the repository folder:
#   powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

function Need($cmd, $hint) {
  if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) { Write-Host "Missing: $cmd. $hint" -ForegroundColor Red; exit 1 }
}

# 1. Python 3.12+
$py = $null
if (Get-Command py -ErrorAction SilentlyContinue) { $py = "py -3" }
elseif (Get-Command python -ErrorAction SilentlyContinue) { $py = "python" }
if (-not $py -or (Invoke-Expression "$py -c `"import sys; print(sys.version_info >= (3, 12))`"") -ne "True") {
  Write-Host "Install Python 3.12 or newer: winget install Python.Python.3.12" -ForegroundColor Red; exit 1
}
Need node "Install Node.js 20 or newer: winget install OpenJS.NodeJS.LTS"

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
  Write-Host "Created .env. Open it and set ANTHROPIC_API_KEY (and DATABASE_URL if not using the default)." -ForegroundColor Yellow
}

# 5. Database: start the local Postgres container if Docker is available and .env points at localhost
$dbUrl = (Get-Content .env | Where-Object { $_ -match '^DATABASE_URL=' }) -replace '^DATABASE_URL=', ''
if ($dbUrl -match 'localhost|127\.0\.0\.1') {
  if (Get-Command docker -ErrorAction SilentlyContinue) {
    docker compose up -d db
    Start-Sleep -Seconds 5
  } else {
    Write-Host "DATABASE_URL points at this PC. Make sure Postgres is running (Docker Desktop, or: winget install PostgreSQL.PostgreSQL.17)." -ForegroundColor Yellow
  }
}

# 6. Create tables and load the knowledge base
& .\.venv\Scripts\python.exe -m allfix load-knowledge
Write-Host "Setup done. Start AllFix with: scripts\run.ps1" -ForegroundColor Green
