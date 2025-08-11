[2025-08-09 21:41:07] [INFO] Iniciando stack Docker coordenada...
# Stack Docker - Log de Deployment

**Data/Hora:** 2025-08-09 21:41:07

**Projeto:** SWAIF WhatsApp Bundle Docker Coordenado

[2025-08-09 21:41:07] [INFO] Subindo Redis Shared...

## Redis Shared


---

[2025-08-09 21:41:14] [INFO] Log detalhado do Redis Shared salvo em: redis_shared\logs\deployment_2025-08-09_21-41-07.md
[2025-08-09 21:41:14] [INFO] Subindo EVO API...

## EVO API


---

[2025-08-09 21:41:15] [INFO] Log detalhado do EVO API salvo em: evo_api\logs\deployment_2025-08-09_21-41-07.md
[2025-08-09 21:41:15] [INFO] Subindo n8n Workflow...

## n8n Workflow


---

[2025-08-09 21:41:24] [INFO] Log detalhado do n8n Workflow salvo em: n8n\logs\deployment_2025-08-09_21-41-07.md
[2025-08-09 21:41:24] [INFO] Subindo SWAIF WAB Streamlit...

## SWAIF WAB Streamlit


---

[2025-08-09 21:41:31] [INFO] Log detalhado do SWAIF WAB Streamlit salvo em: swaif_wab_streamlit\logs\deployment_2025-08-09_21-41-07.md
[2025-08-09 21:41:31] [SUCCESS] Todos os serviços foram processados!
[2025-08-09 21:41:31] [INFO] Tempo total de execução: 24.1125237 segundos

## Resumo Final

**Tempo de execução:** 24.1125237 segundos

[2025-08-09 21:41:31] [INFO] Containers rodando:
### Containers Ativos
```
CONTAINER ID   IMAGE                COMMAND                  CREATED          STATUS                    PORTS                    NAMES
6952f5740f48   n8nio/n8n:latest     "tini -- /docker-ent�Ǫ"   6 minutes ago    Up 5 minutes (healthy)    0.0.0.0:5678->5678/tcp   swaif_n8n
4dcf167ca6ab   postgres:15-alpine   "docker-entrypoint.s�Ǫ"   6 minutes ago    Up 5 minutes (healthy)    0.0.0.0:5434->5432/tcp   swaif_postgres_n8n
f135b3fdf905   redis:alpine         "docker-entrypoint.s�Ǫ"   6 minutes ago    Up 5 minutes (healthy)    0.0.0.0:6381->6379/tcp   swaif_redis_n8n
b4e926e61323   postgres:15-alpine   "docker-entrypoint.s�Ǫ"   14 minutes ago   Up 14 minutes (healthy)   0.0.0.0:5435->5432/tcp   swaif_postgres
f243a18ad12f   redis:alpine         "docker-entrypoint.s�Ǫ"   14 minutes ago   Up 14 minutes (healthy)   0.0.0.0:6379->6379/tcp   swaif_redis
```
[2025-08-09 21:41:32] [INFO] Log principal salvo em: logs\stack_deployment_2025-08-09_21-41-07.md
[2025-08-09 21:41:32] [INFO] Logs detalhados de cada serviço estão em suas respectivas pastas logs/
