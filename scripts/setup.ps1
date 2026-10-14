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
else {
  # A folder filled from a zip next to an empty git repository: link it to GitHub so 'git pull'
  # brings updates. Only when the repository has no commits yet, so local work is never touched.
  $ErrorActionPreference = "Continue"
  & git rev-parse --verify HEAD 2>$null | Out-Null
  $noCommits = ($LASTEXITCODE -ne 0)
  $origin = (& git remote get-url origin 2>$null)
  if ((Test-Path ".git") -and $noCommits -and $origin) {
    Write-Host "Linking this folder to $origin ..." -ForegroundColor Yellow
    # A bare "git remote add" can leave no fetch refspec, so name the target ref explicitly.
    & git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
    & git fetch origin "+refs/heads/main:refs/remotes/origin/main"
    if ($LASTEXITCODE -eq 0) {
      & git reset --hard origin/main
      & git branch -M main
      & git branch -u origin/main
    }
    else { Write-Host "Could not reach GitHub; continuing with the files already here." -ForegroundColor Yellow }
  }
  $ErrorActionPreference = "Stop"
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

# 4b. Claude sign-in: the strategist uses your own Claude plan through Claude Code's login.
# The Agent SDK ships its own Claude Code; use it when Claude Code is not installed separately.
$claude = (Get-Command claude -ErrorAction SilentlyContinue).Source
if (-not $claude) {
  $claude = & .\.venv\Scripts\python.exe -c "import claude_agent_sdk, os; p = os.path.join(os.path.dirname(claude_agent_sdk.__file__), '_bundled', 'claude.exe'); print(p if os.path.exists(p) else '')"
}
if ($claude) {
  $ErrorActionPreference = "Continue"
  $status = (& $claude auth status --json 2>$null) -join "`n"
  if ($status -match '"loggedIn":\s*true') {
    Write-Host "Claude sign-in found." -ForegroundColor Green
  } else {
    Write-Host "Sign in with your own Claude account. A browser window opens; come back here when it says you are signed in." -ForegroundColor Yellow
    & $claude auth login --claudeai
  }
  $ErrorActionPreference = "Stop"
} else {
  Write-Host "Claude Code was not found. Install it (https://code.claude.com) and run 'claude' once to sign in." -ForegroundColor Yellow
}

# Offer the Supabase database instead of a local one. The string is typed here and saved only in .env.
function Use-Supabase {
  Write-Host "To use Supabase, paste its connection string (Supabase > Connect > Session pooler, with your"
  Write-Host "database password in place of [YOUR-PASSWORD]). Nothing shows while you paste. Press Enter to skip." -ForegroundColor Yellow
  $sec = Read-Host -AsSecureString "Connection string"
  $url = [Runtime.InteropServices.Marshal]::PtrToStringBSTR([Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)).Trim()
  if ($url -match 'YOUR-PASSWORD') {
    Write-Host "The string still contains [YOUR-PASSWORD]. Run setup again and put your database password there." -ForegroundColor Red; exit 1
  }
  if ($url) {
    if ($url -notmatch 'sslmode=') { $url += $(if ($url -match '\?') { '&' } else { '?' }) + 'sslmode=require' }
    $lines = Get-Content .env | ForEach-Object { if ($_ -match '^DATABASE_URL=') { "DATABASE_URL=$url" } else { $_ } }
    [IO.File]::WriteAllLines((Join-Path $Root ".env"), [string[]]$lines)  # UTF-8 without BOM
    Write-Host "Saved the Supabase connection in .env." -ForegroundColor Green
  } else {
    Write-Host "Skipped. Install Docker Desktop or PostgreSQL 17 (winget install PostgreSQL.PostgreSQL.17), or rerun setup with a Supabase string." -ForegroundColor Yellow
  }
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
      $out = (& $psql -U postgres -h localhost -c "create user allfix password 'allfix'" 2>&1) -join "`n"
      Write-Host $out
      if ($out -match 'FATAL|could not connect') {
        Write-Host "Could not sign in to your local PostgreSQL." -ForegroundColor Yellow
        $ErrorActionPreference = "Stop"
        Use-Supabase
      } else {
        & $psql -U postgres -h localhost -c "create database allfix owner allfix"
        $ErrorActionPreference = "Stop"
      }
    } else {
      Use-Supabase
    }
  }
}

# 6. Create tables and load the knowledge base
& .\.venv\Scripts\python.exe -m allfix load-knowledge
if ($LASTEXITCODE -ne 0) {
  Write-Host "Could not reach the database in .env (DATABASE_URL). Fix it and run setup again." -ForegroundColor Red; exit 1
}
Write-Host "Setup done. Start AllFix by double-clicking 'Start AllFix.cmd'." -ForegroundColor Green
