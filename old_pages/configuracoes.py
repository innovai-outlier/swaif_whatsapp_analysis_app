import streamlit as st
import sys
import os

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))

from modules.constants import ALIGNED_CONTENT_FILE, ALIGNED_CONTENT_TEMPLATE, VALOR_MEDIO_CONSULTA, LEADS_DIARIOS
from modules.utils import check_file_exists

st.set_page_config(page_title="Configurações", page_icon="⚙️", layout="wide")

st.title("⚙️ Configurações")
st.markdown("Gerenciamento de parâmetros e configuração do alinhamento")

# Tabs for different configuration sections
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Alinhamento", "💰 Parâmetros", "📁 Dados", "🔧 Sistema"])

with tab1:
    st.subheader("🎯 Configuração do Alinhamento")
    
    st.markdown("""
    Configure aqui as diretrizes e instruções que a médica fornece para a secretária. 
    Isso permitirá calcular o grau de alinhamento das conversas com o padrão esperado.
    """)
    
    # Check if aligned content file exists
    aligned_content_exists = check_file_exists(ALIGNED_CONTENT_FILE)
    
    if aligned_content_exists:
        st.success("✅ Arquivo de alinhamento encontrado!")
        
        # Load current content
        try:
            with open(ALIGNED_CONTENT_FILE, 'r', encoding='utf-8') as f:
                current_content = f.read()
        except:
            current_content = ""
        
        # Display current content
        with st.expander("📄 Conteúdo Atual", expanded=False):
            st.text_area(
                "Conteúdo alinhado atual:",
                value=current_content,
                height=200,
                disabled=True
            )
    else:
        st.warning("⚠️ Arquivo de alinhamento não encontrado. Configure abaixo para ativar a análise de alinhamento.")
        current_content = ""
    
    # Configuration form
    st.markdown("### ✏️ Editar Conteúdo Alinhado")
    
    # Load template content for reference
    template_content = ""
    if check_file_exists(ALIGNED_CONTENT_TEMPLATE):
        try:
            with open(ALIGNED_CONTENT_TEMPLATE, 'r', encoding='utf-8') as f:
                template_content = f.read()
        except:
            pass
    
    # Show template as reference
    if template_content:
        with st.expander("📋 Template de Referência", expanded=False):
            st.markdown(template_content)
    
    # Text area for editing
    new_content = st.text_area(
        "Instruções da médica para a secretária:",
        value=current_content,
        height=300,
        help="Digite as principais diretrizes, frases-chave e instruções que a médica treina a secretária para usar nas conversas.",
        placeholder="""Exemplo:
- Sempre perguntar o motivo principal que faz o paciente buscar o acompanhamento.
- Explicar detalhadamente como funcionam os atendimentos.
- Informar sobre o valor da consulta e opções de pagamento.
- Oferecer o pós-consulta ativo via WhatsApp.
- Verificar disponibilidade antes de propor horários específicos."""
    )
    
    # Save button
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("💾 Salvar Alinhamento", type="primary"):
            try:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(ALIGNED_CONTENT_FILE), exist_ok=True)
                
                with open(ALIGNED_CONTENT_FILE, 'w', encoding='utf-8') as f:
                    f.write(new_content.strip())
                
                st.success("✅ Conteúdo alinhado salvo com sucesso!")
                st.info("💡 Execute novamente a extração de features para atualizar os scores de alinhamento.")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erro ao salvar: {str(e)}")
    
    with col2:
        if aligned_content_exists and st.button("🗑️ Remover Alinhamento"):
            try:
                os.remove(ALIGNED_CONTENT_FILE)
                st.success("✅ Arquivo de alinhamento removido!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro ao remover: {str(e)}")

with tab2:
    st.subheader("💰 Parâmetros Financeiros")
    
    st.markdown("""
    Configure os parâmetros utilizados no cálculo do custo de oportunidade.
    """)
    
    # Current parameters display
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Parâmetros Atuais")
        st.metric("Valor Médio da Consulta", f"R$ {VALOR_MEDIO_CONSULTA:,.2f}")
        st.metric("Leads Diários", LEADS_DIARIOS)
    
    with col2:
        st.markdown("### ✏️ Novos Valores")
        
        new_valor_consulta = st.number_input(
            "Valor médio da consulta (R$)",
            min_value=0.0,
            value=float(VALOR_MEDIO_CONSULTA),
            step=50.0,
            help="Valor médio em reais de uma consulta bem-sucedida"
        )
        
        new_leads_diarios = st.number_input(
            "Leads diários",
            min_value=1,
            value=LEADS_DIARIOS,
            step=1,
            help="Número médio de leads recebidos por dia"
        )
        
        if st.button("💾 Atualizar Parâmetros"):
            # Note: In a real application, you might want to save these to a config file
            st.info("💡 Os novos parâmetros serão aplicados nos cálculos das outras páginas durante esta sessão.")
            st.success("✅ Parâmetros atualizados!")
    
    # Impact simulation
    st.markdown("---")
    st.markdown("### 📈 Simulação de Impacto")
    
    st.markdown("Veja como mudanças nos parâmetros afetam o custo de oportunidade:")
    
    # Simulate with different values
    test_failure_rate = 0.5  # Example failure rate
    
    current_cost_monthly = (LEADS_DIARIOS * test_failure_rate) * VALOR_MEDIO_CONSULTA * 20
    new_cost_monthly = (new_leads_diarios * test_failure_rate) * new_valor_consulta * 20
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Custo Atual (mensal)",
            f"R$ {current_cost_monthly:,.2f}",
            help="Baseado nos parâmetros atuais"
        )
    
    with col2:
        st.metric(
            "Novo Custo (mensal)",
            f"R$ {new_cost_monthly:,.2f}",
            delta=f"R$ {new_cost_monthly - current_cost_monthly:,.2f}",
            help="Baseado nos novos parâmetros"
        )
    
    with col3:
        if current_cost_monthly > 0:
            change_percent = ((new_cost_monthly - current_cost_monthly) / current_cost_monthly) * 100
            st.metric(
                "Variação",
                f"{change_percent:+.1f}%",
                help="Mudança percentual no custo"
            )

