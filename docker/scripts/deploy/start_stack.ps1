# Script para subir toda a stack Docker do projeto swaif_whatsapp_app
# Executa cada etapa e mostra logs de cada serviço

$timestamp = Get-Date -Format 'yyyy-MM-dd_HH-mm-ss'
$MainLogFile = "..\..\logs\stack_deployment_$timestamp.md"
$StartTime = Get-Date

# Criar pasta logs se não existir
if (-not (Test-Path "..\..\logs")) {
    New-Item -ItemType Directory -Path "..\..\logs" -Force
}

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    Write-Host $logEntry -ForegroundColor $(
        switch ($Level) {
            "ERROR" { "Red" }
            "WARN" { "Yellow" }
            "SUCCESS" { "Green" }
            default { "White" }
        }
    )
    Add-Content -Path $MainLogFile -Value $logEntry
}

function Start-Service {
    param (
        [string]$ServiceDir,
        [string]$ServiceName
    )
    
    # Criar pasta logs no diretório do serviço se não existir
    $absoluteServiceDir = Resolve-Path $ServiceDir
    $serviceLogDir = Join-Path $absoluteServiceDir "logs"
    if (-not (Test-Path $serviceLogDir)) {
        New-Item -ItemType Directory -Path $serviceLogDir -Force
    }
    
    $serviceLogFile = Join-Path $serviceLogDir "deployment_$timestamp.md"
    
    Write-Log "Subindo ${ServiceName}..." "INFO"
    Add-Content -Path $MainLogFile -Value "`n## ${ServiceName}`n"
    Add-Content -Path $serviceLogFile -Value "# Deployment Log - ${ServiceName}`n"
    Add-Content -Path $serviceLogFile -Value "**Data/Hora:** $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n"
    
    Push-Location $ServiceDir
    
    # Executar docker-compose up
    Write-Host "Executando docker-compose up -d em $ServiceDir..." -ForegroundColor Yellow
    $output = docker-compose up -d 2>&1
    $exitCode = $LASTEXITCODE
    
    # Log no arquivo principal
    Add-Content -Path $MainLogFile -Value "### Comando Executado"
    Add-Content -Path $MainLogFile -Value "``````"
    Add-Content -Path $MainLogFile -Value "docker-compose up -d"
    Add-Content -Path $MainLogFile -Value "``````"
    Add-Content -Path $MainLogFile -Value "`n### Saída do Comando"
    Add-Content -Path $MainLogFile -Value "``````"
    Add-Content -Path $MainLogFile -Value ($output -join "`n")
    Add-Content -Path $MainLogFile -Value "``````"
    
    # Log no arquivo do serviço
    Add-Content -Path $serviceLogFile -Value "## Comando Executado`n"
    Add-Content -Path $serviceLogFile -Value "``````bash"
    Add-Content -Path $serviceLogFile -Value "docker-compose up -d"
    Add-Content -Path $serviceLogFile -Value "``````"
    Add-Content -Path $serviceLogFile -Value "`n## Saída do Comando`n"
    Add-Content -Path $serviceLogFile -Value "``````"
    Add-Content -Path $serviceLogFile -Value ($output -join "`n")
    Add-Content -Path $serviceLogFile -Value "``````"
    
    if ($exitCode -eq 0) {
        Write-Log "${ServiceName} iniciado com sucesso!" "SUCCESS"
        
        # Aguardar um pouco para os containers estabilizarem
        Start-Sleep -Seconds 5
        
        # Mostrar logs recentes (mais detalhados)
        Write-Log "Capturando logs detalhados de ${ServiceName}..." "INFO"
        $logs = docker-compose logs --tail 50 2>&1
        Add-Content -Path $MainLogFile -Value "`n### Logs Recentes (50 linhas)"
        Add-Content -Path $MainLogFile -Value "``````"
        Add-Content -Path $MainLogFile -Value ($logs -join "`n")
        Add-Content -Path $MainLogFile -Value "``````"
        
        Add-Content -Path $serviceLogFile -Value "`n## Logs Recentes (50 linhas)`n"
        Add-Content -Path $serviceLogFile -Value "``````"
        Add-Content -Path $serviceLogFile -Value ($logs -join "`n")
        Add-Content -Path $serviceLogFile -Value "``````"
        
        # Verificar status dos containers
        $status = docker-compose ps 2>&1
        Add-Content -Path $MainLogFile -Value "`n### Status dos Containers"
        Add-Content -Path $MainLogFile -Value "``````"
        Add-Content -Path $MainLogFile -Value ($status -join "`n")
        Add-Content -Path $MainLogFile -Value "``````"
        
        Add-Content -Path $serviceLogFile -Value "`n## Status dos Containers`n"
        Add-Content -Path $serviceLogFile -Value "``````"
        Add-Content -Path $serviceLogFile -Value ($status -join "`n")
        Add-Content -Path $serviceLogFile -Value "``````"
        
        # Verificar saúde dos containers
        Write-Log "Verificando saúde dos containers..." "INFO"
        $health = docker-compose ps --format "table {{.Name}}\t{{.Status}}" 2>&1
        Add-Content -Path $serviceLogFile -Value "`n## Saúde dos Containers`n"
        Add-Content -Path $serviceLogFile -Value "``````"
        Add-Content -Path $serviceLogFile -Value ($health -join "`n")
        Add-Content -Path $serviceLogFile -Value "``````"
        
    } else {
        Write-Log "Erro ao iniciar ${ServiceName}!" "ERROR"
        
        # Capturar logs de erro mais detalhados
        Write-Log "Capturando logs de erro detalhados..." "WARN"
        $errorLogs = docker-compose logs --tail 100 2>&1
        Add-Content -Path $MainLogFile -Value "`n### LOGS DE ERRO (100 linhas)"
        Add-Content -Path $MainLogFile -Value "``````"
        Add-Content -Path $MainLogFile -Value ($errorLogs -join "`n")
        Add-Content -Path $MainLogFile -Value "``````"
        
        Add-Content -Path $serviceLogFile -Value "`n## LOGS DE ERRO (100 linhas)`n"
        Add-Content -Path $serviceLogFile -Value "``````"
        Add-Content -Path $serviceLogFile -Value ($errorLogs -join "`n")
        Add-Content -Path $serviceLogFile -Value "``````"
        
        # Tentar obter informações sobre containers que falharam
        $failedContainers = docker-compose ps --all 2>&1
        Add-Content -Path $serviceLogFile -Value "`n## Containers com Falha`n"
        Add-Content -Path $serviceLogFile -Value "``````"
        Add-Content -Path $serviceLogFile -Value ($failedContainers -join "`n")
        Add-Content -Path $serviceLogFile -Value "``````"
    }
    
    Pop-Location
    Add-Content -Path $MainLogFile -Value "`n---`n"
    Add-Content -Path $serviceLogFile -Value "`n---`n"
    Write-Log "Log detalhado do ${ServiceName} salvo em: $serviceLogFile" "INFO"
}

