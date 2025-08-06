# SWAI Features - Sistema Liga/Desliga
# Filosofia: Cada funcionalidade pode ser ativada/desativada conforme necessidade

"""
Sistema de controle de funcionalidades SWAI
Baseado no princípio da simplicidade progressiva
"""

# Configuração principal de funcionalidades
FEATURES = {
    # Core Features (Sempre disponíveis no MVP)
    "dashboard": True,              # Dashboard principal
    "analysis": True,               # Análise básica de conversas
    "cost_calculator": True,        # Calculadora de custo de oportunidade
    "configuration": True,          # Configurações básicas
    
    # Advanced Features (Podem ser desabilitadas para simplificar)
    "smart_summaries": False,       # Resumos inteligentes com IA
    "advanced_charts": True,        # Gráficos avançados
    "export_data": True,           # Exportação de dados
    "real_time_analysis": False,   # Análise em tempo real
    
    # Future Features (Para versões futuras)
    "api_mode": False,             # Modo API REST
    "whatsapp_integration": False, # Integração direta WhatsApp
    "ai_insights": False,          # Insights com IA generativa
    "multi_user": False,           # Múltiplos usuários
    "database_mode": False,        # Persistência em banco
    
    # Debug Features
    "debug_mode": False,           # Modo debug/desenvolvimento
    "performance_metrics": False,  # Métricas de performance
    "error_tracking": True,        # Rastreamento de erros
}

def feature_enabled(feature_name: str) -> bool:
    """
    Verifica se uma funcionalidade está habilitada
    
    Args:
        feature_name (str): Nome da funcionalidade
        
    Returns:
        bool: True se habilitada, False caso contrário
    """
    return FEATURES.get(feature_name, False)

def toggle_feature(feature_name: str, enabled: bool = None) -> bool:
    """
    Liga/desliga uma funcionalidade ou alterna seu estado
    
    Args:
        feature_name (str): Nome da funcionalidade
        enabled (bool, optional): True para ligar, False para desligar, None para alternar
        
    Returns:
        bool: Novo estado da funcionalidade
    """
    if feature_name not in FEATURES:
        raise ValueError(f"Funcionalidade '{feature_name}' não existe")
    
    if enabled is None:
        # Alternar estado atual
        FEATURES[feature_name] = not FEATURES[feature_name]
    else:
        FEATURES[feature_name] = enabled
    
    return FEATURES[feature_name]

def get_enabled_features() -> list:
    """
    Retorna lista de funcionalidades habilitadas
    
    Returns:
        list: Lista com nomes das funcionalidades ativas
    """
    return [name for name, enabled in FEATURES.items() if enabled]

def get_disabled_features() -> list:
    """
    Retorna lista de funcionalidades desabilitadas
    
    Returns:
        list: Lista com nomes das funcionalidades inativas
    """
    return [name for name, enabled in FEATURES.items() if not enabled]

def feature_count() -> dict:
    """
    Retorna contagem de funcionalidades por status
    
    Returns:
        dict: Dicionário com contadores
    """
    enabled = len(get_enabled_features())
    disabled = len(get_disabled_features())
    total = len(FEATURES)
    
    return {
        "enabled": enabled,
        "disabled": disabled,
        "total": total,
        "percentage_enabled": (enabled / total) * 100 if total > 0 else 0
    }

# Configurações de funcionalidades específicas
FEATURE_CONFIG = {
    "dashboard": {
        "title": "Dashboard Principal",
        "description": "Visão geral das métricas e indicadores",
        "icon": "📊",
        "priority": 1,
        "requires": []
    },
    
    "analysis": {
        "title": "Análise de Conversas",
        "description": "Análise detalhada das mensagens do WhatsApp",
        "icon": "🔍",
        "priority": 2,
        "requires": []
    },
    
    "cost_calculator": {
        "title": "Custo de Oportunidade",
        "description": "Cálculo do impacto financeiro",
        "icon": "💰",
        "priority": 3,
        "requires": ["analysis"]
    },
    
    "configuration": {
        "title": "Configurações",
        "description": "Configurações do sistema e parâmetros",
        "icon": "⚙️",
        "priority": 99,
        "requires": []
    },
    
    "smart_summaries": {
        "title": "Resumos Inteligentes",
        "description": "Resumos automáticos das conversas",
        "icon": "📝",
        "priority": 4,
        "requires": ["analysis"]
    },
    
    "advanced_charts": {
        "title": "Gráficos Avançados",
        "description": "Visualizações detalhadas e interativas",
        "icon": "📈",
        "priority": 5,
        "requires": ["analysis"]
    }
}

def get_feature_info(feature_name: str) -> dict:
    """
    Retorna informações sobre uma funcionalidade
    
    Args:
        feature_name (str): Nome da funcionalidade
        
    Returns:
        dict: Informações da funcionalidade
    """
    return FEATURE_CONFIG.get(feature_name, {
        "title": feature_name.replace("_", " ").title(),
        "description": "Funcionalidade sem descrição",
        "icon": "🔧",
        "priority": 50,
        "requires": []
    })

def validate_dependencies() -> dict:
    """
    Valida dependências entre funcionalidades
    
    Returns:
        dict: Resultado da validação
    """
    issues = []
    
    for feature_name, enabled in FEATURES.items():
        if enabled:
            feature_info = get_feature_info(feature_name)
            requires = feature_info.get("requires", [])
            
            for dependency in requires:
                if not FEATURES.get(dependency, False):
                    issues.append({
                        "feature": feature_name,
                        "missing_dependency": dependency,
                        "message": f"'{feature_name}' requer '{dependency}' mas está desabilitada"
                    })
    
    return {
        "valid": len(issues) == 0,
        "issues": issues
    }

# Estado simplificado para MVP
def enable_mvp_mode():
    """Habilita apenas funcionalidades essenciais para MVP"""
    global FEATURES
    
    mvp_features = [
        "dashboard",
        "analysis", 
        "cost_calculator",
        "configuration",
        "advanced_charts",
        "export_data",
        "error_tracking"
    ]
    
    for feature in FEATURES.keys():
        FEATURES[feature] = feature in mvp_features

def enable_full_mode():
    """Habilita todas as funcionalidades disponíveis"""
    global FEATURES
    
    for feature in FEATURES.keys():
        if feature not in ["api_mode", "whatsapp_integration", "multi_user", "database_mode"]:
            FEATURES[feature] = True

def enable_demo_mode():
    """Modo demo com funcionalidades limitadas"""
    global FEATURES
    
    demo_features = ["dashboard", "analysis", "configuration"]
    
    for feature in FEATURES.keys():
        FEATURES[feature] = feature in demo_features

# Inicialização - garantir modo MVP por padrão
if __name__ == "__main__":
    enable_mvp_mode()
    print("🎯 SWAI Features - MVP Mode Enabled")
    print(f"✅ {len(get_enabled_features())} funcionalidades habilitadas")
    print(f"⏸️ {len(get_disabled_features())} funcionalidades desabilitadas")