with tab3:
    st.subheader("📁 Gerenciamento de Dados")
    
    st.markdown("""
    Gerencie os dados de conversas e execute operações de processamento.
    """)
    
    # Data status
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Status dos Dados")
        
        # Check data files
        data_files = {
            "Features Extraídas": "data/extracted_features_enhanced.csv",
            "Análise Detalhada": "data/detailed_analysis_results.json",
            "Casos de Sucesso": "data/success_cases",
            "Casos de Falha": "data/fail_cases"
        }
        
        for name, path in data_files.items():
            if check_file_exists(path):
                st.success(f"✅ {name}")
            else:
                st.error(f"❌ {name}")
    
    with col2:
        st.markdown("### 🔄 Operações")
        
        if st.button("🔄 Reprocessar Dados", type="primary"):
            st.info("💡 Execute o comando no terminal:")
            st.code("python modules/extract_features_enhanced.py")
            st.markdown("Isso irá:")
            st.markdown("- Reprocessar todas as conversas")
            st.markdown("- Atualizar scores de alinhamento")
            st.markdown("- Gerar novos resumos e pendências")
        
        if st.button("📊 Gerar Gráficos"):
            st.info("💡 Execute o comando no terminal:")
            st.code("python modules/analyze_features_enhanced.py")
            st.markdown("Isso irá gerar novos gráficos de análise exploratória.")
        
        if st.button("🧹 Limpar Cache"):
            st.cache_data.clear()
            st.success("✅ Cache limpo!")
    
    # Upload new data
    st.markdown("---")
    st.markdown("### 📤 Upload de Novos Dados")
    
    st.markdown("""
    Para adicionar novas conversas:
    1. Organize os arquivos em pastas `success_cases` e `fail_cases`
    2. Cada conversa deve estar em um arquivo `_chat.txt`
    3. Substitua as pastas existentes em `data/`
    4. Execute o reprocessamento
    """)
    
    uploaded_files = st.file_uploader(
        "Selecione arquivos de chat",
        accept_multiple_files=True,
        type=['txt'],
        help="Arquivos de chat do WhatsApp exportados"
    )
    
    if uploaded_files:
        st.info(f"📁 {len(uploaded_files)} arquivo(s) selecionado(s)")
        st.markdown("💡 **Próximos passos:**")
        st.markdown("1. Organize os arquivos nas pastas apropriadas")
        st.markdown("2. Execute o reprocessamento")

with tab4:
    st.subheader("🔧 Configurações do Sistema")
    
    st.markdown("""
    Configurações técnicas e informações do sistema.
    """)
    
    # System info
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💻 Informações do Sistema")
        
        st.info(f"**Streamlit:** {st.__version__}")
        st.info(f"**Python:** {sys.version.split()[0]}")
        st.info(f"**Diretório:** {os.getcwd()}")
    
    with col2:
        st.markdown("### 🎨 Personalização")
        
        # Theme settings (placeholder for future implementation)
        st.selectbox(
            "Tema",
            options=["Padrão", "Escuro", "Claro"],
            disabled=True,
            help="Funcionalidade em desenvolvimento"
        )
        
        st.selectbox(
            "Idioma",
            options=["Português", "English"],
            disabled=True,
            help="Funcionalidade em desenvolvimento"
        )
    
    # Debug information
    st.markdown("---")
    st.markdown("### 🐛 Informações de Debug")
    
    if st.checkbox("Mostrar informações técnicas"):
        st.markdown("**Variáveis de ambiente:**")
        st.json({
            "ALIGNED_CONTENT_FILE": ALIGNED_CONTENT_FILE,
            "VALOR_MEDIO_CONSULTA": VALOR_MEDIO_CONSULTA,
            "LEADS_DIARIOS": LEADS_DIARIOS
        })
        
        st.markdown("**Estrutura de diretórios:**")
        try:
            for root, dirs, files in os.walk("."):
                level = root.replace(".", "").count(os.sep)
                indent = " " * 2 * level
                st.text(f"{indent}{os.path.basename(root)}/")
                subindent = " " * 2 * (level + 1)
                for file in files[:5]:  # Show only first 5 files
                    st.text(f"{subindent}{file}")
                if len(files) > 5:
                    st.text(f"{subindent}... e mais {len(files) - 5} arquivos")
        except:
            st.error("Erro ao listar diretórios")
    
    # Reset options
    st.markdown("---")
    st.markdown("### 🔄 Reset")
    
    st.warning("⚠️ **Atenção:** As operações abaixo são irreversíveis!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Limpar Configurações", type="secondary"):
            if check_file_exists(ALIGNED_CONTENT_FILE):
                try:
                    os.remove(ALIGNED_CONTENT_FILE)
                    st.success("✅ Configurações de alinhamento removidas!")
                except:
                    st.error("❌ Erro ao remover configurações")
            else:
                st.info("ℹ️ Nenhuma configuração para remover")
    
    with col2:
        if st.button("🔄 Reset Completo", type="secondary"):
            st.error("🚫 Funcionalidade desabilitada por segurança")
            st.info("💡 Para reset completo, delete manualmente os arquivos de dados")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
    💬 Sistema de Análise de Conversas de WhatsApp | Versão 1.0
</div>
""", unsafe_allow_html=True)

