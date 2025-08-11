@echo off
REM Script para subir toda a stack Docker do projeto swaif_whatsapp_app
REM Executa cada etapa e mostra logs de cada serviço

setlocal enabledelayedexpansion

REM Configurar timestamp
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set mydate=%%c-%%a-%%b
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set mytime=%%a-%%b
set timestamp=%mydate%_%mytime%
set timestamp=%timestamp: =%
set timestamp=%timestamp::=-%

set MainLogFile=logs\stack_deployment_%timestamp%.md
set StartTime=%time%

REM Criar pasta logs se não existir
if not exist logs mkdir logs

echo [%date% %time%] [INFO] Iniciando stack Docker coordenada...
echo # Stack Docker - Log de Deployment > %MainLogFile%
echo. >> %MainLogFile%
echo **Data/Hora:** %date% %time% >> %MainLogFile%
echo **Projeto:** SWAIF WhatsApp Bundle Docker Coordenado >> %MainLogFile%
echo. >> %MainLogFile%

call :StartService "redis_shared" "Redis Shared"
call :StartService "evo_api" "EVO API"
call :StartService "n8n" "n8n Workflow"
call :StartService "swaif_wab_streamlit" "SWAIF WAB Streamlit"

set EndTime=%time%
echo [%date% %time%] [SUCCESS] Todos os serviços foram processados!
echo [%date% %time%] [INFO] Log principal salvo em: %MainLogFile%

echo.
echo ## Resumo Final >> %MainLogFile%
echo **Tempo de execução:** Concluído >> %MainLogFile%

echo [%date% %time%] [INFO] Containers rodando:
docker ps
echo. >> %MainLogFile%
echo ### Containers Ativos >> %MainLogFile%
echo ``` >> %MainLogFile%
docker ps >> %MainLogFile%
echo ``` >> %MainLogFile%

goto :eof

:StartService
set ServiceDir=%~1
set ServiceName=%~2

REM Criar pasta logs no diretório do serviço se não existir
if not exist %ServiceDir%\logs mkdir %ServiceDir%\logs

set serviceLogFile=%ServiceDir%\logs\deployment_%timestamp%.md

echo [%date% %time%] [INFO] Subindo %ServiceName%...
echo. >> %MainLogFile%
echo ## %ServiceName% >> %MainLogFile%
echo. >> %MainLogFile%

echo # Deployment Log - %ServiceName% > %serviceLogFile%
echo **Data/Hora:** %date% %time% >> %serviceLogFile%
echo. >> %serviceLogFile%

pushd %ServiceDir%

echo Executando docker-compose up -d em %ServiceDir%...
docker-compose up -d > temp_output.txt 2>&1
set exitCode=%errorlevel%

REM Log no arquivo principal
echo ### Comando Executado >> %MainLogFile%
echo ``` >> %MainLogFile%
echo docker-compose up -d >> %MainLogFile%
echo ``` >> %MainLogFile%
echo. >> %MainLogFile%
echo ### Saída do Comando >> %MainLogFile%
echo ``` >> %MainLogFile%
type temp_output.txt >> %MainLogFile%
echo ``` >> %MainLogFile%

REM Log no arquivo do serviço
echo ## Comando Executado >> %serviceLogFile%
echo ```bash >> %serviceLogFile%
echo docker-compose up -d >> %serviceLogFile%
echo ``` >> %serviceLogFile%
echo. >> %serviceLogFile%
echo ## Saída do Comando >> %serviceLogFile%
echo ``` >> %serviceLogFile%
type temp_output.txt >> %serviceLogFile%
echo ``` >> %serviceLogFile%

if %exitCode%==0 (
    echo [%date% %time%] [SUCCESS] %ServiceName% iniciado com sucesso!
    
    REM Aguardar um pouco para os containers estabilizarem
    timeout /t 5 /nobreak > nul
    
    REM Mostrar logs recentes
    echo [%date% %time%] [INFO] Capturando logs detalhados de %ServiceName%...
    docker-compose logs --tail 50 > temp_logs.txt 2>&1
    echo. >> %MainLogFile%
    echo ### Logs Recentes (50 linhas) >> %MainLogFile%
    echo ``` >> %MainLogFile%
    type temp_logs.txt >> %MainLogFile%
    echo ``` >> %MainLogFile%
    
    echo. >> %serviceLogFile%
    echo ## Logs Recentes (50 linhas) >> %serviceLogFile%
    echo ``` >> %serviceLogFile%
    type temp_logs.txt >> %serviceLogFile%
    echo ``` >> %serviceLogFile%
    
    REM Verificar status dos containers
    docker-compose ps > temp_status.txt 2>&1
    echo. >> %MainLogFile%
    echo ### Status dos Containers >> %MainLogFile%
    echo ``` >> %MainLogFile%
    type temp_status.txt >> %MainLogFile%
    echo ``` >> %MainLogFile%
    
    echo. >> %serviceLogFile%
    echo ## Status dos Containers >> %serviceLogFile%
    echo ``` >> %serviceLogFile%
    type temp_status.txt >> %serviceLogFile%
    echo ``` >> %serviceLogFile%
    
    REM Limpar arquivos temporários
    del temp_logs.txt temp_status.txt
) else (
    echo [%date% %time%] [ERROR] Erro ao iniciar %ServiceName%!
    
    REM Capturar logs de erro mais detalhados
    echo [%date% %time%] [WARN] Capturando logs de erro detalhados...
    docker-compose logs --tail 100 > temp_error_logs.txt 2>&1
    echo. >> %MainLogFile%
    echo ### LOGS DE ERRO (100 linhas) >> %MainLogFile%
    echo ``` >> %MainLogFile%
    type temp_error_logs.txt >> %MainLogFile%
    echo ``` >> %MainLogFile%
    
    echo. >> %serviceLogFile%
    echo ## LOGS DE ERRO (100 linhas) >> %serviceLogFile%
    echo ``` >> %serviceLogFile%
    type temp_error_logs.txt >> %serviceLogFile%
    echo ``` >> %serviceLogFile%
    
    REM Containers com falha
    docker-compose ps --all > temp_failed.txt 2>&1
    echo. >> %serviceLogFile%
    echo ## Containers com Falha >> %serviceLogFile%
    echo ``` >> %serviceLogFile%
    type temp_failed.txt >> %serviceLogFile%
    echo ``` >> %serviceLogFile%
    
    REM Limpar arquivos temporários
    del temp_error_logs.txt temp_failed.txt
)

del temp_output.txt
popd
echo. >> %MainLogFile%
echo --- >> %MainLogFile%
echo. >> %MainLogFile%
echo [%date% %time%] [INFO] Log detalhado do %ServiceName% salvo em: %serviceLogFile%

goto :eof
