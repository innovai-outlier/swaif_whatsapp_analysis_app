import streamlit as st
import sys
import os

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
from modules.constants import APP_TITLE, APP_SUBTITLE, PRIMARY_COLOR, SECONDARY_COLOR, IMAGE_LOGO_DIR


# Configurar a página principal
st.set_page_config(page_title="Menu Principal", page_icon="💬", layout="wide")


if 'page' not in st.session_state:
    st.session_state.page = 'login'

def logout():
    st.session_state.page = 'login'
    st.success("Logout bem-sucedido! Redirecionando para a página de login...")
    st.rerun()

# Função de login
def login():
    st.header("🔑 Login no Sistema")
    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        login_button = st.form_submit_button("Entrar")

    if login_button:
        # Simulação de autenticação (substituir por lógica real)
        if username == "admin" and password == "admin":
            st.success("Login bem-sucedido! Redirecionando para o menu principal...")
            st.session_state.page = "menu_principal"
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")

# Definir páginas
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
configuracoes_page = st.Page("configuracoes.py", title="Configurações", icon="⚙️")
custo_oportunidade_page = st.Page("custo_de_oportunidade.py", title="Custo de Oportunidade", icon="💰")
dashboards_page = st.Page("dashboard.py", title="Dashboard", icon="📊")
resumos_pendencias_page = st.Page("resumos_e_pendencias.py", title="Resumos e Pendências", icon="📝")#analise_exploratoria_page = st.Page("analise_exploratoria.py", title="Análise Exploratória", icon="🔍")
analise_exploratoria_page = st.Page("analise_exploratoria.py", title="Análise Exploratória", icon="🔍")

try:
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
    st.markdown(f"""
    <div class="main-header">
        <h1>{APP_TITLE}</h1>
        <p>{APP_SUBTITLE}</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        st.logo(IMAGE_LOGO_DIR, icon_image=IMAGE_LOGO_DIR)
    except Exception as e:
        st.error(f"Erro ao carregar a imagem: {str(e)}")

    st.markdown("## Bem-vindo ao Sistema de Análise de Conversas de WhatsApp")

    st.markdown("""
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
    """)
    
    account_pages = [logout_page, configuracoes_page]
    analytical_pages = [custo_oportunidade_page, dashboards_page, analise_exploratoria_page]
    reporting_pages = [resumos_pendencias_page]
    
    page_dict = {}
    page_dict["Minha Conta"] = account_pages
    page_dict["Análise"] = analytical_pages
    page_dict["Relatórios"] = reporting_pages

    if len(page_dict) > 0:
        pg = st.navigation(page_dict)
    else:
        pg = st.navigation([st.Page(login)])
    pg.run()

except Exception as e:
    st.error(f"Ocorreu um erro: {str(e)}")
    
