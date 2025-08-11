# Script de Monitoramento Interativo da Stack Docker SWAIF
# PowerShell - Dashboard com acesso rapido aos servicos

param(
    [int]$RefreshInterval = 10,
    [switch]$SingleRun = $false
)

# Lista de containers a monitorar
$Containers = @(
    @{Name="Redis Shared"; Container="swaif_redis"; Port="6379"; Type="Redis"},
    @{Name="PostgreSQL EVO"; Container="postgres_evo"; Port="5433"; Type="Database"},
    @{Name="Redis EVO"; Container="redis_evo"; Port="6380"; Type="Redis"},
    @{Name="n8n Workflow"; Container="swaif_n8n"; Port="5678"; Type="Web"; URL="http://localhost:5678"},
    @{Name="PostgreSQL n8n"; Container="postgres_n8n"; Port="5434"; Type="Database"},
    @{Name="Redis n8n"; Container="redis_n8n"; Port="6381"; Type="Redis"},
    @{Name="PostgreSQL Streamlit"; Container="postgres_streamlit"; Port="5435"; Type="Database"}
)

# Servicos web principais
$WebServices = @(
    @{Name="Streamlit App"; URL="http://localhost:8501"; Key="1"; Description="Interface principal do SWAIF"},
    @{Name="n8n Workflow"; URL="http://localhost:5678"; Key="2"; Description="Automacao de workflows"},
    @{Name="Evolution API"; URL="http://localhost:8080"; Key="3"; Description="API do WhatsApp Evolution"}
)

function Get-ContainerStatus {
    param([string]$ContainerName)
    
    try {
        $result = docker ps --filter "name=$ContainerName" --format "{{.Status}}" 2>$null
        if ($result) {
            if ($result -match "Up") {
                return @{Status="ONLINE"; Details=$result}
            } else {
                return @{Status="DEGRADED"; Details=$result}
            }
        } else {
            return @{Status="OFFLINE"; Details="Container nao encontrado"}
        }
    } catch {
        return @{Status="ERROR"; Details="Erro ao verificar"}
    }
}

function Test-WebServiceStatus {
    param([string]$Url)
    
    try {
        $response = Invoke-WebRequest -Uri $Url -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
        return @{Status="ONLINE"; Code=$response.StatusCode}
    } catch {
        return @{Status="OFFLINE"; Code="Erro"}
    }
}

function Open-WebService {
    param([string]$Url, [string]$ServiceName)
    
    try {
        Write-Host ""
        Write-Host "🌐 Abrindo $ServiceName..." -ForegroundColor Green
        Write-Host "   URL: $Url" -ForegroundColor Cyan
        Start-Process $Url
        Write-Host "✅ Servico aberto no browser!" -ForegroundColor Green
        Start-Sleep -Seconds 2
    } catch {
        Write-Host "❌ Erro ao abrir $ServiceName`: $($_.Exception.Message)" -ForegroundColor Red
        Start-Sleep -Seconds 2
    }
}

