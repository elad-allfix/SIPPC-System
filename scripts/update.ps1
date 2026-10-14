# Update AllFix from GitHub, then refresh the backend packages and rebuild the interface.
# Close the AllFix window first. Run: powershell -ExecutionPolicy Bypass -File scripts\update.ps1
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

& git fetch origin main
if ($LASTEXITCODE -ne 0) { Write-Host "Could not reach GitHub. Check the internet connection and try again." -ForegroundColor Red; exit 1 }

# Files copied in by hand that already match the new version would block the update: let git take them over.
foreach ($f in (& git diff --name-only HEAD origin/main)) {
  if (-not (Test-Path -LiteralPath $f)) { continue }
  $incoming = (& git rev-parse "origin/main:$f" 2>$null)
  if ($incoming -and ((& git hash-object -- $f) -eq $incoming)) {
    & git ls-files --error-unmatch -- $f 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) { & git checkout -- $f } else { Remove-Item -LiteralPath $f }
  }
}

& git merge --ff-only origin/main
if ($LASTEXITCODE -ne 0) {
  Write-Host "Files in this folder were changed by hand, so the update stopped. Nothing was lost; ask Claude to sort it out." -ForegroundColor Red
  exit 1
}
& .\.venv\Scripts\python.exe -m pip install -e ".\backend[dev]" | Out-Null
Push-Location frontend
npm install --no-fund --no-audit
npm run build
Pop-Location
Write-Host "AllFix is up to date. Start it with 'Start AllFix.cmd' (database changes apply on start)." -ForegroundColor Green
