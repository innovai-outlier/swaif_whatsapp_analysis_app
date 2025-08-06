import streamlit as st
import sys
import os

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules.constants import APP_TITLE, APP_SUBTITLE, PRIMARY_COLOR, SECONDARY_COLOR

# Definindo as páginas
menu_principal_page = st.Page("MENU PRINCIPAL.py", title="Menu Principal", icon="💬")
login_page = st.Page("pages/login.py", title="Login", icon="🔑")

# Configurando a navegação
pg = st.navigation([menu_principal_page, login_page])
st.set_page_config(page_title="Sistema de Análise de WhatsApp", page_icon="💬")

# Executando a página selecionada
pg.run()

# Custom CSS
st.markdown(f"""
<style>
    .main-header {{
        background: linear-gradient(90deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }}
    
    .main-header h1 {{
        color: white;
        margin: 0;
        text-align: center;
    }}
    
    .main-header p {{
        color: white;
        margin: 0;
        text-align: center;
        opacity: 0.9;
    }}
    
    .metric-card {{
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid {SECONDARY_COLOR};
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }}
    
    .sidebar .sidebar-content {{
        background-color: {PRIMARY_COLOR};
    }}
    
    .stSelectbox > div > div {{
        background-color: white;
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="main-header">
    <h1>{APP_TITLE}</h1>
    <p>{APP_SUBTITLE}</p>
</div>
""", unsafe_allow_html=True)

# Adicionando suporte para navegação com st.session_state
if 'page' not in st.session_state:
    st.session_state.page = 'MENU PRINCIPAL'

# Função para redirecionar para outra página
def navigate_to(page_name):
    st.session_state.page = page_name
    st.experimental_set_query_params(page=page_name)

# Main content
st.markdown("""
## Bem-vindo ao Sistema de Análise de Conversas de WhatsApp

Este aplicativo foi desenvolvido para ajudar médicos e secretárias a analisar conversas de WhatsApp, 
identificar padrões de sucesso e falha, e calcular o custo de oportunidade de leads não convertidos.

### Funcionalidades Principais:

- **📊 Dashboard**: Visão geral dos dados e métricas principais
- **🔍 Análise Exploratória**: Gráficos e estatísticas detalhadas
- **💰 Custo de Oportunidade**: Cálculo do impacto financeiro
- **📝 Resumos e Pendências**: Análise detalhada das conversas
- **⚙️ Configurações**: Gerenciamento de parâmetros e alinhamento

### Como usar:

1. **Navegue pelas páginas** usando o menu lateral
2. **Carregue seus dados** de conversas de WhatsApp
3. **Configure o alinhamento** com as diretrizes da médica
4. **Analise os resultados** e tome decisões baseadas em dados

### Primeiros Passos:

1. Vá para a página **Configurações** para definir o conteúdo alinhado
2. Acesse o **Dashboard** para uma visão geral dos dados
3. Explore a **Análise Exploratória** para insights detalhados
""")

# Sidebar
with st.sidebar:
    st.image("assets/image.png", width=100)
    st.markdown("---")
    
    st.markdown("""
    ### 📋 Menu de Navegação
    
    Use as páginas acima para navegar pelo aplicativo.
    
    ### 💡 Dicas
    
    - Mantenha os dados atualizados
    - Configure o alinhamento regularmente
    - Monitore o custo de oportunidade
    
    ### 📞 Suporte
    
    Em caso de dúvidas, consulte a documentação ou entre em contato com o suporte técnico.
    """)

