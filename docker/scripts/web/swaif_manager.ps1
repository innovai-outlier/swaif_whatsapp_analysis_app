# SWAIF Stack Manager - Script Completo
# PowerShell - Deploy, Monitor e Acesso Web Unificado

param(
    [ValidateSet("deploy", "monitor", "stop", "status", "web")]
    [string]$Action = "monitor",
    [int]$RefreshInterval = 10,
    [switch]$SingleRun = $false
)

# URLs dos servicos web principais
$WebServices = @{
    "streamlit" = @{Name="Streamlit App"; URL="http://localhost:8501"; Port="8501"}
    "n8n" = @{Name="n8n Workflow"; URL="http://localhost:5678"; Port="5678"}
    "evolution" = @{Name="Evolution API"; URL="http://localhost:8080"; Port="8080"}
}

function Show-Banner {
    Clear-Host
    Write-Host ""
    Write-Host "  ██████  ██     ██  █████  ██ ███████     ███████ ████████  █████   ██████ ██   ██ " -ForegroundColor Cyan
    Write-Host " ██       ██     ██ ██   ██ ██ ██          ██         ██    ██   ██ ██      ██  ██  " -ForegroundColor Cyan  
    Write-Host " ██████   ██  █  ██ ███████ ██ █████       ███████    ██    ███████ ██      █████   " -ForegroundColor Cyan
    Write-Host "      ██  ██ ███ ██ ██   ██ ██ ██               ██    ██    ██   ██ ██      ██  ██  " -ForegroundColor Cyan
    Write-Host " ██████    ███ ███  ██   ██ ██ ██          ███████    ██    ██   ██  ██████ ██   ██ " -ForegroundColor Cyan
    Write-Host ""
    Write-Host "                    🐳 Docker Stack Manager - WhatsApp Bundle                      " -ForegroundColor White
    Write-Host "================================================================================" -ForegroundColor Gray
}

function Show-Menu {
    Write-Host ""
    Write-Host "🎯 ACOES DISPONIVEIS:" -ForegroundColor Yellow
    Write-Host "  [1] Deploy Stack      -> Subir todos os containers" -ForegroundColor Green
    Write-Host "  [2] Monitor Dashboard -> Monitoramento em tempo real" -ForegroundColor Cyan
    Write-Host "  [3] Acesso Web        -> Abrir servicos no browser" -ForegroundColor Blue
    Write-Host "  [4] Status Rapido     -> Verificacao pontual" -ForegroundColor White
    Write-Host "  [5] Parar Stack       -> Desligar todos os containers" -ForegroundColor Red
    Write-Host "  [0] Sair" -ForegroundColor Gray
    Write-Host ""
}

function Deploy-Stack {
    Write-Host "🚀 Iniciando deploy da stack..." -ForegroundColor Green
    & ".\start_stack.ps1"
}

function Stop-Stack {
    Write-Host "🛑 Parando a stack..." -ForegroundColor Red
    & ".\stop_stack.ps1"
}

function Show-WebMenu {
    Clear-Host
    Show-Banner
    Write-Host "🌐 SERVICOS WEB DISPONIVEIS" -ForegroundColor Yellow
    Write-Host ""
    
    $i = 1
    foreach ($key in $WebServices.Keys) {
        $service = $WebServices[$key]
        $status = Test-WebService $service.URL
        $statusColor = if ($status -eq "ONLINE") { "Green" } else { "Red" }
        $statusIcon = if ($status -eq "ONLINE") { "🟢" } else { "🔴" }
        
        Write-Host "  [$i] $($service.Name)" -ForegroundColor Cyan
        Write-Host "      URL: $($service.URL)" -ForegroundColor Gray
        Write-Host "      Status: " -NoNewline -ForegroundColor Gray
        Write-Host "$statusIcon $status" -ForegroundColor $statusColor
        Write-Host ""
        $i++
    }
    
    Write-Host "  [0] Voltar ao menu principal" -ForegroundColor Gray
    Write-Host ""
    
    do {
        $choice = Read-Host "Escolha um servico para abrir (1-3) ou 0 para voltar"
        switch ($choice) {
            "1" { Open-WebService $WebServices["streamlit"].URL $WebServices["streamlit"].Name }
            "2" { Open-WebService $WebServices["n8n"].URL $WebServices["n8n"].Name }
            "3" { Open-WebService $WebServices["evolution"].URL $WebServices["evolution"].Name }
            "0" { return }
            default { Write-Host "Opcao invalida!" -ForegroundColor Red }
        }
    } while ($choice -ne "0")
}

function Test-WebService {
    param([string]$Url)
    try {
        $response = Invoke-WebRequest -Uri $Url -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
        return "ONLINE"
    } catch {
        return "OFFLINE"
    }
}

function Open-WebService {
    param([string]$Url, [string]$ServiceName)
    try {
        Write-Host "🌐 Abrindo $ServiceName..." -ForegroundColor Green
        Start-Process $Url
        Write-Host "✅ $ServiceName aberto no browser!" -ForegroundColor Green
        Start-Sleep -Seconds 2
    } catch {
        Write-Host "❌ Erro ao abrir $ServiceName" -ForegroundColor Red
        Start-Sleep -Seconds 2
    }
}

function Show-QuickStatus {
    Clear-Host
    Show-Banner
    Write-Host "📊 STATUS RAPIDO DA STACK" -ForegroundColor Yellow
    Write-Host ""
    
    # Status dos servicos web
    Write-Host "🌐 Servicos Web:" -ForegroundColor Cyan
    foreach ($key in $WebServices.Keys) {
        $service = $WebServices[$key]
        $status = Test-WebService $service.URL
        $statusColor = if ($status -eq "ONLINE") { "Green" } else { "Red" }
        $statusIcon = if ($status -eq "ONLINE") { "🟢" } else { "🔴" }
        Write-Host "  $statusIcon $($service.Name)" -ForegroundColor $statusColor
    }
    
    Write-Host ""
    Write-Host "🐳 Containers Docker:" -ForegroundColor Cyan
    $containers = docker ps --format "table {{.Names}}\t{{.Status}}" 2>$null
    if ($containers) {
        $lines = $containers -split "`n"
        foreach ($line in $lines[1..([Math]::Min(8, $lines.Count-1))]) {
            Write-Host "  🟢 $line" -ForegroundColor Green
        }
    } else {
        Write-Host "  🔴 Nenhum container rodando" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "Pressione qualquer tecla para voltar ao menu..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

function Start-Monitor {
    & ".\monitor_web.ps1"
}

function Show-MainMenu {
    while ($true) {
        Show-Banner
        Show-Menu
        
        $choice = Read-Host "Digite sua opcao (0-5)"
        
        switch ($choice) {
            "1" { Deploy-Stack; Read-Host "Pressione Enter para continuar..." }
            "2" { Start-Monitor }
            "3" { Show-WebMenu }
            "4" { Show-QuickStatus }
            "5" { Stop-Stack; Read-Host "Pressione Enter para continuar..." }
            "0" { 
                Write-Host "👋 Ate logo!" -ForegroundColor Green
                return 
            }
            default { 
                Write-Host "❌ Opcao invalida! Tente novamente." -ForegroundColor Red
                Start-Sleep -Seconds 1
            }
        }
    }
}

# Executar baseado no parametro
switch ($Action) {
    "deploy" { Deploy-Stack }
    "monitor" { 
        if ($SingleRun) {
            Show-QuickStatus
        } else {
            Start-Monitor
        }
    }
    "stop" { Stop-Stack }
    "status" { Show-QuickStatus }
    "web" { Show-WebMenu }
    default { Show-MainMenu }
}
