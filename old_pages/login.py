import streamlit as st

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False 

if 'page' not in st.session_state:
    st.session_state.page = 'login'
    
# Definir páginas
login_page = st.Page("login.py", title="Login", icon="🔑")
cadastro_page = st.Page("cadastrar_usuario.py", title="Cadastro", icon="📝")
menu_principal_page = st.Page("menu_principal.py", title="Menu Principal", icon="💬")

# Configurar a página atual
if not st.session_state.logged_in:
    st.set_page_config(page_title="Login", page_icon="🔑", layout="centered")
    st.title("🔑 Login no Sistema")

    # Formulário de Login
    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        login_button = st.form_submit_button("Entrar")

    if login_button:
        # Simulação de autenticação (substituir por lógica real)
        if username == "admin" and password == "admin":
            st.success("Login bem-sucedido! Redirecionando para o menu principal...")
            st.session_state.logged_in = True
            st.session_state.page = "menu_principal"
            st.rerun()
            
        else:
            st.error("Usuário ou senha inválidos.")

    # Link para cadastro de novos usuários
    st.markdown("---")
    st.markdown("Novo usuário? [Cadastre-se aqui](cadastrar_usuario.py)")
    

if st.session_state.logged_in and st.session_state.page == "menu_principal":
    pg = st.navigation([menu_principal_page])
    pg.run()
