#!/bin/bash
# Script para subir toda a stack Docker do projeto swaif_whatsapp_app
# Executa cada etapa e mostra logs de cada serviço

timestamp=$(date '+%Y-%m-%d_%H-%M-%S')
MainLogFile="logs/stack_deployment_$timestamp.md"
StartTime=$(date)

# Criar pasta logs se não existir
mkdir -p logs

# Função para log colorido
write_log() {
    local message="$1"
    local level="${2:-INFO}"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local log_entry="[$timestamp] [$level] $message"
    
    case $level in
        "ERROR")
            echo -e "\e[31m$log_entry\e[0m"
            ;;
        "WARN")
            echo -e "\e[33m$log_entry\e[0m"
            ;;
        "SUCCESS")
            echo -e "\e[32m$log_entry\e[0m"
            ;;
        *)
            echo "$log_entry"
            ;;
    esac
    
    echo "$log_entry" >> "$MainLogFile"
}

# Função para iniciar serviço
start_service() {
    local service_dir="$1"
    local service_name="$2"
    
    # Criar pasta logs no diretório do serviço se não existir
    mkdir -p "$service_dir/logs"
    
    local service_log_file="$service_dir/logs/deployment_$timestamp.md"
    
    write_log "Subindo $service_name..." "INFO"
    echo "" >> "$MainLogFile"
    echo "## $service_name" >> "$MainLogFile"
    echo "" >> "$MainLogFile"
    
    echo "# Deployment Log - $service_name" > "$service_log_file"
    echo "**Data/Hora:** $(date '+%Y-%m-%d %H:%M:%S')" >> "$service_log_file"
    echo "" >> "$service_log_file"
    
    pushd "$service_dir" > /dev/null
    
    # Executar docker-compose up
    echo "Executando docker-compose up -d em $service_dir..."
    output=$(docker-compose up -d 2>&1)
    exit_code=$?
    
    # Log no arquivo principal
    echo "### Comando Executado" >> "$MainLogFile"
    echo "\`\`\`" >> "$MainLogFile"
    echo "docker-compose up -d" >> "$MainLogFile"
    echo "\`\`\`" >> "$MainLogFile"
    echo "" >> "$MainLogFile"
    echo "### Saída do Comando" >> "$MainLogFile"
    echo "\`\`\`" >> "$MainLogFile"
    echo "$output" >> "$MainLogFile"
    echo "\`\`\`" >> "$MainLogFile"
    
    # Log no arquivo do serviço
    echo "## Comando Executado" >> "$service_log_file"
    echo "\`\`\`bash" >> "$service_log_file"
    echo "docker-compose up -d" >> "$service_log_file"
    echo "\`\`\`" >> "$service_log_file"
    echo "" >> "$service_log_file"
    echo "## Saída do Comando" >> "$service_log_file"
    echo "\`\`\`" >> "$service_log_file"
    echo "$output" >> "$service_log_file"
    echo "\`\`\`" >> "$service_log_file"
    
    if [ $exit_code -eq 0 ]; then
        write_log "$service_name iniciado com sucesso!" "SUCCESS"
        
        # Aguardar um pouco para os containers estabilizarem
        sleep 5
        
        # Mostrar logs recentes (mais detalhados)
        write_log "Capturando logs detalhados de $service_name..." "INFO"
        logs=$(docker-compose logs --tail 50 2>&1)
        echo "" >> "$MainLogFile"
        echo "### Logs Recentes (50 linhas)" >> "$MainLogFile"
        echo "\`\`\`" >> "$MainLogFile"
        echo "$logs" >> "$MainLogFile"
        echo "\`\`\`" >> "$MainLogFile"
        
        echo "" >> "$service_log_file"
        echo "## Logs Recentes (50 linhas)" >> "$service_log_file"
        echo "\`\`\`" >> "$service_log_file"
        echo "$logs" >> "$service_log_file"
        echo "\`\`\`" >> "$service_log_file"
        
        # Verificar status dos containers
        status=$(docker-compose ps 2>&1)
        echo "" >> "$MainLogFile"
        echo "### Status dos Containers" >> "$MainLogFile"
        echo "\`\`\`" >> "$MainLogFile"
        echo "$status" >> "$MainLogFile"
        echo "\`\`\`" >> "$MainLogFile"
        
        echo "" >> "$service_log_file"
        echo "## Status dos Containers" >> "$service_log_file"
        echo "\`\`\`" >> "$service_log_file"
        echo "$status" >> "$service_log_file"
        echo "\`\`\`" >> "$service_log_file"
        
        # Verificar saúde dos containers
        write_log "Verificando saúde dos containers..." "INFO"
        health=$(docker-compose ps --format "table {{.Name}}\t{{.Status}}" 2>&1)
        echo "" >> "$service_log_file"
        echo "## Saúde dos Containers" >> "$service_log_file"
        echo "\`\`\`" >> "$service_log_file"
        echo "$health" >> "$service_log_file"
        echo "\`\`\`" >> "$service_log_file"
        
    else
        write_log "Erro ao iniciar $service_name!" "ERROR"
        
        # Capturar logs de erro mais detalhados
        write_log "Capturando logs de erro detalhados..." "WARN"
        error_logs=$(docker-compose logs --tail 100 2>&1)
        echo "" >> "$MainLogFile"
        echo "### LOGS DE ERRO (100 linhas)" >> "$MainLogFile"
        echo "\`\`\`" >> "$MainLogFile"
        echo "$error_logs" >> "$MainLogFile"
        echo "\`\`\`" >> "$MainLogFile"
        
        echo "" >> "$service_log_file"
        echo "## LOGS DE ERRO (100 linhas)" >> "$service_log_file"
        echo "\`\`\`" >> "$service_log_file"
        echo "$error_logs" >> "$service_log_file"
        echo "\`\`\`" >> "$service_log_file"
        
        # Tentar obter informações sobre containers que falharam
        failed_containers=$(docker-compose ps --all 2>&1)
        echo "" >> "$service_log_file"
        echo "## Containers com Falha" >> "$service_log_file"
        echo "\`\`\`" >> "$service_log_file"
        echo "$failed_containers" >> "$service_log_file"
        echo "\`\`\`" >> "$service_log_file"
    fi
    
    popd > /dev/null
    echo "" >> "$MainLogFile"
    echo "---" >> "$MainLogFile"
    echo "" >> "$MainLogFile"
    write_log "Log detalhado do $service_name salvo em: $service_log_file" "INFO"
}

