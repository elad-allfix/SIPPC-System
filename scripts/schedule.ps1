# Schedule AllFix's daily Google Ads account check (Windows Task Scheduler).
#   scripts\schedule.ps1            register it for 07:30 every day
#   scripts\schedule.ps1 -Remove    remove it
# The check runs inside the running AllFix server (it reuses the Stage 01 route check) and uses no
# Claude usage: it is plain comparisons. If AllFix is not running, the task does nothing.
param([switch]$Remove, [string]$At = "7:30am")
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Name = "AllFix daily account check"
if ($Remove) {
  Unregister-ScheduledTask -TaskName $Name -Confirm:$false
  Write-Host "Removed: $Name"; exit 0
}
# pythonw: no console window. Output goes to logs\check-accounts.log.
$python = Join-Path $Root ".venv\Scripts\pythonw.exe"
$action = New-ScheduledTaskAction -Execute $python -Argument "-m allfix check-accounts" -WorkingDirectory (Join-Path $Root "backend")
$trigger = New-ScheduledTaskTrigger -Daily -At $At
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 20)
Register-ScheduledTask -TaskName $Name -Action $action -Trigger $trigger -Settings $settings -Force | Out-Null
Write-Host "Scheduled: $Name at $At"
