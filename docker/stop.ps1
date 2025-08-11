# SWAIF Stack - Script Principal de Parada
# PowerShell - Chama o script de parada organizado

Write-Host "🛑 SWAIF Stack - Shutdown" -ForegroundColor Red
Write-Host "Parando todos os servicos..." -ForegroundColor Yellow
Write-Host ""

# Chamar o script de parada organizado
& ".\scripts\deploy\stop_stack.ps1" @args
