# Update AllFix from GitHub, then refresh the backend packages and rebuild the interface.
# Start AllFix.cmd runs this before every start. By hand (AllFix closed): powershell -ExecutionPolicy Bypass -File scripts\update.ps1
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

& git fetch -q origin main
if ($LASTEXITCODE -ne 0) { Write-Host "Could not reach GitHub; keeping the current version." -ForegroundColor Yellow; exit 1 }
if ((& git rev-parse HEAD) -eq (& git rev-parse origin/main)) { Write-Host "AllFix is up to date."; exit 0 }
Write-Host "Updating AllFix..." -ForegroundColor Yellow

# Files copied in by hand that already match the new version would block the update: let git take them over.
foreach ($f in (& git diff --name-only HEAD origin/main)) {
  if (-not (Test-Path -LiteralPath $f)) { continue }
  $incoming = (& git rev-parse "origin/main:$f" 2>$null)
  # Compare raw bytes and the line-ending-normalised form (Git for Windows may convert CRLF).
  if ($incoming -and (((& git hash-object --no-filters -- $f) -eq $incoming) -or ((& git hash-object -- $f) -eq $incoming))) {
    & git ls-files --error-unmatch -- $f 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) { & git checkout -- $f } else { Remove-Item -LiteralPath $f }
  }
}

& git merge --ff-only origin/main
if ($LASTEXITCODE -ne 0) {
  Write-Host "Files in this folder were changed by hand, so the update stopped. Nothing was lost; ask Claude to sort it out." -ForegroundColor Red
  # Tell the running server not to restart for this version again.
  New-Item -ItemType Directory -Force -Path logs | Out-Null
  Set-Content -Path logs\update-blocked.txt -Value (& git rev-parse origin/main)
  exit 1
}
& .\.venv\Scripts\python.exe -m pip install -e ".\backend[dev]" | Out-Null
Push-Location frontend
npm install --no-fund --no-audit
npm run build
Pop-Location
Write-Host "AllFix updated." -ForegroundColor Green
