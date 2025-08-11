# SWAIF Stack - Gerenciador Principal
# PowerShell - Interface unificada para todos os scripts

param(
    [ValidateSet("deploy", "monitor", "web", "stop", "status", "menu")]
    [string]$Action = "menu"
)

# Configuracao UTF-8 para evitar caracteres estranhos
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['Out-File:Encoding'] = 'UTF8'

function Show-Header {
    Clear-Host
    Write-Host ""
    Write-Host "===============================================================================" -ForegroundColor Cyan
    Write-Host "                        SWAIF STACK - DOCKER MANAGER                          " -ForegroundColor Cyan
    Write-Host "                          WhatsApp Bundle Coordenado                          " -ForegroundColor White
    Write-Host "===============================================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Show-ProjectStructure {
    Write-Host "ESTRUTURA DO PROJETO:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "docker_coordinated/" -ForegroundColor White
    Write-Host "  main.ps1              # Script principal (este arquivo)" -ForegroundColor Magenta
    Write-Host "  deploy.ps1            # Script de deploy" -ForegroundColor Green
    Write-Host "  monitor.ps1           # Script de monitoramento" -ForegroundColor Cyan
    Write-Host "  web.ps1               # Script de acesso web" -ForegroundColor Blue
    Write-Host "  stop.ps1              # Script de parada" -ForegroundColor Red
    Write-Host "  docs/                 # Documentacao" -ForegroundColor Gray
    Write-Host "  scripts/              # Scripts organizados" -ForegroundColor Gray
    Write-Host "  services/             # Servicos Docker" -ForegroundColor Gray
    Write-Host "|- logs/                 # Logs de execucao" -ForegroundColor Gray
    Write-Host ""
}

function Show-MainMenu {
    Write-Host "ACOES DISPONIVEIS:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  [1] Deploy Stack        # Subir todos os containers" -ForegroundColor Green
    Write-Host "  [2] Monitor Dashboard   # Monitoramento em tempo real" -ForegroundColor Cyan
    Write-Host "  [3] Acesso Web          # Abrir servicos no browser" -ForegroundColor Blue
    Write-Host "  [4] Status Rapido       # Verificacao pontual" -ForegroundColor White
    Write-Host "  [5] Parar Stack         # Desligar todos os containers" -ForegroundColor Red
    Write-Host "  [6] Estrutura Projeto   # Mostrar organizacao de pastas" -ForegroundColor Yellow
    Write-Host "  [0] Sair" -ForegroundColor Gray
    Write-Host ""
}

function Show-QuickStatus {
    Clear-Host
    Show-Header
    Write-Host "STATUS RAPIDO DA STACK" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "Containers Docker Ativos:" -ForegroundColor Cyan
    try {
        $containers = docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>$null
        if ($containers -and $containers.Count -gt 0) {
            # Quebrar em linhas e exibir formatado
            $lines = $containers -split "`r?`n" | Where-Object { $_.Trim() -ne "" }
            foreach ($line in $lines) {
                Write-Host "  $line" -ForegroundColor Green
            }
            Write-Host ""
        } else {
            Write-Host "  >> Nenhum container rodando" -ForegroundColor Red
            Write-Host ""
        }
    } catch {
        Write-Host "  >> Erro ao verificar containers: $_" -ForegroundColor Red
        Write-Host ""
    }
    
    Write-Host "URLs dos Servicos:" -ForegroundColor Cyan
    Write-Host "  - Streamlit App: http://localhost:8501" -ForegroundColor White
    Write-Host "  - n8n Workflow: http://localhost:5678" -ForegroundColor White  
    Write-Host "  - Evolution API: http://localhost:8080" -ForegroundColor White
    Write-Host ""
}

function Start-InteractiveMenu {
    while ($true) {
        Show-Header
        Show-MainMenu
        
        $choice = Read-Host "Digite sua opcao (0-6)"
        
        switch ($choice) {
            "1" { 
                & ".\deploy.ps1"
                Read-Host "Pressione Enter para continuar..."
            }
            "2" { 
                & ".\monitor.ps1"
            }
            "3" { 
                & ".\web.ps1"
            }
            "4" { 
                Show-QuickStatus
                Read-Host "Pressione Enter para continuar..."
            }
            "5" { 
                & ".\stop.ps1"
                Read-Host "Pressione Enter para continuar..."
            }
            "6" {
                Clear-Host
                Show-Header
                Show-ProjectStructure
                Read-Host "Pressione Enter para continuar..."
            }
            "0" { 
                Clear-Host
                Write-Host "Obrigado por usar o SWAIF Stack Manager!" -ForegroundColor Green
                Write-Host "Projeto organizado e pronto para uso profissional!" -ForegroundColor Cyan
                Write-Host ""
                return 
            }
            default { 
                Write-Host "Opcao invalida! Tente novamente." -ForegroundColor Red
                Start-Sleep -Seconds 1
            }
        }
    }
}

# Executar baseado no parametro
switch ($Action) {
    "deploy" { & ".\deploy.ps1" }
    "monitor" { & ".\monitor.ps1" }
    "web" { & ".\web.ps1" }
    "stop" { & ".\stop.ps1" }
    "status" { Show-QuickStatus; Read-Host "Pressione Enter para continuar..." }
    "menu" { Start-InteractiveMenu }
    default { Start-InteractiveMenu }
}
