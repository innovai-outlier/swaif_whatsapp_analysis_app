# Script de Monitoramento da Stack Docker SWAIF
# PowerShell - Monitor com Dashboard em tempo real

param(
    [int]$RefreshInterval = 30,
    [switch]$ContinuousMode = $true
)

# Configuracoes dos servicos
$Services = @{
    "swaif_redis" = @{
        Name = "Redis Shared"
        URL = "localhost:6379"
        HealthCheck = "redis-cli -p 6379 ping"
        Type = "Redis"
    }
    "postgres_evo" = @{
        Name = "PostgreSQL EVO"
        URL = "localhost:5433"
        HealthCheck = "pg_isready -h localhost -p 5433"
        Type = "Database"
    }
    "redis_evo" = @{
        Name = "Redis EVO"
        URL = "localhost:6380"
        HealthCheck = "redis-cli -p 6380 ping"
        Type = "Redis"
    }
    "swaif_n8n" = @{
        Name = "n8n Workflow"
        URL = "http://localhost:5678"
        HealthCheck = "curl -s http://localhost:5678/healthz"
        Type = "Web"
    }
    "postgres_n8n" = @{
        Name = "PostgreSQL n8n"
        URL = "localhost:5434"
        HealthCheck = "pg_isready -h localhost -p 5434"
        Type = "Database"
    }
    "redis_n8n" = @{
        Name = "Redis n8n"
        URL = "localhost:6381"
        HealthCheck = "redis-cli -p 6381 ping"
        Type = "Redis"
    }
    "postgres_streamlit" = @{
        Name = "PostgreSQL Streamlit"
        URL = "localhost:5435"
        HealthCheck = "pg_isready -h localhost -p 5435"
        Type = "Database"
    }
    "streamlit_app" = @{
        Name = "Streamlit App"
        URL = "http://localhost:8501"
        HealthCheck = "curl -s http://localhost:8501/_stcore/health"
        Type = "Web"
    }
}

# Variaveis globais para monitoramento
$global:ServiceStats = @{}
$global:StartTime = Get-Date
$global:LogFile = "logs\monitor_$(Get-Date -Format 'yyyy-MM-dd').log"

# Inicializar estatisticas
foreach ($serviceId in $Services.Keys) {
    $global:ServiceStats[$serviceId] = @{
        FailureCount = 0
        LastFailure = $null
        Uptime = 0
        LastCheck = $null
        Status = "Unknown"
        ResponseTime = 0
    }
}

# Criar pasta logs se nao existir
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" -Force
}

function Write-MonitorLog {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    Add-Content -Path $global:LogFile -Value $logEntry
}

function Get-ContainerStatus {
    param([string]$ContainerName)
    
    try {
        $containerInfo = docker inspect $ContainerName 2>$null | ConvertFrom-Json
        if ($containerInfo) {
            $state = $containerInfo.State
            if ($state.Running -eq $true) {
                if ($state.Health) {
                    return $state.Health.Status
                } else {
                    return "running"
                }
            } else {
                return "stopped"
            }
        }
    } catch {
        return "not_found"
    }
    return "unknown"
}

function Test-ServiceHealth {
    param([hashtable]$Service, [string]$ServiceId)
    
    $startTime = Get-Date
    $status = "red"  # Padrao: vermelho
    $responseTime = 0
    
    try {
        $containerStatus = Get-ContainerStatus $ServiceId
        
        if ($containerStatus -eq "healthy" -or $containerStatus -eq "running") {
            # Container esta rodando, testar conectividade especifica
            switch ($Service.Type) {
                "Redis" {
                    $port = ($Service.URL -split ':')[1]
                    $result = Test-NetConnection -ComputerName "localhost" -Port $port -WarningAction SilentlyContinue
                    if ($result.TcpTestSucceeded) {
                        $status = "green"
                    } else {
                        $status = "yellow"
                    }
                }
                "Database" {
                    $port = ($Service.URL -split ':')[1]
                    $result = Test-NetConnection -ComputerName "localhost" -Port $port -WarningAction SilentlyContinue
                    if ($result.TcpTestSucceeded) {
                        $status = "green"
                    } else {
                        $status = "yellow"
                    }
                }
                "Web" {
                    try {
                        $response = Invoke-WebRequest -Uri $Service.URL -TimeoutSec 5 -ErrorAction Stop
                        if ($response.StatusCode -eq 200) {
                            $status = "green"
                        } else {
                            $status = "yellow"
                        }
                    } catch {
                        $status = "yellow"
                    }
                }
            }
        } elseif ($containerStatus -eq "stopped") {
            $status = "red"
        } else {
            $status = "yellow"
        }
        
        $responseTime = (Get-Date) - $startTime
        $responseTimeMs = [math]::Round($responseTime.TotalMilliseconds, 2)
        
        # Atualizar estatisticas
        $stats = $global:ServiceStats[$ServiceId]
        $stats.LastCheck = Get-Date
        $stats.Status = $status
        $stats.ResponseTime = $responseTimeMs
        
        if ($status -eq "red") {
            $stats.FailureCount++
            $stats.LastFailure = Get-Date
            Write-MonitorLog "Falha detectada no servico $ServiceId" "WARN"
        }
        
        return @{
            Status = $status
            ResponseTime = $responseTimeMs
            ContainerStatus = $containerStatus
        }
        
    } catch {
        $global:ServiceStats[$ServiceId].FailureCount++
        $global:ServiceStats[$ServiceId].LastFailure = Get-Date
        Write-MonitorLog "Erro ao verificar servico ${ServiceId}: $($_.Exception.Message)" "ERROR"
        
        return @{
            Status = "red"
            ResponseTime = 0
            ContainerStatus = "error"
        }
    }
}

