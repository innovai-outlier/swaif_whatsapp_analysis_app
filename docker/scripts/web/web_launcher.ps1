# SWAIF Stack Manager - Script Simples
# PowerShell - Deploy, Monitor e Acesso Web

param(
    [ValidateSet("deploy", "monitor", "stop", "status", "web")]
    [string]$Action = "web",
    [switch]$SingleRun = $false
)

# URLs dos servicos web principais
$WebServices = @{
    "streamlit" = @{Name="Streamlit App"; URL="http://localhost:8501"}
    "n8n" = @{Name="n8n Workflow"; URL="http://localhost:5678"}
    "evolution" = @{Name="Evolution API"; URL="http://localhost:8080"}
}

function Show-Banner {
    Clear-Host
    Write-Host ""
    Write-Host "===============================================================================" -ForegroundColor Cyan
    Write-Host "                    SWAIF STACK - Docker Manager                              " -ForegroundColor Cyan
    Write-Host "===============================================================================" -ForegroundColor Cyan
    Write-Host ""
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
        Write-Host "Abrindo $ServiceName..." -ForegroundColor Green
        Write-Host "URL: $Url" -ForegroundColor Cyan
        Start-Process $Url
        Write-Host "$ServiceName aberto no browser!" -ForegroundColor Green
        Start-Sleep -Seconds 2
    } catch {
        Write-Host "Erro ao abrir $ServiceName" -ForegroundColor Red
        Start-Sleep -Seconds 2
    }
}

function Show-WebMenu {
    Show-Banner
    Write-Host "SERVICOS WEB DISPONIVEIS" -ForegroundColor Yellow
    Write-Host ""
    
    $i = 1
    foreach ($key in $WebServices.Keys) {
        $service = $WebServices[$key]
        $status = Test-WebService $service.URL
        $statusColor = if ($status -eq "ONLINE") { "Green" } else { "Red" }
        
        Write-Host "[$i] $($service.Name)" -ForegroundColor Cyan
        Write-Host "    URL: $($service.URL)" -ForegroundColor Gray
        Write-Host "    Status: $status" -ForegroundColor $statusColor
        Write-Host ""
        $i++
    }
    
    Write-Host "[0] Sair" -ForegroundColor Gray
    Write-Host ""
    
    do {
        $choice = Read-Host "Escolha um servico para abrir (1-3) ou 0 para sair"
        switch ($choice) {
            "1" { Open-WebService $WebServices["streamlit"].URL $WebServices["streamlit"].Name }
            "2" { Open-WebService $WebServices["n8n"].URL $WebServices["n8n"].Name }
            "3" { Open-WebService $WebServices["evolution"].URL $WebServices["evolution"].Name }
            "0" { return }
            default { Write-Host "Opcao invalida!" -ForegroundColor Red }
        }
    } while ($choice -ne "0")
}

function Show-QuickStatus {
    Show-Banner
    Write-Host "STATUS RAPIDO DA STACK" -ForegroundColor Yellow
    Write-Host ""
    
    # Status dos servicos web
    Write-Host "Servicos Web:" -ForegroundColor Cyan
    foreach ($key in $WebServices.Keys) {
        $service = $WebServices[$key]
        $status = Test-WebService $service.URL
        $statusColor = if ($status -eq "ONLINE") { "Green" } else { "Red" }
        Write-Host "  $($service.Name): $status" -ForegroundColor $statusColor
    }
    
    Write-Host ""
    Write-Host "Containers Docker:" -ForegroundColor Cyan
    $containers = docker ps --format "table {{.Names}}\t{{.Status}}" 2>$null
    if ($containers) {
        $lines = $containers -split "`n"
        foreach ($line in $lines[1..([Math]::Min(8, $lines.Count-1))]) {
            Write-Host "  $line" -ForegroundColor Green
        }
    } else {
        Write-Host "  Nenhum container rodando" -ForegroundColor Red
    }
    
    if (-not $SingleRun) {
        Write-Host ""
        Write-Host "Pressione qualquer tecla para continuar..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
}

function Deploy-Stack {
    Write-Host "Iniciando deploy da stack..." -ForegroundColor Green
    & "..\..\scripts\deploy\start_stack.ps1"
}

function Stop-Stack {
    Write-Host "Parando a stack..." -ForegroundColor Red
    & "..\..\scripts\deploy\stop_stack.ps1"
}

function Start-Monitor {
    & "..\monitor\monitor_web.ps1"
}

# Executar baseado no parametro
switch ($Action) {
    "deploy" { Deploy-Stack }
    "monitor" { Start-Monitor }
    "stop" { Stop-Stack }
    "status" { Show-QuickStatus }
    "web" { Show-WebMenu }
    default { Show-WebMenu }
}
