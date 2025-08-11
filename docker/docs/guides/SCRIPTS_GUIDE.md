# SWAIF Docker Stack - Scripts Multiplataforma

Este projeto agora inclui scripts para diferentes sistemas operacionais e shells, facilitando o deploy e monitoramento em qualquer ambiente.

## 📁 Estrutura de Scripts

```
docker_coordinated/
├── start_stack.ps1         # Deploy - PowerShell (Windows)
├── start_stack.cmd         # Deploy - CMD (Windows)
├── start_stack.sh          # Deploy - Bash (Linux/macOS)
├── stop_stack.ps1          # Shutdown - PowerShell (Windows)
├── monitor_stack.ps1       # Monitor Avançado - PowerShell
├── monitor_stack.cmd       # Monitor Básico - CMD
├── monitor_stack.sh        # Monitor Avançado - Bash
└── monitor_simple.ps1      # Monitor Simples - PowerShell
```

## 🚀 Scripts de Deploy

### Windows PowerShell
```powershell
# Subir toda a stack
.\start_stack.ps1

# Parar toda a stack
.\stop_stack.ps1
```

### Windows CMD
```cmd
# Subir toda a stack
start_stack.cmd
```

### Linux/macOS Bash
```bash
# Tornar executável
chmod +x start_stack.sh

# Subir toda a stack
./start_stack.sh
```

## 📊 Scripts de Monitoramento

### Monitor Avançado (PowerShell)
```powershell
# Monitoramento contínuo (padrão - 30s)
.\monitor_stack.ps1

# Monitoramento com intervalo personalizado
.\monitor_stack.ps1 -RefreshInterval 15

# Execução única (snapshot)
.\monitor_stack.ps1 -ContinuousMode:$false
```

### Monitor Simples (PowerShell)
```powershell
# Monitoramento contínuo (padrão - 10s)
.\monitor_simple.ps1

# Execução única
.\monitor_simple.ps1 -SingleRun
```

### Monitor Básico (CMD)
```cmd
# Monitoramento básico
monitor_stack.cmd
```

### Monitor Avançado (Bash)
```bash
# Tornar executável
chmod +x monitor_stack.sh

# Monitoramento contínuo
./monitor_stack.sh
```

## 🎯 Funcionalidades dos Scripts

### Scripts de Deploy
- ✅ **Ordem correta**: Redis → EVO API → n8n → Streamlit
- 📝 **Logs detalhados**: 50 linhas (sucesso) / 100 linhas (erro)
- 📁 **Organização**: Logs salvos em `logs/` de cada serviço
- 🏥 **Health checks**: Verificação de saúde dos containers
- ⏱️ **Timestamps**: Logs com data/hora completa
- 🔍 **Status final**: Resumo de todos os containers

### Scripts de Monitoramento

#### Dashboard Avançado (PowerShell/Bash)
- 🖥️ **Interface rica**: Dashboard colorido com emojis
- 🟢🟡🔴 **Status visual**: Semáforos (Verde/Amarelo/Vermelho)
- ⚡ **Tempo de resposta**: Medição em millisegundos
- 📊 **Estatísticas**: Contador de falhas acumuladas
- 🔗 **URLs**: Endpoints de cada serviço
- ⏰ **Uptime**: Tempo de monitoramento ativo
- 📝 **Logs automáticos**: Eventos salvos automaticamente

#### Monitor Simples (PowerShell)
- 📋 **Tabela limpa**: Status básico dos containers
- 🎯 **Informações essenciais**: Nome, status, porta
- 📈 **Resumo**: Contadores por status
- 🐳 **Lista Docker**: Containers ativos do Docker

## 🌈 Indicadores de Status

### 🟢 Verde (ONLINE)
- Container rodando normalmente
- Portas acessíveis
- Serviços web respondendo (200 OK)

### 🟡 Amarelo (DEGRADADO)  
- Container rodando mas com problemas
- Conectividade limitada
- Serviços web com erros

### 🔴 Vermelho (OFFLINE)
- Container parado
- Serviço não encontrado
- Falha crítica

## 📋 Serviços Monitorados

| Serviço | Container | URL/Endpoint | Tipo |
|---------|-----------|--------------|------|
| Redis Shared | `swaif_redis` | localhost:6379 | Redis |
| PostgreSQL EVO | `postgres_evo` | localhost:5433 | Database |
| Redis EVO | `redis_evo` | localhost:6380 | Redis |
| n8n Workflow | `swaif_n8n` | http://localhost:5678 | Web |
| PostgreSQL n8n | `postgres_n8n` | localhost:5434 | Database |
| Redis n8n | `redis_n8n` | localhost:6381 | Redis |
| PostgreSQL Streamlit | `postgres_streamlit` | localhost:5435 | Database |
| Streamlit App | - | http://localhost:8501 | Web |

## 📂 Sistema de Logs

### Estrutura de Logs
```
logs/
├── stack_deployment_YYYY-MM-DD_HH-MM-SS.md    # Deploy principal
├── stack_shutdown_YYYY-MM-DD_HH-MM-SS.md      # Shutdown
├── monitor_YYYY-MM-DD.log                      # Monitor diário
├── redis_shared/logs/
│   └── deployment_YYYY-MM-DD_HH-MM-SS.md
├── evo_api/logs/
│   └── deployment_YYYY-MM-DD_HH-MM-SS.md
├── n8n/logs/
│   └── deployment_YYYY-MM-DD_HH-MM-SS.md
└── swaif_wab_streamlit/logs/
    └── deployment_YYYY-MM-DD_HH-MM-SS.md
```

### Conteúdo dos Logs
- 📅 **Timestamp**: Data/hora de cada operação
- 💻 **Comandos**: Histórico completo dos comandos executados
- 📤 **Output**: Saída completa do Docker Compose
- 🏥 **Health checks**: Status de saúde dos containers
- ⚠️ **Erros**: Logs detalhados de falhas (100 linhas)
- ✅ **Sucessos**: Logs de operações bem-sucedidas (50 linhas)

## 🔧 Credenciais Padrão

### PostgreSQL (Todos os bancos)
- **Usuário**: `swaif_user`
- **Senha**: `swaif_password_secure_2024`

### Redis (Todos os bancos)
- **Senha**: `swaif_redis_password_2024`

## 💡 Dicas de Uso

### Para Desenvolvimento
```powershell
# Deploy rápido para testes
.\start_stack.ps1

# Monitor simples durante desenvolvimento
.\monitor_simple.ps1 -RefreshInterval 5
```

### Para Produção
```powershell
# Deploy com logs completos
.\start_stack.ps1

# Monitor avançado para produção
.\monitor_stack.ps1 -RefreshInterval 30
```

### Para Troubleshooting
```powershell
# Verificação única do status
.\monitor_simple.ps1 -SingleRun

# Verificar logs específicos
Get-Content logs\stack_deployment_*.md | Select-Object -Last 50
```

## 🆘 Solução de Problemas

### Container não inicia
1. Verificar logs: `logs/[service]/deployment_*.md`
2. Verificar Docker: `docker ps -a`
3. Verificar rede: `docker network ls`

### Serviço degradado
1. Verificar conectividade de porta
2. Verificar logs do container
3. Verificar dependências (PostgreSQL, Redis)

### Monitor não funciona
1. Verificar se Docker está rodando
2. Verificar se containers estão criados
3. Verificar permissões de execução dos scripts

Agora você tem uma stack completa com scripts para todas as plataformas e um sistema robusto de monitoramento! 🎉
