# SWAI WhatsApp Analyzer - Script Principal Corrigido
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

# Adicionar o diretório correto ao path
current_dir = Path(__file__).parent
swai_dir = current_dir / "swaif_whatsapp_analyzer"
sys.path.insert(0, str(swai_dir))

# Importações locais com tratamento de erro
try:
    from swai_features import FEATURES, feature_enabled
    from swai_settings import SWAI_SETTINGS
    from swai_ui_dashboard import show_dashboard
    from swai_ui_analysis import show_analysis
    from swai_ui_cost import show_cost_calculator
    from swai_ui_config import show_configuration 
    imports_successful = True
except ImportError as e:
    imports_successful = False
    import_error = str(e)

# Se as importações falharam, mostrar página de erro e instruções
if not imports_successful:
    st.error("❌ Erro na importação de módulos SWAI")
    st.code(f"Erro: {import_error}")
    
    st.markdown("""
    ## 🔧 Como Corrigir:
    
    ### Opção 1: Executar na pasta correta
    ```bash
    cd swaif_whatsapp_analyzer
    streamlit run swai_app_main.py
    ```
    
    ### Opção 2: Executar o teste primeiro
    ```bash
    cd swaif_whatsapp_analyzer
    python swai_test.py
    ```
    
    ### Opção 3: Instalar dependências
    ```bash
    pip install streamlit pandas plotly
    ```
    
    ### Estrutura esperada:
    ```
    whatsapp_analysis_app/
    ├── run_swai.py                    # Este arquivo
    └── swaif_whatsapp_analyzer/
        ├── swai_app_main.py
        ├── swai_settings.py
        ├── swai_features.py
        ├── swai_core.py
        └── swai_ui_*.py
    ```
    """)
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
        st.markdown("🧠 **SWAI Factory**")
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
            page_key = "config"
        
        # Status das funcionalidades
        st.markdown("---")
        st.markdown("### 🎛️ Status")
        
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
        st.caption("Tecnologia como libertação")
        st.caption("Simplicidade que transcende")
    
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
            show_dashboard()
            
    except Exception as e:
        st.error(f"❌ Erro ao carregar página: {str(e)}")
        st.info("🔧 Tente acessar as Configurações para verificar o sistema.")
        
        # Mostrar página de configurações como fallback
        try:
            show_configuration()
        except:
            st.error("Sistema com problemas. Verifique os arquivos SWAI.")
    
    # Footer SWAI
    st.markdown("---")
    st.markdown(f"""
    <div class="swai-footer">
        <strong>🧠 SWAI Factory - Fábrica de Soluções Inteligentes</strong><br>
        <small>Versão 1.0 MVP | Filosofia: Senna + Stark + Clássicos</small>
    </div>
    """, unsafe_allow_html=True)

def show_welcome():
    """Página de boas-vindas para novos usuários"""
    st.title("🌟 Bem-vindo ao SWAI WhatsApp Analyzer")
    
    st.markdown("""
    ### 🎯 O que é o SWAI?
    
    O SWAI é uma fábrica de soluções inteligentes para análise de conversas do WhatsApp
    em clínicas médicas, focada na otimização da conversão de leads.
    
    ### 🚀 Como Começar:
    
    1. **📊 Dashboard**: Visão geral das métricas
    2. **🔍 Análise**: Explore padrões detalhados  
    3. **💰 Custo**: Calcule impacto financeiro
    4. **⚙️ Config**: Ajuste conforme necessário
    """)
    
    if st.button("🚀 Começar Agora", type="primary", use_container_width=True):
        st.session_state.show_welcome = False
        st.rerun()

if __name__ == "__main__":
    # Verificar se é a primeira execução
    if 'show_welcome' not in st.session_state:
        st.session_state.show_welcome = True
    
    if st.session_state.show_welcome:
        show_welcome()
    else:
        main()
