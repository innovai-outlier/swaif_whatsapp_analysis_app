# SWAI Settings - Configurações Centralizadas
# Baseado na filosofia SWAI: simplicidade, elegância e propósito

"""
Configurações centralizadas do SWAI WhatsApp Analyzer
Inspirado nos princípios de Senna (perfeição técnica) e Stark (inovação responsável)
"""

import os
from pathlib import Path

# Caminhos base
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

# Configurações visuais (inspiradas na filosofia clássica)
SWAI_SETTINGS = {
    # Cores - Paleta SWAI (inspirada no cosmos e na terra)
    "PRIMARY_COLOR": "#0A1128",     # Azul cósmico (profundidade do conhecimento)
    "SECONDARY_COLOR": "#FF7F11",   # Laranja energético (força vital)
    "SUCCESS_COLOR": "#28a745",     # Verde da natureza (crescimento)
    "WARNING_COLOR": "#ffc107",     # Amarelo do sol (atenção)
    "ERROR_COLOR": "#dc3545",       # Vermelho do fogo (urgência)
    "INFO_COLOR": "#17a2b8",        # Azul água (informação)
    
    # Configurações de negócio
    "VALOR_MEDIO_CONSULTA": 800.0,
    "LEADS_DIARIOS": 5,
    "DIAS_UTEIS_MES": 20,
    "DIAS_UTEIS_ANO": 240,
    
    # Caminhos de arquivos
    "LOGO_PATH": str(ASSETS_DIR / "image.png"),
    "SUCCESS_CASES_DIR": str(DATA_DIR / "success_cases"),
    "FAIL_CASES_DIR": str(DATA_DIR / "fail_cases"),
    "FEATURES_CSV": str(DATA_DIR / "extracted_features_enhanced.csv"),
    "ANALYSIS_JSON": str(DATA_DIR / "detailed_analysis_results.json"),
    
    # Configurações de UI
    "APP_TITLE": "SWAI WhatsApp Analyzer",
    "APP_SUBTITLE": "Libertando o potencial humano através da análise inteligente",
    "PAGE_ICON": "🧠",
    "LAYOUT": "wide",
    
    # Limites e thresholds
    "MIN_CONVERSATION_MESSAGES": 3,
    "MAX_CONVERSATION_DURATION": 1440,  # 24 horas em minutos
    "SUCCESS_RATE_THRESHOLD": 0.6,      # 60% taxa de sucesso ideal
    "COST_ALERT_THRESHOLD": 10000.0,    # R$ 10k alerta de custo alto
    
    # Configurações de análise
    "AGENDAMENTO_KEYWORDS": [
        "agendar", "agenda", "consulta", "horário", "disponibilidade",
        "marcação", "marcar", "quando", "data", "horários"
    ],
    
    "PRECO_KEYWORDS": [
        "preço", "valor", "custo", "quanto", "custa", "cobrar",
        "pagamento", "pagar", "investimento", "valores"
    ],
    
    # Mensagens do sistema
    "MESSAGES": {
        "no_data": "❌ Dados não encontrados. Execute primeiro a extração de features.",
        "data_loaded": "✅ Dados carregados com sucesso!",
        "feature_disabled": "⏸️ Funcionalidade desabilitada",
        "processing": "🔄 Processando dados...",
        "error": "❌ Erro no processamento",
        "success": "✅ Operação realizada com sucesso"
    }
}

def get_setting(key: str, default=None):
    """
    Obtém uma configuração do sistema
    
    Args:
        key (str): Chave da configuração
        default: Valor padrão se não encontrar
        
    Returns:
        Valor da configuração ou padrão
    """
    return SWAI_SETTINGS.get(key, default)

def update_setting(key: str, value):
    """
    Atualiza uma configuração do sistema
    
    Args:
        key (str): Chave da configuração
        value: Novo valor
    """
    SWAI_SETTINGS[key] = value

def get_financial_settings() -> dict:
    """
    Retorna configurações financeiras
    
    Returns:
        dict: Configurações financeiras
    """
    return {
        "valor_consulta": SWAI_SETTINGS["VALOR_MEDIO_CONSULTA"],
        "leads_diarios": SWAI_SETTINGS["LEADS_DIARIOS"],
        "dias_uteis_mes": SWAI_SETTINGS["DIAS_UTEIS_MES"],
        "dias_uteis_ano": SWAI_SETTINGS["DIAS_UTEIS_ANO"]
    }

def update_financial_settings(valor_consulta=None, leads_diarios=None):
    """
    Atualiza configurações financeiras
    
    Args:
        valor_consulta (float, optional): Valor médio da consulta
        leads_diarios (int, optional): Número de leads por dia
    """
    if valor_consulta is not None:
        SWAI_SETTINGS["VALOR_MEDIO_CONSULTA"] = float(valor_consulta)
    
    if leads_diarios is not None:
        SWAI_SETTINGS["LEADS_DIARIOS"] = int(leads_diarios)

def get_color_scheme() -> dict:
    """
    Retorna esquema de cores do SWAI
    
    Returns:
        dict: Cores do sistema
    """
    return {
        "primary": SWAI_SETTINGS["PRIMARY_COLOR"],
        "secondary": SWAI_SETTINGS["SECONDARY_COLOR"],
        "success": SWAI_SETTINGS["SUCCESS_COLOR"],
        "warning": SWAI_SETTINGS["WARNING_COLOR"],
        "error": SWAI_SETTINGS["ERROR_COLOR"],
        "info": SWAI_SETTINGS["INFO_COLOR"]
    }

def ensure_directories():
    """
    Garante que os diretórios necessários existam
    """
    directories = [
        DATA_DIR,
        DATA_DIR / "success_cases",
        DATA_DIR / "fail_cases",
        ASSETS_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Inicialização
if __name__ == "__main__":
    ensure_directories()
    print("🎯 SWAI Settings - Configurações carregadas")
    print(f"📁 Diretório base: {BASE_DIR}")
    print(f"💰 Valor consulta: R$ {SWAI_SETTINGS['VALOR_MEDIO_CONSULTA']}")
    print(f"📊 Leads diários: {SWAI_SETTINGS['LEADS_DIARIOS']}")
