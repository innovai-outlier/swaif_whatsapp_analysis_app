# SWAIF Stack - Script Principal de Monitoramento
# PowerShell - Chama o monitor web organizado

Write-Host "📊 SWAIF Stack - Monitor Dashboard" -ForegroundColor Cyan
Write-Host "Iniciando monitoramento..." -ForegroundColor Yellow
Write-Host ""

# Chamar o script de monitoramento organizado
& ".\scripts\monitor\monitor_web.ps1" @args
