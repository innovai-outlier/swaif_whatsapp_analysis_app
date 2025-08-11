# 🚀 SWAIF Stack v2.0 - Sistema Coordenado

> **✨ PROJETO REORGANIZADO!** Leia o [REORGANIZATION.md](REORGANIZATION.md) para ver as mudanças!

## 🎯 Início Rápido

```powershell
# Método principal (RECOMENDADO)
.\manager.ps1

# Ou use diretamente:
.\deploy.ps1    # Subir stack
.\web.ps1       # Acesso web  
.\monitor.ps1   # Monitorar
.\stop.ps1      # Parar stack
```

## 🏗️ Estrutura do Projeto

```
📁 docker_coordinated/
├── 🚀 manager.ps1           # Gerenciador principal
├── 🚀 deploy.ps1            # Deploy da stack
├── 📊 monitor.ps1           # Monitoramento
├── 🌐 web.ps1               # Acesso web
├── 🛑 stop.ps1              # Parar stack
├── 📚 docs/                 # Documentação
├── 🔧 scripts/              # Scripts organizados
├── 🐳 services/             # Serviços Docker
└── 📝 logs/                # Logs centralizados
```

## 🐳 Serviços Incluídos

- **🔧 Redis Shared**: Banco de dados compartilhado (porta 6379)
- **📱 Evolution API**: API WhatsApp (porta 8080)
- **🔄 N8N**: Automação e workflows (porta 5678)  
- **🌐 Streamlit**: Interface principal (porta 8501)

## 📚 Documentação

- **[REORGANIZATION.md](REORGANIZATION.md)**: O que mudou na v2.0
- **[docs/guides/QUICK_START.md](docs/guides/QUICK_START.md)**: Guia rápido
- **[docs/guides/SCRIPTS_GUIDE.md](docs/guides/SCRIPTS_GUIDE.md)**: Guia completo
- **[docs/DEPLOY_GUIDE.md](docs/DEPLOY_GUIDE.md)**: Guia de deploy

## ⚡ Comandos Principais

### Deploy e Status
```powershell
.\deploy.ps1             # Subir toda a stack
.\manager.ps1 status     # Ver status rápido
.\stop.ps1               # Parar toda a stack
```

### Acesso aos Serviços
```powershell
.\web.ps1                # Menu interativo para abrir serviços
# Ou abra diretamente no navegador:
# http://localhost:8501   # Streamlit (Principal)
# http://localhost:8080   # Evolution API
# http://localhost:5678   # N8N
```

### Monitoramento
```powershell
.\monitor.ps1            # Monitor básico
# Ou use monitors avançados em scripts/monitor/
```

## 🔄 Cross-Platform

Além dos scripts PowerShell, também temos versões para:
- **Windows CMD**: `scripts/deploy/start_stack.cmd`
- **Linux/macOS**: `scripts/deploy/start_stack.sh`

## 🎉 Resultado

Seu projeto SWAIF Stack agora está **100% organizado e profissional**!

**Use `.\manager.ps1` para a melhor experiência! 🚀**
