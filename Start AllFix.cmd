@echo off
rem Double-click to start AllFix; it opens at http://127.0.0.1:8000
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run.ps1
pause
