import streamlit as st

st.set_page_config(page_title="Cadastro", page_icon="📝", layout="centered")

st.title("📝 Cadastro de Novo Usuário")

# Formulário de Cadastro
with st.form("register_form"):
    username = st.text_input("Usuário")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")
    confirm_password = st.text_input("Confirme a Senha", type="password")
    register_button = st.form_submit_button("Cadastrar")

if register_button:
    if password == confirm_password:
        # Simulação de registro (substituir por lógica real)
        st.success("Usuário cadastrado com sucesso! Volte para a página de login.")
    else:
        st.error("As senhas não coincidem. Tente novamente.")

# Link para voltar ao login
st.markdown("---")
st.markdown("Já possui uma conta? [Volte para o login](home.py)")
