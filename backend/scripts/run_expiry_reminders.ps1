$ErrorActionPreference = 'Stop'

$backendPath = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $backendPath

$pythonPath = Join-Path $backendPath '.venv\Scripts\python.exe'
& $pythonPath manage.py send_expiry_reminders
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
