@echo off
REM Script de Monitoramento da Stack Docker SWAIF
REM CMD - Monitor com Dashboard em tempo real

setlocal enabledelayedexpansion

set RefreshInterval=30
set LogFile=logs\monitor_%date:~-4,4%-%date:~-10,2%-%date:~-7,2%.log

REM Criar pasta logs se não existir
if not exist logs mkdir logs

echo [%date% %time%] [INFO] Iniciando monitoramento da stack SWAIF >> %LogFile%

:MainLoop
cls
echo.
echo ===============================================================================
echo                   STACK DOCKER SWAIF - MONITOR DASHBOARD
echo ===============================================================================
echo Horario: %date% %time% ^| Atualizacao: a cada %RefreshInterval% segundos
echo Log: %LogFile%
echo ===============================================================================
echo.

REM Cabeçalho da tabela
echo SERVICO                   URL/ENDPOINT           STATUS        RESP.    FALHAS
echo -------------------------------------------------------------------------------

REM Verificar cada serviço
call :CheckService "swaif_redis" "Redis Shared" "localhost:6379" "redis"
call :CheckService "postgres_evo" "PostgreSQL EVO" "localhost:5433" "database"
call :CheckService "redis_evo" "Redis EVO" "localhost:6380" "redis"
call :CheckService "swaif_n8n" "n8n Workflow" "localhost:5678" "web"
call :CheckService "postgres_n8n" "PostgreSQL n8n" "localhost:5434" "database"
call :CheckService "redis_n8n" "Redis n8n" "localhost:6381" "redis"
call :CheckService "postgres_streamlit" "PostgreSQL Streamlit" "localhost:5435" "database"

echo -------------------------------------------------------------------------------
echo.

REM Mostrar resumo
docker ps --format "table {{.Names}}\t{{.Status}}" | findstr /v "NAMES"
echo.
echo Pressione Ctrl+C para parar o monitoramento...
echo ===============================================================================

timeout /t %RefreshInterval% /nobreak > nul
goto MainLoop

:CheckService
set ContainerName=%~1
set ServiceName=%~2
set ServiceURL=%~3
set ServiceType=%~4

REM Verificar se o container está rodando
docker inspect %ContainerName% > nul 2>&1
if errorlevel 1 (
    echo %ServiceName:~0,25%   %ServiceURL:~0,22%   [OFFLINE]     ---      ---
    echo [%date% %time%] [WARN] Container %ContainerName% nao encontrado >> %LogFile%
    goto :eof
)

REM Verificar status do container
for /f "tokens=*" %%i in ('docker inspect --format="{{.State.Running}}" %ContainerName% 2^>nul') do set IsRunning=%%i

if "%IsRunning%"=="true" (
    REM Container rodando - verificar conectividade
    if "%ServiceType%"=="web" (
        REM Para serviços web, tentar curl (se disponível)
        curl -s -o nul -w "%%{http_code}" http://%ServiceURL% > temp_response.txt 2>nul
        if errorlevel 1 (
            echo %ServiceName:~0,25%   %ServiceURL:~0,22%   [DEGRADADO]   ---      ---
        ) else (
            set /p ResponseCode=<temp_response.txt
            if "!ResponseCode!"=="200" (
                echo %ServiceName:~0,25%   %ServiceURL:~0,22%   [ONLINE]      OK       0
            ) else (
                echo %ServiceName:~0,25%   %ServiceURL:~0,22%   [DEGRADADO]   !ResponseCode!      ---
            )
        )
        del temp_response.txt 2>nul
    ) else (
        REM Para bancos de dados e Redis, verificar se a porta está aberta
        netstat -an | findstr ":%ServiceURL:~-4%" > nul
        if errorlevel 1 (
            echo %ServiceName:~0,25%   %ServiceURL:~0,22%   [DEGRADADO]   ---      ---
        ) else (
            echo %ServiceName:~0,25%   %ServiceURL:~0,22%   [ONLINE]      OK       0
        )
    )
) else (
    echo %ServiceName:~0,25%   %ServiceURL:~0,22%   [OFFLINE]     ---      ---
    echo [%date% %time%] [ERROR] Container %ContainerName% parado >> %LogFile%
)

goto :eof
