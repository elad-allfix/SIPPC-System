@echo off
rem Double-click to update AllFix from GitHub. Close AllFix first.
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\update.ps1
pause
