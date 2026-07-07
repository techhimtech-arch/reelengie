$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

Write-Host "Reel Engine — starting backend + frontend..."
Write-Host "Backend:  http://127.0.0.1:8765"
Write-Host "Frontend: http://127.0.0.1:5173"
Write-Host ""

$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:Root
    powershell -ExecutionPolicy Bypass -File scripts/start-backend.ps1
}

Set-Location (Join-Path $Root "frontend")
npm run dev

Stop-Job $backendJob -ErrorAction SilentlyContinue
Remove-Job $backendJob -ErrorAction SilentlyContinue
