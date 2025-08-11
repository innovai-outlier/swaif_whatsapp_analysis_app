[2025-08-09 21:42:30] [INFO] Iniciando stack Docker coordenada...
# Stack Docker - Log de Deployment

**Data/Hora:** 2025-08-09 21:42:30

**Projeto:** SWAIF WhatsApp Bundle Docker Coordenado

[2025-08-09 21:42:30] [INFO] Subindo Redis Shared...

## Redis Shared


---

[2025-08-09 21:42:36] [INFO] Log detalhado do Redis Shared salvo em: C:\Users\dmene\Downloads\docker_bundle_coordinated\docker_coordinated\redis_shared\logs\deployment_2025-08-09_21-42-30.md
[2025-08-09 21:42:36] [INFO] Subindo EVO API...

## EVO API


---

[2025-08-09 21:42:37] [INFO] Log detalhado do EVO API salvo em: C:\Users\dmene\Downloads\docker_bundle_coordinated\docker_coordinated\evo_api\logs\deployment_2025-08-09_21-42-30.md
[2025-08-09 21:42:37] [INFO] Subindo n8n Workflow...

## n8n Workflow


---

[2025-08-09 21:42:45] [INFO] Log detalhado do n8n Workflow salvo em: C:\Users\dmene\Downloads\docker_bundle_coordinated\docker_coordinated\n8n\logs\deployment_2025-08-09_21-42-30.md
[2025-08-09 21:42:45] [INFO] Subindo SWAIF WAB Streamlit...

## SWAIF WAB Streamlit


---

[2025-08-09 21:42:52] [INFO] Log detalhado do SWAIF WAB Streamlit salvo em: C:\Users\dmene\Downloads\docker_bundle_coordinated\docker_coordinated\swaif_wab_streamlit\logs\deployment_2025-08-09_21-42-30.md
[2025-08-09 21:42:52] [SUCCESS] Todos os serviços foram processados!
[2025-08-09 21:42:52] [INFO] Tempo total de execução: 22.1619671 segundos

## Resumo Final

**Tempo de execução:** 22.1619671 segundos

[2025-08-09 21:42:52] [INFO] Containers rodando:
### Containers Ativos
```
CONTAINER ID   IMAGE                COMMAND                  CREATED          STATUS                    PORTS                    NAMES
6952f5740f48   n8nio/n8n:latest     "tini -- /docker-ent�Ǫ"   7 minutes ago    Up 7 minutes (healthy)    0.0.0.0:5678->5678/tcp   swaif_n8n
4dcf167ca6ab   postgres:15-alpine   "docker-entrypoint.s�Ǫ"   7 minutes ago    Up 7 minutes (healthy)    0.0.0.0:5434->5432/tcp   swaif_postgres_n8n
f135b3fdf905   redis:alpine         "docker-entrypoint.s�Ǫ"   7 minutes ago    Up 7 minutes (healthy)    0.0.0.0:6381->6379/tcp   swaif_redis_n8n
b4e926e61323   postgres:15-alpine   "docker-entrypoint.s�Ǫ"   15 minutes ago   Up 15 minutes (healthy)   0.0.0.0:5435->5432/tcp   swaif_postgres
f243a18ad12f   redis:alpine         "docker-entrypoint.s�Ǫ"   16 minutes ago   Up 16 minutes (healthy)   0.0.0.0:6379->6379/tcp   swaif_redis
```
[2025-08-09 21:42:52] [INFO] Log principal salvo em: logs\stack_deployment_2025-08-09_21-42-30.md
[2025-08-09 21:42:52] [INFO] Logs detalhados de cada serviço estão em suas respectivas pastas logs/
