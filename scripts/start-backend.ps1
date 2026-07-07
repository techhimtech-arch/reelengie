$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Backend = Join-Path $Root "backend"
$VenvPython = Join-Path $Backend ".venv\Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Error "Backend venv not found. Run: cd backend; python -m venv .venv; pip install -r requirements.txt"
}

Set-Location $Backend
& $VenvPython -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8765
