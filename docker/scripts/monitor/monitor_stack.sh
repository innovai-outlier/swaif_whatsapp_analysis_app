#!/bin/bash
# Script de Monitoramento da Stack Docker SWAIF
# Bash - Monitor com Dashboard em tempo real

# Configurações
REFRESH_INTERVAL=30
LOG_FILE="logs/monitor_$(date '+%Y-%m-%d').log"
START_TIME=$(date +%s)

# Cores ANSI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

# Emojis de status
STATUS_ONLINE="🟢"
STATUS_DEGRADED="🟡"
STATUS_OFFLINE="🔴"
STATUS_UNKNOWN="⚪"

# Configurações dos serviços
declare -A SERVICES=(
    ["swaif_redis"]="Redis Shared|localhost:6379|redis"
    ["postgres_evo"]="PostgreSQL EVO|localhost:5433|database"
    ["redis_evo"]="Redis EVO|localhost:6380|redis"
    ["swaif_n8n"]="n8n Workflow|localhost:5678|web"
    ["postgres_n8n"]="PostgreSQL n8n|localhost:5434|database"
    ["redis_n8n"]="Redis n8n|localhost:6381|redis"
    ["postgres_streamlit"]="PostgreSQL Streamlit|localhost:5435|database"
)

# Arrays para estatísticas
declare -A FAILURE_COUNT
declare -A LAST_FAILURE
declare -A LAST_CHECK
declare -A RESPONSE_TIME

# Criar pasta logs se não existir
mkdir -p logs

# Função para log
write_log() {
    local message="$1"
    local level="${2:-INFO}"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
}

# Função para verificar status do container
get_container_status() {
    local container_name="$1"
    
    if ! docker inspect "$container_name" &>/dev/null; then
        echo "not_found"
        return
    fi
    
    local is_running=$(docker inspect --format='{{.State.Running}}' "$container_name" 2>/dev/null)
    local health_status=$(docker inspect --format='{{.State.Health.Status}}' "$container_name" 2>/dev/null)
    
    if [[ "$is_running" == "true" ]]; then
        if [[ "$health_status" == "healthy" ]] || [[ "$health_status" == "<no value>" ]]; then
            echo "running"
        else
            echo "$health_status"
        fi
    else
        echo "stopped"
    fi
}

# Função para testar conectividade do serviço
test_service_connectivity() {
    local service_url="$1"
    local service_type="$2"
    local start_time=$(date +%s%N)
    
    case "$service_type" in
        "redis")
            local port=$(echo "$service_url" | cut -d':' -f2)
            if timeout 5 bash -c "</dev/tcp/localhost/$port" 2>/dev/null; then
                echo "online"
            else
                echo "degraded"
            fi
            ;;
        "database")
            local port=$(echo "$service_url" | cut -d':' -f2)
            if timeout 5 bash -c "</dev/tcp/localhost/$port" 2>/dev/null; then
                echo "online"
            else
                echo "degraded"
            fi
            ;;
        "web")
            local url="http://$service_url"
            if curl -s --max-time 5 "$url" >/dev/null 2>&1; then
                echo "online"
            else
                echo "degraded"
            fi
            ;;
        *)
            echo "unknown"
            ;;
    esac
    
    local end_time=$(date +%s%N)
    local duration=$(((end_time - start_time) / 1000000))
    echo "$duration"
}

# Função para verificar saúde do serviço
check_service_health() {
    local container_name="$1"
    local service_info="$2"
    
    IFS='|' read -r service_name service_url service_type <<< "$service_info"
    
    local container_status=$(get_container_status "$container_name")
    local connectivity_result
    local response_time=0
    
    if [[ "$container_status" == "running" ]] || [[ "$container_status" == "healthy" ]]; then
        local test_result=$(test_service_connectivity "$service_url" "$service_type")
        local connectivity_status=$(echo "$test_result" | head -n1)
        response_time=$(echo "$test_result" | tail -n1)
        
        case "$connectivity_status" in
            "online")
                echo "green|$response_time"
                ;;
            "degraded")
                echo "yellow|$response_time"
                ;;
            *)
                echo "red|0"
                ;;
        esac
    elif [[ "$container_status" == "stopped" ]] || [[ "$container_status" == "not_found" ]]; then
        echo "red|0"
    else
        echo "yellow|0"
    fi
}

