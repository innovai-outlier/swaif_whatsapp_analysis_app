# SWAIF WhatsApp — Bundle Docker Coordenado

Este projeto utiliza uma stack coordenada de containers Docker para o aplicativo `swaif_whatsapp_app`. A stack é composta pelos seguintes serviços principais:

- **evo_api**: API principal do sistema
- **n8n**: Plataforma de automação de workflows
- **redis_shared**: Banco de dados Redis compartilhado entre os serviços
- **swaif_wab_streamlit**: Interface web para monitoramento e controle

## 📁 Estrutura Organizada

```
docker_coordinated/
├── 🚀 main.ps1              # Gerenciador principal (RECOMENDADO)
├── 🚀 deploy.ps1            # Script principal de deploy
├── 📊 monitor.ps1           # Script principal de monitoramento  
├── 🌐 web.ps1               # Script principal de acesso web
├── 🛑 stop.ps1              # Script principal de parada
├── 📚 docs/                 # Documentação
│   ├── guides/              # Guias de uso
│   │   ├── QUICK_START.md   # Guia rápido
│   │   └── SCRIPTS_GUIDE.md # Guia completo
│   └── DEPLOY_GUIDE.md      # Guia de deploy
├── 🔧 scripts/              # Scripts organizados
│   ├── deploy/              # Scripts de deploy/parada
│   ├── monitor/             # Scripts de monitoramento
│   └── web/                 # Scripts de acesso web
├── 🐳 services/             # Serviços Docker
│   ├── redis_shared/        # Redis compartilhado
│   ├── evo_api/            # API Evolution
│   ├── n8n/                # Workflow n8n
│   └── swaif_wab_streamlit/ # Interface Streamlit
└── 📝 logs/                # Logs de execução
```

## 🚀 Início Rápido (Novo - Recomendado)

### Método Unificado
```powershell
# Gerenciador principal com menu interativo
.\main.ps1

# Ou use diretamente:
.\main.ps1 -Action deploy    # Deploy
.\main.ps1 -Action web       # Acesso web
.\main.ps1 -Action monitor   # Monitoramento
.\main.ps1 -Action stop      # Parar stack
```

### Método Individual (Scripts principais)
```powershell
.\deploy.ps1    # Subir a stack
.\web.ps1       # Acessar serviços web
.\monitor.ps1   # Monitorar stack
.\stop.ps1      # Parar a stack
```

## Scripts Disponíveis

### 🌟 Script Principal (Recomendado)
- **PowerShell**: `main.ps1` - Gerenciador unificado com menu interativo

### Scripts Individuais  
- **PowerShell**: `deploy.ps1` - Deploy da stack
- **PowerShell**: `web.ps1` - Acesso rápido aos serviços web
- **PowerShell**: `monitor.ps1` - Monitoramento em tempo real
- **PowerShell**: `stop.ps1` - Parada da stack

### Scripts Organizados (pasta scripts/)
- **Deploy**: `scripts/deploy/` - Scripts de deploy para múltiplas plataformas
- **Monitor**: `scripts/monitor/` - Scripts de monitoramento avançado
- **Web**: `scripts/web/` - Scripts de acesso web e launchers

## 🌐 Acesso Rápido aos Serviços Web

