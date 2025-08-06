# SWAI WhatsApp Analyzer - Dockerfile
# Filosofia: Containerização simples e eficiente

FROM python:3.11-slim

# Metadata
LABEL maintainer="SWAI Factory"
LABEL description="SWAI WhatsApp Analyzer - Versão Simplificada"
LABEL version="1.0-MVP"

# Diretório de trabalho
WORKDIR /app

# Variáveis de ambiente
ENV PYTHONPATH=/app
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Instalar dependências do sistema (mínimas)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiar requirements e instalar dependências Python
COPY swai_requirements.txt .
RUN pip install --no-cache-dir -r swai_requirements.txt

# Copiar código da aplicação
COPY swai_*.py ./
COPY README_SWAI.md ./

# Criar estrutura de diretórios
RUN mkdir -p data/success_cases data/fail_cases assets

# Expor porta
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Comando padrão
CMD ["streamlit", "run", "swai_app_main.py", "--server.address", "0.0.0.0"]
