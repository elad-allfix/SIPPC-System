# Start AllFix (or just open it if it is already running) and keep it updated: when a newer version
# is on GitHub the server stops itself while idle, and this script updates and starts it again.
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$port = 8000
$line = Get-Content .env -ErrorAction SilentlyContinue | Where-Object { $_ -match '^PORT=' }
if ($line) { $port = ($line -replace '^PORT=', '').Trim() }
$url = "http://127.0.0.1:$port"

try { Invoke-WebRequest "$url/api/health" -UseBasicParsing -TimeoutSec 2 | Out-Null; Start-Process $url; exit 0 } catch { }

$env:PYTHONUTF8 = "1"
$env:ALLFIX_AUTO_UPDATE = "1"
$opened = $false
while ($true) {
  & powershell -NoProfile -ExecutionPolicy Bypass -File scripts\update.ps1
  if (-not $opened) {
    # Open the browser once the server answers (connecting to a remote database can take a while).
    Start-Job { foreach ($i in 1..90) { try { Invoke-WebRequest "$using:url/api/health" -UseBasicParsing -TimeoutSec 2 | Out-Null; break } catch { Start-Sleep -Seconds 1 } }; Start-Process $using:url } | Out-Null
    $opened = $true
  }
  & .\.venv\Scripts\python.exe -m allfix serve
  if ($LASTEXITCODE -ne 75) { break }
  Write-Host "Updating AllFix to the newest version..." -ForegroundColor Yellow
}
