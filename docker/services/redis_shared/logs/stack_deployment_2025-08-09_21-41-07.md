### Comando Executado
```
docker-compose up -d
```

### Saída do Comando
```
 Container swaif_redis  Running
```
[2025-08-09 21:41:08] [SUCCESS] Redis Shared iniciado com sucesso!
[2025-08-09 21:41:13] [INFO] Capturando logs detalhados de Redis Shared...

### Logs Recentes (50 linhas)
```
swaif_redis  | 1:C 10 Aug 2025 00:26:37.764 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
swaif_redis  | 1:C 10 Aug 2025 00:26:37.764 * Redis version=8.2.0, bits=64, commit=00000000, modified=1, pid=1, just started
swaif_redis  | 1:C 10 Aug 2025 00:26:37.764 * Configuration loaded
swaif_redis  | 1:M 10 Aug 2025 00:26:37.766 * monotonic clock: POSIX clock_gettime
swaif_redis  | 1:M 10 Aug 2025 00:26:37.772 * Running mode=standalone, port=6379.
swaif_redis  | 1:M 10 Aug 2025 00:26:37.776 * Server initialized
swaif_redis  | 1:M 10 Aug 2025 00:26:37.780 * Ready to accept connections tcp
```

### Status dos Containers
```
NAME          IMAGE          COMMAND                  SERVICE       CREATED          STATUS                    PORTS
swaif_redis   redis:alpine   "docker-entrypoint.s�Ǫ"   swaif_redis   14 minutes ago   Up 14 minutes (healthy)   0.0.0.0:6379->6379/tcp
```
[2025-08-09 21:41:14] [INFO] Verificando saúde dos containers...