### Principais Interfaces
- 🚀 **[Streamlit App](http://localhost:8501)** - Interface principal do SWAIF WhatsApp
- ⚙️ **[n8n Workflow](http://localhost:5678)** - Automação e workflows  
- 📱 **[Evolution API](http://localhost:8080)** - API do WhatsApp Evolution

### Como Acessar
1. **Via Gerenciador Principal** (🌟 **MAIS FÁCIL**):
   ```powershell
   .\main.ps1
   # Menu interativo completo
   ```

2. **Via Script Web Direto**:
   ```powershell
   .\web.ps1
   # Menu interativo - digite 1, 2 ou 3 para abrir no browser
   ```

3. **Acesso Direto**:
   - Clique nos links acima (se estiver visualizando no VS Code/GitHub)
   - Ou copie as URLs para seu browser

4. **Via PowerShell**:
   ```powershell
   # Exemplos de abertura direta
   Start-Process "http://localhost:8501"  # Streamlit
   Start-Process "http://localhost:5678"  # n8n
   Start-Process "http://localhost:8080"  # Evolution
   ```

## Como Usar

### Método Automatizado (Recomendado)

#### Windows PowerShell
```powershell
# NOVO - Gerenciador unificado (RECOMENDADO)
.\main.ps1

# Ou use os scripts individuais:
.\deploy.ps1              # Subir a stack
.\web.ps1                 # Acesso rápido aos serviços web
.\monitor.ps1             # Monitor em tempo real
.\stop.ps1                # Parar a stack
```

#### Windows CMD
```cmd
REM Subir a stack
start_stack.cmd

REM Monitorar a stack
monitor_stack.cmd
```

#### Linux/macOS Bash
```bash
# Tornar executável
chmod +x start_stack.sh monitor_stack.sh

# Subir a stack
./start_stack.sh

# Monitorar a stack (dashboard em tempo real)
./monitor_stack.sh
```

### Funcionalidades dos Scripts

#### Scripts de Deploy (`start_stack.*`)
- ✅ Subir cada serviço em ordem correta
- 📝 Gerar logs detalhados de cada etapa (50 linhas de sucesso, 100 linhas de erro)
- 🔍 Mostrar o status final de todos os containers
- 📁 Salvar logs organizados na pasta `logs/` de cada serviço
- 🏥 Verificação de saúde dos containers

#### Scripts de Monitoramento (`monitor_stack.*`)

**Dashboard em Tempo Real:**
- ✅ Status visual com semáforos (🟢 Verde, 🟡 Amarelo, 🔴 Vermelho)
- ⏱️ Tempo de resposta de cada serviço
- 📊 Contador de falhas acumuladas
- 🔗 URLs e endpoints de cada serviço
- ⏰ Tempo de conexão ativa (uptime)
- 📝 Log automático de eventos

**Indicadores de Status:**
- 🟢 **Verde (ONLINE)**: Serviço funcionando perfeitamente
- 🟡 **Amarelo (DEGRADADO)**: Container rodando mas com problemas de conectividade
- 🔴 **Vermelho (OFFLINE)**: Container parado ou com falha crítica

**Serviços Monitorados:**
- Redis Shared (localhost:6379)
- PostgreSQL EVO (localhost:5433)
- Redis EVO (localhost:6380)
- n8n Workflow (http://localhost:5678)
- PostgreSQL n8n (localhost:5434)
- Redis n8n (localhost:6381)
- PostgreSQL Streamlit (localhost:5435)
- Streamlit App (http://localhost:8501)

### Método Manual

Se preferir subir cada serviço manualmente:

```bash
# 1. Subir Redis compartilhado
cd redis_shared
docker-compose up -d

# 2. Subir EVO API
cd ../evo_api
docker-compose up -d

# 3. Subir n8n
cd ../n8n
docker-compose up -d

# 4. Subir Streamlit
cd ../swaif_wab_streamlit
docker-compose up -d
```

## 🌐 URLs e Interfaces Web

### 🎯 Serviços Principais
| Serviço | URL | Descrição | Status |
|---------|-----|-----------|---------|
| **Streamlit App** | [http://localhost:8501](http://localhost:8501) | Interface principal do SWAIF | 🚀 Principal |
| **n8n Workflow** | [http://localhost:5678](http://localhost:5678) | Automação e workflows | ⚙️ Automação |
| **Evolution API** | [http://localhost:8080](http://localhost:8080) | API do WhatsApp | 📱 WhatsApp |

### 💡 Dica de Acesso Rápido
Use o monitor interativo para abrir os serviços automaticamente:
```powershell
.\monitor_interactive.ps1
# Pressione 1, 2 ou 3 para abrir no browser
```

## Portas e Acessos

### Interfaces Web
- **n8n Workflow**: http://localhost:5678
- **Streamlit App**: http://localhost:8501

### Bancos de Dados
- **Redis Shared**: localhost:6379
- **PostgreSQL EVO**: localhost:5433
- **Redis EVO**: localhost:6380
- **PostgreSQL n8n**: localhost:5434
- **Redis n8n**: localhost:6381
- **PostgreSQL Streamlit**: localhost:5435

## Usuários e Credenciais

### PostgreSQL (Todos os bancos)
- **Usuário**: `swaif_user`
- **Senha**: `swaif_password_secure_2024`

### Redis (Todos os bancos)
- **Senha**: `swaif_redis_password_2024`

### n8n
- **Interface**: http://localhost:5678
- Configuração inicial necessária no primeiro acesso

## Logs e Monitoramento

Todos os scripts geram logs detalhados na pasta `logs/`:
- **Deploy**: `stack_deployment_timestamp.md`
- **Monitor**: `monitor_yyyy-mm-dd.log`
- **Shutdown**: `stack_shutdown_timestamp.md`
- **Por serviço**: `[service]/logs/deployment_timestamp.md`

Para mais detalhes sobre deploy, consulte `docs/DEPLOY_GUIDE.md`.
