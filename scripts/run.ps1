# Start AllFix and open it in the browser.
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$port = 8000
$line = Get-Content .env -ErrorAction SilentlyContinue | Where-Object { $_ -match '^PORT=' }
if ($line) { $port = ($line -replace '^PORT=', '').Trim() }
# Open the browser once the server answers (connecting to a remote database can take a while).
Start-Job {
  foreach ($i in 1..60) {
    try { Invoke-WebRequest "http://127.0.0.1:$using:port/api/health" -UseBasicParsing -TimeoutSec 2 | Out-Null; break } catch { Start-Sleep -Seconds 1 }
  }
  Start-Process "http://127.0.0.1:$using:port"
} | Out-Null
$env:PYTHONUTF8 = "1"
& .\.venv\Scripts\python.exe -m allfix serve
