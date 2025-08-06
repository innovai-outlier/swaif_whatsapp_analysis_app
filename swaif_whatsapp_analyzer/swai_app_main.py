# SWAI WhatsApp Analyzer - Versão Simplificada
# Baseado na filosofia SWAI Factory: Tecnologia como libertação

import streamlit as st
import sys
import os
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="SWAI WhatsApp Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Adicionar paths para importações
sys.path.append(str(Path(__file__).parent))

# Importações locais
try:
    from swai_features import FEATURES, feature_enabled
    from swai_settings import SWAI_SETTINGS
    from swai_ui_dashboard import show_dashboard
    from swai_ui_analysis import show_analysis
    from swai_ui_cost import show_cost_calculator
    from swai_ui_config import show_configuration
except ImportError as e:
    st.error(f"❌ Erro na importação de módulos: {e}")
    st.info("Verifique se todos os arquivos SWAI estão presentes no diretório.")
    st.stop()

# CSS Global SWAI
st.markdown(f"""
<style>
    /* SWAI Theme - Inspirado na filosofia clássica */
    .main-header {{
        background: linear-gradient(135deg, {SWAI_SETTINGS['PRIMARY_COLOR']} 0%, {SWAI_SETTINGS['SECONDARY_COLOR']} 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    
    .main-header h1 {{
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }}
    
    .main-header p {{
        color: white;
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }}
    
    .feature-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid {SWAI_SETTINGS['SECONDARY_COLOR']};
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    .feature-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    
    .swai-metric {{
        background: linear-gradient(45deg, #f8f9fa, #ffffff);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        text-align: center;
    }}
    
    .sidebar .sidebar-content {{
        background: linear-gradient(180deg, {SWAI_SETTINGS['PRIMARY_COLOR']} 0%, #1a2332 100%);
    }}
    
    /* Filosofia visual: simplicidade elegante */
    .stSelectbox > div > div {{
        background-color: white;
        border-radius: 8px;
    }}
    
    /* Footer SWAI */
    .swai-footer {{
        background: {SWAI_SETTINGS['PRIMARY_COLOR']};
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-top: 2rem;
    }}
</style>
""", unsafe_allow_html=True)

