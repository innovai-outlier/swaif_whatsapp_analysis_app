# SWAI WhatsApp Analyzer - Versão Simplificada
# Baseado na filosofia SWAI Factory: Tecnologia como libertação

import streamlit as st
import sys
import os
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="SWAI WhatsApp Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Adicionar paths para importações
sys.path.append(str(Path(__file__).parent))

# Importações locais
from swai_config.features import FEATURES, feature_enabled
from swai_config.settings import SWAI_SETTINGS
from swai_ui.dashboard import show_dashboard
from swai_ui.analysis import show_analysis
from swai_ui.cost import show_cost_calculator
from swai_ui.config import show_configuration

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
        st.image(SWAI_SETTINGS.get('LOGO_PATH', 'assets/image.png'), width=80)
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
            page_key = pages[selected_page]
        else:
            st.error("Nenhuma funcionalidade habilitada!")
            st.stop()
        
        # Status das funcionalidades
        st.markdown("---")
        st.markdown("### 🎛️ Status das Funcionalidades")
        
        for feature, enabled in FEATURES.items():
            if enabled:
                st.success(f"✅ {feature.replace('_', ' ').title()}")
            else:
                st.warning(f"⏸️ {feature.replace('_', ' ').title()}")
        
        # Filosofia SWAI
        st.markdown("---")
        st.markdown("""
        ### 💭 Filosofia SWAI
        
        > *"Não é que temos pouco tempo, mas sim que desperdiçamos muito dele"* - Sêneca
        
        **Princípios:**
        - 🎯 Tecnologia como libertação
        - 🤝 Preservação da dignidade humana  
        - ⚡ Eficiência com propósito
        """)
    
    # Roteamento de páginas
    if page_key == "dashboard":
        show_dashboard()
    elif page_key == "analysis":
        show_analysis()
    elif page_key == "cost":
        show_cost_calculator()
    elif page_key == "config":
        show_configuration()
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🏗️ SWAI Factory**")
        st.caption("Fábrica de soluções inteligentes")
    
    with col2:
        st.markdown("**⏱️ Tempo Sagrado**")
        st.caption("Devolvendo tempo às pessoas")
    
    with col3:
        st.markdown("**🎯 Versão Atual**")
        st.caption("1.0 - MVP Simplificado")

if __name__ == "__main__":
    main()