function Show-InteractiveDashboard {
    Clear-Host
    
    Write-Host "╔══════════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor White
    Write-Host "║                    🐳 STACK DOCKER SWAIF - MONITOR INTERATIVO                   ║" -ForegroundColor White
    Write-Host "╠══════════════════════════════════════════════════════════════════════════════════╣" -ForegroundColor White
    Write-Host "║ Horário: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | Atualização: $RefreshInterval segundos                        ║" -ForegroundColor White
    Write-Host "╚══════════════════════════════════════════════════════════════════════════════════╝" -ForegroundColor White
    Write-Host ""
    
    # Secao de servicos web principais
    Write-Host "🌐 SERVIÇOS WEB PRINCIPAIS" -ForegroundColor Yellow
    Write-Host "┌─────┬─────────────────────────┬─────────────────────────┬────────────────────┐" -ForegroundColor Gray
    Write-Host "│ KEY │ SERVIÇO                 │ URL                     │ STATUS             │" -ForegroundColor Gray
    Write-Host "├─────┼─────────────────────────┼─────────────────────────┼────────────────────┤" -ForegroundColor Gray
    
    foreach ($service in $WebServices) {
        $webStatus = Test-WebServiceStatus $service.URL
        $statusColor = if ($webStatus.Status -eq "ONLINE") { "Green" } else { "Red" }
        $statusIcon = if ($webStatus.Status -eq "ONLINE") { "🟢" } else { "🔴" }
        
        $key = " $($service.Key)  ".PadRight(4)
        $name = $service.Name.PadRight(23)
        $url = $service.URL.PadRight(23)
        $status = "$statusIcon $($webStatus.Status)".PadRight(18)
        
        Write-Host "│$key │ $name │ $url │ " -NoNewline -ForegroundColor White
        Write-Host $status -NoNewline -ForegroundColor $statusColor
        Write-Host " │" -ForegroundColor White
    }
    
    Write-Host "└─────┴─────────────────────────┴─────────────────────────┴────────────────────┘" -ForegroundColor Gray
    Write-Host ""
    
    # Secao de containers
    Write-Host "🐳 STATUS DOS CONTAINERS" -ForegroundColor Yellow
    Write-Host "┌─────────────────────────┬──────────────────────────┬───────────────┬─────────┐" -ForegroundColor Gray
    Write-Host "│ SERVIÇO                 │ CONTAINER                │ STATUS        │ PORTA   │" -ForegroundColor Gray
    Write-Host "├─────────────────────────┼──────────────────────────┼───────────────┼─────────┤" -ForegroundColor Gray
    
    $onlineCount = 0
    $offlineCount = 0
    $degradedCount = 0
    
    foreach ($container in $Containers) {
        $status = Get-ContainerStatus $container.Container
        
        $statusColor = switch ($status.Status) {
            "ONLINE" { "Green"; $onlineCount++ }
            "DEGRADED" { "Yellow"; $degradedCount++ }
            "OFFLINE" { "Red"; $offlineCount++ }
            default { "Gray" }
        }
        
        $statusIcon = switch ($status.Status) {
            "ONLINE" { "🟢" }
            "DEGRADED" { "🟡" }
            "OFFLINE" { "🔴" }
            default { "⚪" }
        }
        
        $serviceName = $container.Name.PadRight(23)
        $containerName = $container.Container.PadRight(24)
        $port = $container.Port.PadRight(7)
        $statusDisplay = "$statusIcon $($status.Status)".PadRight(13)
        
        Write-Host "│ $serviceName │ $containerName │ " -NoNewline -ForegroundColor White
        Write-Host $statusDisplay -NoNewline -ForegroundColor $statusColor
        Write-Host " │ $port │" -ForegroundColor White
    }
    
    Write-Host "└─────────────────────────┴──────────────────────────┴───────────────┴─────────┘" -ForegroundColor Gray
    Write-Host ""
    
    # Resumo de status
    Write-Host "📊 RESUMO GERAL" -ForegroundColor Yellow
    Write-Host "  🟢 Online: $onlineCount   🟡 Degradado: $degradedCount   🔴 Offline: $offlineCount" -ForegroundColor White
    
    # Verificar containers Docker
    Write-Host ""
    Write-Host "🐳 CONTAINERS DOCKER ATIVOS" -ForegroundColor Yellow
    $runningContainers = docker ps --format "table {{.Names}}\t{{.Status}}" 2>$null
    if ($runningContainers) {
        $lines = $runningContainers -split "`n"
        foreach ($line in $lines[0..([Math]::Min(5, $lines.Count-1))]) {
            Write-Host "  $line" -ForegroundColor Cyan
        }
        if ($lines.Count -gt 6) {
            Write-Host "  ... e mais $($lines.Count - 6) containers" -ForegroundColor Gray
        }
    } else {
        Write-Host "  ❌ Nenhum container em execução" -ForegroundColor Red
    }
    
    if (-not $SingleRun) {
        Write-Host ""
        Write-Host "💡 COMANDOS DISPONÍVEIS" -ForegroundColor Yellow
        Write-Host "  1, 2, 3  -> Abrir serviços web no browser" -ForegroundColor Cyan
        Write-Host "  r        -> Atualizar agora" -ForegroundColor Green
        Write-Host "  q        -> Sair do monitoramento" -ForegroundColor Red
        Write-Host "  Ctrl+C   -> Forçar saída" -ForegroundColor Red
        Write-Host ""
        Write-Host "════════════════════════════════════════════════════════════════════════════════════════" -ForegroundColor Gray
    }
}

# Executar monitoramento
if ($SingleRun) {
    Show-InteractiveDashboard
} else {
    Write-Host "🚀 Iniciando Monitor Interativo da Stack Docker SWAIF..." -ForegroundColor Green
    Write-Host "   Pressione as teclas numéricas para abrir os serviços web" -ForegroundColor Cyan
    Write-Host ""
    
    try {
        while ($true) {
            Show-InteractiveDashboard
            
            # Verificar input do usuario
            $timeout = $RefreshInterval * 10  # timeout em decisegundos
            while ($timeout -gt 0) {
                if ($host.UI.RawUI.KeyAvailable) {
                    $key = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
                    
                    switch ($key.Character) {
                        '1' { 
                            Open-WebService $WebServices[0].URL $WebServices[0].Name
                            break
                        }
                        '2' { 
                            Open-WebService $WebServices[1].URL $WebServices[1].Name
                            break
                        }
                        '3' { 
                            Open-WebService $WebServices[2].URL $WebServices[2].Name
                            break
                        }
                        'r' {
                            Write-Host "🔄 Atualizando dashboard..." -ForegroundColor Yellow
                            Start-Sleep -Seconds 1
                            break
                        }
                        'q' {
                            Write-Host "👋 Saindo do monitoramento..." -ForegroundColor Yellow
                            return
                        }
                    }
                }
                Start-Sleep -Milliseconds 100
                $timeout--
            }
        }
    } catch {
        Write-Host ""
        Write-Host "🛑 Monitoramento interrompido." -ForegroundColor Yellow
    }
}
