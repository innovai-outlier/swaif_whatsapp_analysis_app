# SWAIF Stack - Script Principal de Deploy
# PowerShell - Chama o script de deploy organizado

Write-Host "🚀 SWAIF Stack - Deploy Automatizado" -ForegroundColor Green
Write-Host "Executando script de deploy..." -ForegroundColor Cyan
Write-Host ""

# Chamar o script de deploy organizado
& ".\scripts\deploy\start_stack.ps1" @args
