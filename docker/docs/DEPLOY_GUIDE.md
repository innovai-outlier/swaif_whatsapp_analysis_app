# Guia de Deploy Coordenado — SWAIF WhatsApp (Evolution API + n8n + SWAIF)
Siga os passos para subir, testar e monitorar a stack em sequência.

1) Crie a rede: `docker network create swaif_net`
2) Ajuste os `.env` conforme os `.env.example`
3) Suba cada pasta na ordem: `evo_api` → `n8n` → `swaif_wab_streamlit`
- healthchecks, URLs e validações estão descritos em cada compose.
