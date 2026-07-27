# AprendeYa — Asistente Documental
# Uso: powershell -ExecutionPolicy Bypass -File scripts/run.ps1

param(
    [ValidateSet("api", "chat", "ask", "ingest", "search")]
    [string]$Mode = "chat"
)

$Root = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
Set-Location $Root

function Start-API {
    Write-Host "=== Iniciando API en http://localhost:8000 ===" -ForegroundColor Green
    Write-Host "Health: http://localhost:8000/health" -ForegroundColor Cyan
    python scripts/api.py
}

function Start-Chat {
    Write-Host "=== Iniciando servidor con chat web ===" -ForegroundColor Green
    $apiJob = Start-Job -ScriptBlock { python scripts/api.py }
    Start-Sleep -Seconds 10
    $url = "http://localhost:8000/chat.html"
    Write-Host "API activa en http://localhost:8000" -ForegroundColor Cyan
    Write-Host "Chat web en: file://$((Get-Item scripts/chat.html).FullName)" -ForegroundColor Cyan
    Write-Host "O sirve con Live Server o similar." -ForegroundColor Yellow
    Write-Host "Presiona Ctrl+C para detener." -ForegroundColor Yellow
    Wait-Job $apiJob
}

function Ask-Question {
    param([string]$Question)
    python -c "import sys; sys.path.insert(0, 'scripts'); from pipeline.agent import Agent; import json; a=Agent(); r=a.ask('$Question'); print(r['respuesta'])"
}

switch ($Mode) {
    "api" { Start-API }
    "chat" { Start-Chat }
    "ingest" { python scripts/ingest.py }
    "search" {
        $q = Read-Host "Pregunta"
        python scripts/search.py $q
    }
    "ask" { Ask-Question -Question $args[0] }
    default { Start-Chat }
}
