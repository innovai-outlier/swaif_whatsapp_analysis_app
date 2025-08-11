# 🚀 GUIA RÁPIDO - SWAIF Stack

## ⚡ Início Rápido (3 passos)

### 1️⃣ Subir a Stack
```powershell
.\start_stack.ps1
```

### 2️⃣ Acessar os Serviços
```powershell
.\web_launcher.ps1
```

### 3️⃣ Usar as Aplicações
- **Digite 1** → Streamlit App (Interface principal)
- **Digite 2** → n8n Workflow (Automação)  
- **Digite 3** → Evolution API (WhatsApp)

---

## 🌐 URLs Diretas

| Serviço | URL | Função |
|---------|-----|---------|
| 🚀 **Streamlit** | [http://localhost:8501](http://localhost:8501) | Interface principal do SWAIF |
| ⚙️ **n8n** | [http://localhost:5678](http://localhost:5678) | Automação de workflows |
| 📱 **Evolution** | [http://localhost:8080](http://localhost:8080) | API do WhatsApp |

---

## 📋 Scripts Principais

```powershell
# DEPLOY
.\start_stack.ps1          # Subir toda a stack

# ACESSO WEB  
.\web_launcher.ps1         # Menu para abrir serviços (RECOMENDADO)

# MONITORAMENTO
.\monitor_web.ps1          # Dashboard com acesso web
.\monitor_simple.ps1       # Monitor básico

# PARAR
.\stop_stack.ps1           # Parar toda a stack
```

---

## 🆘 Solução Rápida de Problemas

### Serviço não abre?
1. Verificar se a stack está rodando:
   ```powershell
   .\web_launcher.ps1 -Action status -SingleRun
   ```

2. Se offline, subir a stack:
   ```powershell
   .\start_stack.ps1
   ```

### Containers não sobem?
1. Verificar se Docker está rodando
2. Verificar logs:
   ```powershell
   Get-Content logs\stack_deployment_*.md | Select-Object -Last 20
   ```

### Porta ocupada?
1. Verificar processos:
   ```powershell
   netstat -ano | findstr ":8501"  # Para Streamlit
   netstat -ano | findstr ":5678"  # Para n8n
   netstat -ano | findstr ":8080"  # Para Evolution
   ```

---

## 🎯 Fluxo de Trabalho Recomendado

1. **Manhã** → `.\start_stack.ps1` (subir stack)
2. **Trabalho** → `.\web_launcher.ps1` (acessar serviços)
3. **Noite** → `.\stop_stack.ps1` (parar stack - opcional)

---

## 💡 Dicas Profissionais

- 🔗 **Bookmarks**: Salve as URLs nos favoritos do browser
- ⌨️ **Atalhos**: Crie atalhos na área de trabalho para os scripts
- 📊 **Monitor**: Deixe `monitor_web.ps1` rodando em terminal separado
- 🔄 **Auto-start**: Configure `start_stack.ps1` para rodar na inicialização

---

**🎉 Pronto! Sua stack SWAIF está configurada e pronta para uso profissional!**
