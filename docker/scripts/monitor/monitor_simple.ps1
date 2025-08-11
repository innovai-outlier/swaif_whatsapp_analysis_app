# Script de Monitoramento Simples da Stack Docker SWAIF
# PowerShell - Dashboard basico

param(
    [int]$RefreshInterval = 10,
    [switch]$SingleRun = $false
)

# Lista de containers a monitorar
$Containers = @(
    @{Name="Redis Shared"; Container="swaif_redis"; Port="6379"},
    @{Name="PostgreSQL EVO"; Container="postgres_evo"; Port="5433"},
    @{Name="Redis EVO"; Container="redis_evo"; Port="6380"},
    @{Name="n8n Workflow"; Container="swaif_n8n"; Port="5678"},
    @{Name="PostgreSQL n8n"; Container="postgres_n8n"; Port="5434"},
    @{Name="Redis n8n"; Container="redis_n8n"; Port="6381"},
    @{Name="PostgreSQL Streamlit"; Container="postgres_streamlit"; Port="5435"}
)

function Get-ContainerStatus {
    param([string]$ContainerName)
    
    try {
        $result = docker ps --filter "name=$ContainerName" --format "{{.Status}}" 2>$null
        if ($result) {
            if ($result -match "Up") {
                return "ONLINE"
            } else {
                return "DEGRADED"
            }
        } else {
            return "OFFLINE"
        }
    } catch {
        return "ERROR"
    }
}

function Open-WebService {
    param([string]$Url, [string]$ServiceName)
    
    try {
        Write-Host "Abrindo $ServiceName..." -ForegroundColor Green
        Start-Process $Url
    } catch {
        Write-Host "Erro ao abrir $ServiceName`: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Show-MonitorDashboard {
    Clear-Host
    
    Write-Host "===============================================================================" -ForegroundColor Cyan
    Write-Host "                 STACK DOCKER SWAIF - MONITOR DASHBOARD" -ForegroundColor Cyan
    Write-Host "===============================================================================" -ForegroundColor Cyan
    Write-Host "Horario: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor White
    Write-Host "Atualizacao automatica a cada $RefreshInterval segundos" -ForegroundColor Gray
    Write-Host "===============================================================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Menu de acesso rapido
    Write-Host "🌐 ACESSO RAPIDO AOS SERVICOS:" -ForegroundColor Yellow
    Write-Host "  [1] Streamlit App     -> http://localhost:8501" -ForegroundColor Cyan
    Write-Host "  [2] n8n Workflow      -> http://localhost:5678" -ForegroundColor Cyan  
    Write-Host "  [3] Evolution API     -> http://localhost:8080" -ForegroundColor Cyan
    Write-Host "  Digite o numero + Enter para abrir no browser" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "SERVICO                   CONTAINER               STATUS        PORTA" -ForegroundColor White
    Write-Host "-----------------------------------------------------------------------" -ForegroundColor Gray
    
    $onlineCount = 0
    $offlineCount = 0
    $degradedCount = 0
    
    foreach ($service in $Containers) {
        $status = Get-ContainerStatus $service.Container
        
        $statusColor = switch ($status) {
            "ONLINE" { "Green"; $onlineCount++ }
            "DEGRADED" { "Yellow"; $degradedCount++ }
            "OFFLINE" { "Red"; $offlineCount++ }
            default { "Gray" }
        }
        
        $serviceName = $service.Name.PadRight(25)
        $containerName = $service.Container.PadRight(23)
        $port = $service.Port.PadRight(8)
        
        Write-Host "$serviceName $containerName " -NoNewline -ForegroundColor White
        Write-Host $status.PadRight(12) -NoNewline -ForegroundColor $statusColor
        Write-Host " $port" -ForegroundColor White
    }
    
    Write-Host "-----------------------------------------------------------------------" -ForegroundColor Gray
    Write-Host ""
    
    # Resumo
    Write-Host "RESUMO DO STATUS:" -ForegroundColor White
    Write-Host "  ONLINE: $onlineCount" -ForegroundColor Green
    Write-Host "  DEGRADED: $degradedCount" -ForegroundColor Yellow  
    Write-Host "  OFFLINE: $offlineCount" -ForegroundColor Red
    
    Write-Host ""
    
    # Verificar containers rodando
    Write-Host "CONTAINERS ATIVOS:" -ForegroundColor White
    $runningContainers = docker ps --format "table {{.Names}}\t{{.Status}}" 2>$null
    if ($runningContainers) {
        Write-Host $runningContainers -ForegroundColor Cyan
    } else {
        Write-Host "Nenhum container em execucao" -ForegroundColor Red
    }
    
    if (-not $SingleRun) {
        Write-Host ""
        Write-Host "💡 COMANDOS INTERATIVOS:" -ForegroundColor Yellow
        Write-Host "  1, 2, 3 -> Abrir servicos web no browser" -ForegroundColor Cyan
        Write-Host "  Ctrl+C  -> Parar monitoramento" -ForegroundColor Red
        Write-Host "===============================================================================" -ForegroundColor Cyan
    }
}

# Executar monitoramento
if ($SingleRun) {
    Show-MonitorDashboard
} else {
    Write-Host "Iniciando monitoramento da Stack Docker SWAIF..." -ForegroundColor Green
    Write-Host "Pressione 1, 2 ou 3 para abrir os servicos web no browser" -ForegroundColor Cyan
    Write-Host ""
    
    # Configurar para input nao bloqueante
    $host.UI.RawUI.KeyAvailable
    
    try {
        while ($true) {
            Show-MonitorDashboard
            
            # Verificar input do usuario por alguns segundos
            $timeout = $RefreshInterval
            while ($timeout -gt 0) {
                if ($host.UI.RawUI.KeyAvailable) {
                    $key = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
                    switch ($key.Character) {
                        '1' { 
                            Open-WebService "http://localhost:8501" "Streamlit App"
                        }
                        '2' { 
                            Open-WebService "http://localhost:5678" "n8n Workflow"
                        }
                        '3' { 
                            Open-WebService "http://localhost:8080" "Evolution API"
                        }
                    }
                    break
                }
                Start-Sleep -Seconds 1
                $timeout--
            }
        }
    } catch {
        Write-Host ""
        Write-Host "Monitoramento interrompido." -ForegroundColor Yellow
    }
}