function Show-Dashboard {
    Clear-Host
    
    $currentTime = Get-Date
    $uptime = $currentTime - $global:StartTime
    
    Write-Host "===============================================================================" -ForegroundColor White
    Write-Host "                    STACK DOCKER SWAIF - MONITOR DASHBOARD                     " -ForegroundColor White
    Write-Host "===============================================================================" -ForegroundColor White
    Write-Host " Horario: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | Uptime Monitor: $($uptime.ToString('hh\:mm\:ss'))                     " -ForegroundColor White
    Write-Host " Atualizacao: a cada $RefreshInterval segundos | Log: $global:LogFile      " -ForegroundColor White
    Write-Host "===============================================================================" -ForegroundColor White
    Write-Host ""
    
    # Cabecalho da tabela
    Write-Host "---------------------------------------------------------------------------------" -ForegroundColor Gray
    Write-Host " SERVICO                   URL/ENDPOINT           STATUS        RESP.    FALHAS " -ForegroundColor Gray
    Write-Host "---------------------------------------------------------------------------------" -ForegroundColor Gray
    
    foreach ($serviceId in $Services.Keys | Sort-Object) {
        $service = $Services[$serviceId]
        $result = Test-ServiceHealth $service $serviceId
        $stats = $global:ServiceStats[$serviceId]
        
        # Formatacao do status com cores
        $statusDisplay = switch ($result.Status) {
            "green"  { "ONLINE    " }
            "yellow" { "DEGRADADO " }
            "red"    { "OFFLINE   " }
            default  { "UNKNOWN   " }
        }
        
        $statusColor = switch ($result.Status) {
            "green"  { "Green" }
            "yellow" { "Yellow" }
            "red"    { "Red" }
            default  { "Gray" }
        }
        
        $serviceName = $service.Name.PadRight(25)
        $serviceUrl = $service.URL.PadRight(23)
        $responseTime = "$($result.ResponseTime)ms".PadRight(7)
        $failures = $stats.FailureCount.ToString().PadRight(8)
        
        Write-Host " $serviceName $serviceUrl " -NoNewline -ForegroundColor White
        Write-Host $statusDisplay -NoNewline -ForegroundColor $statusColor
        Write-Host " $responseTime $failures" -ForegroundColor White
    }
    
    Write-Host "---------------------------------------------------------------------------------" -ForegroundColor Gray
    
    # Resumo de status
    $totalServices = $Services.Count
    $onlineServices = ($global:ServiceStats.Values | Where-Object { $_.Status -eq "green" }).Count
    $degradedServices = ($global:ServiceStats.Values | Where-Object { $_.Status -eq "yellow" }).Count
    $offlineServices = ($global:ServiceStats.Values | Where-Object { $_.Status -eq "red" }).Count
    
    Write-Host ""
    Write-Host "RESUMO: " -NoNewline -ForegroundColor White
    Write-Host "$onlineServices Online  " -NoNewline -ForegroundColor Green
    Write-Host "$degradedServices Degradado  " -NoNewline -ForegroundColor Yellow
    Write-Host "$offlineServices Offline" -ForegroundColor Red
    
    $totalFailures = ($global:ServiceStats.Values | Measure-Object -Property FailureCount -Sum).Sum
    Write-Host "Total de falhas acumuladas: $totalFailures" -ForegroundColor $(if ($totalFailures -gt 0) { "Yellow" } else { "Green" })
    
    Write-Host ""
    Write-Host "Pressione Ctrl+C para parar o monitoramento" -ForegroundColor Cyan
    Write-Host "===============================================================================" -ForegroundColor Gray
}

# Funcao principal de monitoramento
function Start-Monitoring {
    Write-MonitorLog "Iniciando monitoramento da stack SWAIF" "INFO"
    
    if ($ContinuousMode) {
        Write-Host "Iniciando monitoramento continuo da Stack Docker SWAIF..." -ForegroundColor Green
        Write-Host "   Atualizacoes a cada $RefreshInterval segundos" -ForegroundColor Cyan
        Write-Host ""
        
        try {
            while ($true) {
                Show-Dashboard
                Start-Sleep -Seconds $RefreshInterval
            }
        } catch {
            Write-Host ""
            Write-Host "Monitoramento interrompido pelo usuario" -ForegroundColor Yellow
            Write-MonitorLog "Monitoramento interrompido pelo usuario" "INFO"
        }
    } else {
        Show-Dashboard
    }
}

# Executar monitoramento
Start-Monitoring
