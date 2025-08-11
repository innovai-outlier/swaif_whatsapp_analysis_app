# Script para parar toda a stack Docker do projeto swaif_whatsapp_app
# PowerShell - Stop Stack Script

$timestamp = Get-Date -Format 'yyyy-MM-dd_HH-mm-ss'
$MainLogFile = "..\..\logs\stack_shutdown_$timestamp.md"
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

function Stop-Service {
    param (
        [string]$ServiceDir,
        [string]$ServiceName
    )
    
    Write-Log "Parando ${ServiceName}..." "INFO"
    Add-Content -Path $MainLogFile -Value "`n## ${ServiceName}`n"
    
    Push-Location $ServiceDir
    
    # Executar docker-compose down
    Write-Host "Executando docker-compose down em $ServiceDir..." -ForegroundColor Yellow
    $output = docker-compose down 2>&1
    $exitCode = $LASTEXITCODE
    
    # Log no arquivo principal
    Add-Content -Path $MainLogFile -Value "### Comando Executado"
    Add-Content -Path $MainLogFile -Value "``````"
    Add-Content -Path $MainLogFile -Value "docker-compose down"
    Add-Content -Path $MainLogFile -Value "``````"
    Add-Content -Path $MainLogFile -Value "`n### Saída do Comando"
    Add-Content -Path $MainLogFile -Value "``````"
    Add-Content -Path $MainLogFile -Value ($output -join "`n")
    Add-Content -Path $MainLogFile -Value "``````"
    
    if ($exitCode -eq 0) {
        Write-Log "${ServiceName} parado com sucesso!" "SUCCESS"
    } else {
        Write-Log "Erro ao parar ${ServiceName}!" "ERROR"
    }
    
    Pop-Location
    Add-Content -Path $MainLogFile -Value "`n---`n"
}

Write-Log "Iniciando shutdown da stack Docker coordenada..." "INFO"
Add-Content -Path $MainLogFile -Value "# Stack Docker - Log de Shutdown`n"
Add-Content -Path $MainLogFile -Value "**Data/Hora:** $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n"
Add-Content -Path $MainLogFile -Value "**Projeto:** SWAIF WhatsApp Bundle Docker Coordenado`n"

# Parar serviços em ordem reversa
Stop-Service -ServiceDir "..\..\services\swaif_wab_streamlit" -ServiceName "SWAIF WAB Streamlit"
Stop-Service -ServiceDir "..\..\services\n8n" -ServiceName "n8n Workflow"
Stop-Service -ServiceDir "..\..\services\evo_api" -ServiceName "EVO API"
Stop-Service -ServiceDir "..\..\services\redis_shared" -ServiceName "Redis Shared"

$EndTime = Get-Date
$Duration = $EndTime - $StartTime

Write-Log "Todos os serviços foram parados!" "SUCCESS"
Write-Log "Tempo total de execução: $($Duration.TotalSeconds) segundos" "INFO"

Add-Content -Path $MainLogFile -Value "`n## Resumo Final`n"
Add-Content -Path $MainLogFile -Value "**Tempo de execução:** $($Duration.TotalSeconds) segundos`n"

Write-Log "Containers ainda rodando:" "INFO"
$containers = docker ps
Write-Host ($containers -join "`n") -ForegroundColor Cyan

Add-Content -Path $MainLogFile -Value "### Containers Restantes"
Add-Content -Path $MainLogFile -Value "``````"
Add-Content -Path $MainLogFile -Value ($containers -join "`n")
Add-Content -Path $MainLogFile -Value "``````"

Write-Log "Log de shutdown salvo em: $MainLogFile" "INFO"
