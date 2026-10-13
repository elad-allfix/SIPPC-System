@echo off
rem Double-click to set up AllFix on this PC (Python, Node, database, interface).
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\setup.ps1
pause