# Função para mostrar o dashboard
show_dashboard() {
    clear
    
    local current_time=$(date '+%Y-%m-%d %H:%M:%S')
    local uptime_seconds=$(($(date +%s) - START_TIME))
    local uptime_formatted=$(printf "%02d:%02d:%02d" $((uptime_seconds/3600)) $(((uptime_seconds%3600)/60)) $((uptime_seconds%60)))
    
    echo -e "${WHITE}╔══════════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${WHITE}║                    🐳 STACK DOCKER SWAIF - MONITOR DASHBOARD                     ║${NC}"
    echo -e "${WHITE}╠══════════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${WHITE}║ Horário: $current_time | Uptime Monitor: $uptime_formatted                     ║${NC}"
    echo -e "${WHITE}║ Atualização: a cada $REFRESH_INTERVAL segundos | Log: $LOG_FILE      ║${NC}"
    echo -e "${WHITE}╚══════════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Cabeçalho da tabela
    echo -e "${GRAY}┌─────────────────────────┬──────────────────────┬───────────────┬─────────┬──────────┬─────────────┐${NC}"
    echo -e "${GRAY}│ SERVIÇO                 │ URL/ENDPOINT         │ STATUS        │ RESP.   │ FALHAS   │ ÚLTIMO OK   │${NC}"
    echo -e "${GRAY}├─────────────────────────┼──────────────────────┼───────────────┼─────────┼──────────┼─────────────┤${NC}"
    
    local total_services=0
    local online_services=0
    local degraded_services=0
    local offline_services=0
    
    for container_name in $(echo "${!SERVICES[@]}" | tr ' ' '\n' | sort); do
        local service_info="${SERVICES[$container_name]}"
        IFS='|' read -r service_name service_url service_type <<< "$service_info"
        
        local health_result=$(check_service_health "$container_name" "$service_info")
        IFS='|' read -r status_color response_time <<< "$health_result"
        
        # Atualizar estatísticas
        LAST_CHECK["$container_name"]=$(date '+%H:%M:%S')
        RESPONSE_TIME["$container_name"]=$response_time
        
        if [[ "$status_color" == "red" ]]; then
            ((FAILURE_COUNT["$container_name"]++))
            LAST_FAILURE["$container_name"]=$(date '+%H:%M:%S')
            write_log "Falha detectada no serviço $container_name" "WARN"
            ((offline_services++))
        elif [[ "$status_color" == "yellow" ]]; then
            ((degraded_services++))
        elif [[ "$status_color" == "green" ]]; then
            ((online_services++))
        fi
        
        ((total_services++))
        
        # Formatação do status com cores
        local status_display
        local status_color_display
        case "$status_color" in
            "green")
                status_display="${STATUS_ONLINE} ONLINE    "
                status_color_display="${GREEN}"
                ;;
            "yellow")
                status_display="${STATUS_DEGRADED} DEGRADADO "
                status_color_display="${YELLOW}"
                ;;
            "red")
                status_display="${STATUS_OFFLINE} OFFLINE   "
                status_color_display="${RED}"
                ;;
            *)
                status_display="${STATUS_UNKNOWN} UNKNOWN   "
                status_color_display="${GRAY}"
                ;;
        esac
        
        local service_name_padded=$(printf "%-23s" "$service_name")
        local service_url_padded=$(printf "%-20s" "$service_url")
        local response_time_padded=$(printf "%-7s" "${response_time}ms")
        local failures_padded=$(printf "%-8s" "${FAILURE_COUNT[$container_name]:-0}")
        local last_ok_padded=$(printf "%-11s" "${LAST_CHECK[$container_name]:-"---"}")
        
        echo -e "${WHITE}│ $service_name_padded │ $service_url_padded │ ${status_color_display}$status_display${WHITE} │ $response_time_padded │ $failures_padded │ $last_ok_padded │${NC}"
    done
    
    echo -e "${GRAY}└─────────────────────────┴──────────────────────┴───────────────┴─────────┴──────────┴─────────────┘${NC}"
    
    # Resumo de status
    echo ""
    echo -e "${WHITE}📊 RESUMO: ${GREEN}${STATUS_ONLINE} $online_services Online  ${YELLOW}${STATUS_DEGRADED} $degraded_services Degradado  ${RED}${STATUS_OFFLINE} $offline_services Offline${NC}"
    
    local total_failures=0
    for container_name in "${!FAILURE_COUNT[@]}"; do
        ((total_failures += FAILURE_COUNT["$container_name"]))
    done
    
    if [[ $total_failures -gt 0 ]]; then
        echo -e "${YELLOW}⚠️  Total de falhas acumuladas: $total_failures${NC}"
    else
        echo -e "${GREEN}⚠️  Total de falhas acumuladas: $total_failures${NC}"
    fi
    
    echo ""
    echo -e "${CYAN}💡 Pressione Ctrl+C para parar o monitoramento${NC}"
    echo -e "${GRAY}═══════════════════════════════════════════════════════════════════════════════════════════${NC}"
}

# Função principal de monitoramento
start_monitoring() {
    write_log "Iniciando monitoramento da stack SWAIF" "INFO"
    
    echo -e "${GREEN}🚀 Iniciando monitoramento contínuo da Stack Docker SWAIF...${NC}"
    echo -e "${CYAN}   Atualizações a cada $REFRESH_INTERVAL segundos${NC}"
    echo ""
    
    # Inicializar contadores de falhas
    for container_name in "${!SERVICES[@]}"; do
        FAILURE_COUNT["$container_name"]=0
    done
    
    # Trap para capturar Ctrl+C
    trap 'echo -e "\n${YELLOW}🛑 Monitoramento interrompido pelo usuário${NC}"; write_log "Monitoramento interrompido pelo usuário" "INFO"; exit 0' INT
    
    while true; do
        show_dashboard
        sleep "$REFRESH_INTERVAL"
    done
}

# Verificar se curl está disponível
if ! command -v curl &> /dev/null; then
    echo -e "${YELLOW}⚠️ Aviso: curl não encontrado. Verificação de serviços web pode ser limitada.${NC}"
    echo ""
fi

# Executar monitoramento
start_monitoring