Write-Log "Iniciando stack Docker coordenada..." "INFO"
Add-Content -Path $MainLogFile -Value "# Stack Docker - Log de Deployment`n"
Add-Content -Path $MainLogFile -Value "**Data/Hora:** $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n"
Add-Content -Path $MainLogFile -Value "**Projeto:** SWAIF WhatsApp Bundle Docker Coordenado`n"

# Subir Redis
Start-Service -ServiceDir "..\..\services\redis_shared" -ServiceName "Redis Shared"

# Subir API
Start-Service -ServiceDir "..\..\services\evo_api" -ServiceName "EVO API"

# Subir n8n
Start-Service -ServiceDir "..\..\services\n8n" -ServiceName "n8n Workflow"

# Subir Streamlit
Start-Service -ServiceDir "..\..\services\swaif_wab_streamlit" -ServiceName "SWAIF WAB Streamlit"

$EndTime = Get-Date
$Duration = $EndTime - $StartTime

Write-Log "Todos os serviços foram processados!" "SUCCESS"
Write-Log "Tempo total de execução: $($Duration.TotalSeconds) segundos" "INFO"

Add-Content -Path $MainLogFile -Value "`n## Resumo Final`n"
Add-Content -Path $MainLogFile -Value "**Tempo de execução:** $($Duration.TotalSeconds) segundos`n"

Write-Log "Containers rodando:" "INFO"
$containers = docker ps
Write-Host ($containers -join "`n") -ForegroundColor Cyan

Add-Content -Path $MainLogFile -Value "### Containers Ativos"
Add-Content -Path $MainLogFile -Value "``````"
Add-Content -Path $MainLogFile -Value ($containers -join "`n")
Add-Content -Path $MainLogFile -Value "``````"

Write-Log "Log principal salvo em: $MainLogFile" "INFO"
Write-Log "Logs detalhados de cada serviço estão em suas respectivas pastas logs/" "INFO"
