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
    Write-Host "                         SWAIF STACK MANAGER v2.0                            " -ForegroundColor Cyan  
    Write-Host "                         Docker Bundle Coordenado                            " -ForegroundColor White
    Write-Host "===============================================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Show-ProjectStructure {
    Write-Host "ESTRUTURA DO PROJETO:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "docker_coordinated/" -ForegroundColor White
    Write-Host "├── deploy.ps1              # Script principal de deploy" -ForegroundColor Green
    Write-Host "├── monitor.ps1             # Script principal de monitoramento" -ForegroundColor Cyan
    Write-Host "├── web.ps1                 # Script principal de acesso web" -ForegroundColor Blue
    Write-Host "├── stop.ps1                # Script principal de parada" -ForegroundColor Red
    Write-Host "├── main.ps1                # Este script (gerenciador)" -ForegroundColor Magenta
    Write-Host "├── docs/" -ForegroundColor Gray
    Write-Host "│   ├── guides/" -ForegroundColor Gray
    Write-Host "│   │   ├── QUICK_START.md" -ForegroundColor Gray
    Write-Host "│   │   └── SCRIPTS_GUIDE.md" -ForegroundColor Gray
    Write-Host "│   └── DEPLOY_GUIDE.md" -ForegroundColor Gray
    Write-Host "├── scripts/" -ForegroundColor Gray
    Write-Host "│   ├── deploy/             # Scripts de deploy/parada" -ForegroundColor Gray
    Write-Host "│   ├── monitor/            # Scripts de monitoramento" -ForegroundColor Gray
    Write-Host "│   └── web/                # Scripts de acesso web" -ForegroundColor Gray
    Write-Host "├── services/" -ForegroundColor Gray
    Write-Host "│   ├── redis_shared/" -ForegroundColor Gray
    Write-Host "│   ├── evo_api/" -ForegroundColor Gray
    Write-Host "│   ├── n8n/" -ForegroundColor Gray
    Write-Host "│   └── swaif_wab_streamlit/" -ForegroundColor Gray
    Write-Host "└── logs/                   # Logs de execucao" -ForegroundColor Gray
    Write-Host ""
}

function Show-MainMenu {
    Write-Host "ACOES DISPONIVEIS:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  [1] Deploy Stack           # Subir todos os containers" -ForegroundColor Green
    Write-Host "  [2] Monitor Dashboard      # Monitoramento em tempo real" -ForegroundColor Cyan
    Write-Host "  [3] Acesso Web             # Abrir servicos no browser" -ForegroundColor Blue
    Write-Host "  [4] Status Rapido          # Verificacao pontual" -ForegroundColor White
    Write-Host "  [5] Parar Stack            # Desligar todos os containers" -ForegroundColor Red
    Write-Host "  [6] Estrutura Projeto      # Mostrar organizacao de pastas" -ForegroundColor Yellow
    Write-Host "  [7] Documentacao           # Abrir guias de uso" -ForegroundColor Magenta
    Write-Host "  [0] Sair" -ForegroundColor Gray
    Write-Host ""
}

function Show-QuickStatus {
    Clear-Host
    Show-Header
    Write-Host "STATUS RAPIDO DA STACK" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "Containers Docker Ativos:" -ForegroundColor Cyan
    $containers = docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>$null
    if ($containers) {
        Write-Host ""
        Write-Host $containers -ForegroundColor Green
        Write-Host ""
    } else {
        Write-Host "  >> Nenhum container rodando" -ForegroundColor Red
        Write-Host ""
    }
    
    Write-Host "URLs dos Servicos:" -ForegroundColor Cyan
    Write-Host "  - Streamlit App: http://localhost:8501" -ForegroundColor White
    Write-Host "  - n8n Workflow: http://localhost:5678" -ForegroundColor White  
    Write-Host "  - Evolution API: http://localhost:8080" -ForegroundColor White
    Write-Host ""
}

function Show-Documentation {
    Clear-Host
    Show-Header
    Write-Host "DOCUMENTACAO DISPONIVEL" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "  [1] Guia Rapido (QUICK_START.md)" -ForegroundColor Green
    Write-Host "  [2] Guia Completo de Scripts (SCRIPTS_GUIDE.md)" -ForegroundColor Cyan
    Write-Host "  [3] Guia de Deploy (DEPLOY_GUIDE.md)" -ForegroundColor Yellow
    Write-Host "  [0] Voltar ao menu principal" -ForegroundColor Gray
    Write-Host ""
    
    $choice = Read-Host "Escolha uma documentacao para abrir"
    switch ($choice) {
        "1" { 
            if (Test-Path "docs\guides\QUICK_START.md") {
                Start-Process "docs\guides\QUICK_START.md"
            } else {
                Write-Host ">> Arquivo nao encontrado!" -ForegroundColor Red
            }
        }
        "2" { 
            if (Test-Path "docs\guides\SCRIPTS_GUIDE.md") {
                Start-Process "docs\guides\SCRIPTS_GUIDE.md"
            } else {
                Write-Host ">> Arquivo nao encontrado!" -ForegroundColor Red
            }
        }
        "3" { 
            if (Test-Path "docs\DEPLOY_GUIDE.md") {
                Start-Process "docs\DEPLOY_GUIDE.md"
            } else {
                Write-Host ">> Arquivo nao encontrado!" -ForegroundColor Red
            }
        }
    }
    
    if ($choice -ne "0") {
        Start-Sleep -Seconds 2
    }
}

function Start-InteractiveMenu {
    while ($true) {
        Show-Header
        Show-MainMenu
        
        $choice = Read-Host "Digite sua opção (0-7)"
        
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
            "7" {
                Show-Documentation
            }
            "0" { 
                Clear-Host
                Write-Host "Obrigado por usar o SWAIF Stack Manager!" -ForegroundColor Green
                Write-Host "Projeto organizado e pronto para uso profissional!" -ForegroundColor Cyan
                Write-Host ""
                return 
            }
            default { 
                Write-Host ">> Opcao invalida! Tente novamente." -ForegroundColor Red
                Start-Sleep -Seconds 1
            }
        }
    }
}

# Executar baseado no parâmetro
switch ($Action) {
    "deploy" { & ".\deploy.ps1" }
    "monitor" { & ".\monitor.ps1" }
    "web" { & ".\web.ps1" }
    "stop" { & ".\stop.ps1" }
    "status" { Show-QuickStatus; Read-Host "Pressione Enter para continuar..." }
    "menu" { Start-InteractiveMenu }
    default { Start-InteractiveMenu }
}