def main():
    """Aplicativo principal SWAI WhatsApp Analyzer"""
    
    # Header principal
    st.markdown(f"""
    <div class="main-header">
        <h1>🧠 SWAI WhatsApp Analyzer</h1>
        <p>Libertando o potencial humano através da análise inteligente</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar de navegação
    with st.sidebar:
        # Logo e branding
        logo_path = SWAI_SETTINGS.get('LOGO_PATH', 'assets/image.png')
        if Path(logo_path).exists():
            st.image(logo_path, width=80)
        else:
            st.markdown("🧠")
        
        st.markdown("---")
        
        st.markdown("### 🧭 Navegação SWAI")
        
        # Menu principal com funcionalidades liga-desliga
        pages = {}
        
        if feature_enabled("dashboard"):
            pages["📊 Dashboard"] = "dashboard"
            
        if feature_enabled("analysis"):
            pages["🔍 Análise de Conversas"] = "analysis"
            
        if feature_enabled("cost_calculator"):
            pages["💰 Custo de Oportunidade"] = "cost"
            
        if feature_enabled("configuration"):
            pages["⚙️ Configurações"] = "config"
        
        # Seleção de página
        if pages:
            selected_page = st.selectbox(
                "Escolha uma funcionalidade:",
                list(pages.keys()),
                key="page_selector"
            )
            page_key = pages.get(selected_page, "dashboard")
        else:
            st.error("❌ Nenhuma funcionalidade habilitada!")
            st.info("Ative pelo menos uma funcionalidade nas configurações.")
            page_key = "config"  # Forçar ir para configurações
        
        # Status das funcionalidades
        st.markdown("---")
        st.markdown("### 🎛️ Status das Funcionalidades")
        
        feature_status = {
            "dashboard": "📊 Dashboard",
            "analysis": "🔍 Análise",
            "cost_calculator": "💰 Custo",
            "configuration": "⚙️ Config"
        }
        
        for feature, label in feature_status.items():
            if feature_enabled(feature):
                st.success(f"✅ {label}")
            else:
                st.warning(f"⏸️ {label}")
        
        # Filosofia SWAI
        st.markdown("---")
        st.markdown("### 💭 Filosofia SWAI")
        
        st.markdown("""
        > *"Não é que temos pouco tempo, mas sim que desperdiçamos muito dele"* - Sêneca
        
        **Princípios:**
        - 🎯 Tecnologia como libertação
        - 🤝 Preservação da dignidade humana  
        - ⚡ Eficiência com propósito
        - 🧠 Simplicidade que transcende
        """)
        
        # Versão e informações
        st.markdown("---")
        st.caption("🏗️ **SWAI Factory v1.0**")
        st.caption("Fábrica de soluções inteligentes")
        st.caption("Filosofia: Senna + Stark + Clássicos")
    
    # Roteamento de páginas
    try:
        if page_key == "dashboard":
            show_dashboard()
        elif page_key == "analysis":
            show_analysis()
        elif page_key == "cost":
            show_cost_calculator()
        elif page_key == "config":
            show_configuration()
        else:
            # Página padrão se algo der errado
            show_dashboard()
            
    except Exception as e:
        st.error(f"❌ Erro ao carregar página: {str(e)}")
        st.info("🔧 Tente acessar as Configurações para verificar o sistema.")
        
        # Mostrar página de configurações como fallback
        show_configuration()
    
    # Footer SWAI
    st.markdown("---")
    st.markdown(f"""
    <div class="swai-footer">
        <strong>🧠 SWAI Factory - Fábrica de Soluções Inteligentes</strong><br>
        <em>"O tempo que devolvemos às pessoas não é apenas produtividade recuperada.<br>
        É oportunidade para amor, crescimento, contemplação, criação."</em><br><br>
        <small>Versão 1.0 MVP | Filosofia: Senna + Stark + Sábios Clássicos</small>
    </div>
    """, unsafe_allow_html=True)

def show_welcome():
    """
    Página de boas-vindas para novos usuários
    """
    st.title("🌟 Bem-vindo ao SWAI WhatsApp Analyzer")
    
    st.markdown("""
    ### 🎯 O que é o SWAI?
    
    O SWAI (Smart WhatsApp AI) é uma fábrica de soluções inteligentes projetada especificamente 
    para clínicas médicas que desejam otimizar suas conversas de WhatsApp e maximizar a conversão de leads.
    
    ### 🏛️ Nossa Filosofia
    
    Baseado nos ensinamentos dos grandes mestres:
    - **Sêneca**: *"Não é que temos pouco tempo, mas sim que desperdiçamos muito dele"*
    - **Ayrton Senna**: Perfeição técnica que permite transcendência humana
    - **Tony Stark**: Tecnologia criada conscientemente para transformar o mundo
    
    ### 🚀 Funcionalidades Principais
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 📊 Dashboard Executivo
        - Visão geral das métricas principais
        - Taxa de conversão em tempo real
        - Insights automáticos para tomada de decisão
        
        #### 🔍 Análise Profunda
        - Padrões de sucesso vs falha
        - Correlações entre variáveis
        - Explorador interativo de conversas
        """)
    
    with col2:
        st.markdown("""
        #### 💰 Custo de Oportunidade
        - Cálculo preciso de receita perdida
        - Simulador de cenários de melhoria
        - ROI de investimentos em treinamento
        
        #### ⚙️ Controle Total
        - Sistema liga-desliga de funcionalidades
        - Configurações financeiras personalizáveis
        - Backup e restore completo
        """)
    
    st.markdown("---")
    
    # Primeiros passos
    st.markdown("### 🎯 Primeiros Passos")
    
    step1, step2, step3 = st.columns(3)
    
    with step1:
        st.markdown("""
        #### 1. 📁 Dados
        - Coloque suas conversas do WhatsApp nas pastas apropriadas
        - Ou use dados de exemplo para testar
        """)
    
    with step2:
        st.markdown("""
        #### 2. ⚙️ Configure
        - Defina parâmetros financeiros
        - Ative funcionalidades desejadas
        - Personalize conforme sua clínica
        """)
    
    with step3:
        st.markdown("""
        #### 3. 📊 Analise
        - Explore o dashboard
        - Identifique padrões
        - Tome decisões baseadas em dados
        """)
    
    if st.button("🚀 Começar Agora", use_container_width=True, type="primary"):
        st.session_state.show_welcome = False
        st.experimental_rerun()

if __name__ == "__main__":
    # Verificar se é a primeira execução
    if 'show_welcome' not in st.session_state:
        st.session_state.show_welcome = True
    
    if st.session_state.show_welcome:
        show_welcome()
    else:
        main()