write_log "Iniciando stack Docker coordenada..." "INFO"
echo "# Stack Docker - Log de Deployment" > "$MainLogFile"
echo "" >> "$MainLogFile"
echo "**Data/Hora:** $(date '+%Y-%m-%d %H:%M:%S')" >> "$MainLogFile"
echo "**Projeto:** SWAIF WhatsApp Bundle Docker Coordenado" >> "$MainLogFile"
echo "" >> "$MainLogFile"

# Subir Redis
start_service "redis_shared" "Redis Shared"

# Subir API
start_service "evo_api" "EVO API"

# Subir n8n
start_service "n8n" "n8n Workflow"

# Subir Streamlit
start_service "swaif_wab_streamlit" "SWAIF WAB Streamlit"

EndTime=$(date)

write_log "Todos os serviços foram processados!" "SUCCESS"
write_log "Iniciado em: $StartTime" "INFO"
write_log "Finalizado em: $EndTime" "INFO"

echo "" >> "$MainLogFile"
echo "## Resumo Final" >> "$MainLogFile"
echo "**Iniciado em:** $StartTime" >> "$MainLogFile"
echo "**Finalizado em:** $EndTime" >> "$MainLogFile"

write_log "Containers rodando:" "INFO"
containers=$(docker ps)
echo "$containers"

echo "### Containers Ativos" >> "$MainLogFile"
echo "\`\`\`" >> "$MainLogFile"
echo "$containers" >> "$MainLogFile"
echo "\`\`\`" >> "$MainLogFile"

write_log "Log principal salvo em: $MainLogFile" "INFO"
write_log "Logs detalhados de cada serviço estão em suas respectivas pastas logs/" "INFO"
