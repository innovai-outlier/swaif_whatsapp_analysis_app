# SWAIF Stack - Acesso Rapido aos Servicos Web
# PowerShell - Chama o web launcher organizado

Write-Host "🌐 SWAIF Stack - Acesso Web" -ForegroundColor Blue
Write-Host "Abrindo menu de servicos..." -ForegroundColor Cyan
Write-Host ""

# Chamar o script web organizado
& ".\scripts\web\web_launcher.ps1" @args
