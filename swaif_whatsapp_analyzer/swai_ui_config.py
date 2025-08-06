# SWAI UI Config - Configurações do Sistema
# Filosofia: Controle total com simplicidade máxima

"""
Módulo de configurações do SWAI WhatsApp Analyzer
Interface para gerenciar funcionalidades, parâmetros e sistema
"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime

def show_configuration():
    """
    Exibe a página de configurações do sistema
    """
    
    from swai_settings import SWAI_SETTINGS, update_setting, get_financial_settings, update_financial_settings
    from swai_features import FEATURES, toggle_feature, feature_enabled, get_enabled_features, get_disabled_features, feature_count
    from swai_core import SWAIConversationExtractor, create_sample_data
    
    st.title("⚙️ Configurações SWAI")
    st.markdown("*Controle total do sistema com simplicidade máxima*")
    
    # === CONTROLE DE FUNCIONALIDADES ===
    st.markdown("### 🎛️ Controle de Funcionalidades")
    st.markdown("*Sistema liga-desliga inspirado na filosofia de simplicidade progressiva*")
    
    # Status geral
    feature_stats = feature_count()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Funcionalidades Ativas", feature_stats['enabled'])
    
    with col2:
        st.metric("Funcionalidades Inativas", feature_stats['disabled'])
    
    with col3:
        st.metric("Percentual Ativo", f"{feature_stats['percentage_enabled']:.0f}%")
    
    st.markdown("---")
    
    # Controles individuais de funcionalidades
    tab1, tab2, tab3 = st.tabs(["🔧 Core Features", "🚀 Advanced Features", "🔮 Future Features"])
    
    with tab1:
        st.markdown("#### Funcionalidades Essenciais")
        st.caption("Funcionalidades principais do SWAI - recomendado manter ativas")
        
        core_features = {
            "dashboard": "Dashboard Principal - Visão geral das métricas",
            "analysis": "Análise de Conversas - Análise detalhada dos dados",
            "cost_calculator": "Custo de Oportunidade - Cálculos financeiros",
            "configuration": "Configurações - Este módulo (sempre ativo)"
        }
        
        for feature, description in core_features.items():
            if feature == "configuration":
                st.info(f"✅ **{description}** (sempre ativo)")
            else:
                current_state = feature_enabled(feature)
                new_state = st.checkbox(
                    f"**{feature.replace('_', ' ').title()}**",
                    value=current_state,
                    help=description,
                    key=f"core_{feature}"
                )
                
                if new_state != current_state:
                    toggle_feature(feature, new_state)
                    st.rerun()
    
    with tab2:
        st.markdown("#### Funcionalidades Avançadas")
        st.caption("Recursos adicionais que podem ser ativados conforme necessidade")
        
        advanced_features = {
            "advanced_charts": "Gráficos Avançados - Visualizações interativas detalhadas",
            "export_data": "Exportação de Dados - Download de relatórios e dados",
            "smart_summaries": "Resumos Inteligentes - Resumos automáticos com IA (experimental)",
            "real_time_analysis": "Análise em Tempo Real - Processamento contínuo (experimental)"
        }
        
        for feature, description in advanced_features.items():
            current_state = feature_enabled(feature)
            new_state = st.checkbox(
                f"**{feature.replace('_', ' ').title()}**",
                value=current_state,
                help=description,
                key=f"advanced_{feature}"
            )
            
            if new_state != current_state:
                toggle_feature(feature, new_state)
                st.rerun()
    
    with tab3:
        st.markdown("#### Funcionalidades Futuras")
        st.caption("Recursos planejados para versões futuras (atualmente indisponíveis)")
        
        future_features = {
            "api_mode": "Modo API - Interface REST para integração",
            "whatsapp_integration": "Integração WhatsApp - Conexão direta com WhatsApp Business",
            "ai_insights": "Insights com IA - Análises avançadas com IA generativa",
            "multi_user": "Múltiplos Usuários - Sistema multiusuário com permissões",
            "database_mode": "Modo Banco de Dados - Persistência avançada de dados"
        }
        
        for feature, description in future_features.items():
            st.info(f"🔮 **{feature.replace('_', ' ').title()}**: {description} (em desenvolvimento)")
    
    # === MODOS RÁPIDOS ===
    st.markdown("---")
    st.markdown("### ⚡ Modos Rápidos")
    st.markdown("*Configurações predefinidas para diferentes necessidades*")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Modo MVP", use_container_width=True, help="Apenas funcionalidades essenciais"):
            from swai_features import enable_mvp_mode
            enable_mvp_mode()
            st.success("✅ Modo MVP ativado!")
            st.rerun()
    
    with col2:
        if st.button("🚀 Modo Completo", use_container_width=True, help="Todas funcionalidades disponíveis"):
            from swai_features import enable_full_mode
            enable_full_mode()
            st.success("✅ Modo Completo ativado!")
            st.rerun()
    
    with col3:
        if st.button("🎮 Modo Demo", use_container_width=True, help="Configuração para demonstrações"):
            from swai_features import enable_demo_mode
            enable_demo_mode()
            st.success("✅ Modo Demo ativado!")
            st.rerun()
    
    # === CONFIGURAÇÕES FINANCEIRAS ===
    st.markdown("---")
    st.markdown("### 💰 Parâmetros Financeiros")
    
    financial_config = get_financial_settings()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💵 Valores")
        
        new_valor_consulta = st.number_input(
            "Valor Médio da Consulta (R$)",
            min_value=50.0,
            max_value=10000.0,
            value=financial_config['valor_consulta'],
            step=50.0,
            help="Valor médio de receita por consulta realizada"
        )
        
        new_leads_diarios = st.slider(
            "Leads por Dia",
            min_value=1,
            max_value=100,
            value=financial_config['leads_diarios'],
            help="Número médio de leads que entram em contato por dia"
        )
    
    with col2:
        st.markdown("#### 📅 Calendário")
        
        new_dias_uteis_mes = st.slider(
            "Dias Úteis por Mês",
            min_value=15,
            max_value=25,
            value=financial_config['dias_uteis_mes'],
            help="Quantidade de dias úteis trabalhados por mês"
        )
        
        dias_uteis_ano = new_dias_uteis_mes * 12
        st.metric("Dias Úteis por Ano", dias_uteis_ano)
    
    # Salvar alterações financeiras
    if (new_valor_consulta != financial_config['valor_consulta'] or 
        new_leads_diarios != financial_config['leads_diarios']):
        
        if st.button("💾 Salvar Configurações Financeiras", use_container_width=True):
            update_financial_settings(new_valor_consulta, new_leads_diarios)
            update_setting('DIAS_UTEIS_MES', new_dias_uteis_mes)
            st.success("✅ Configurações financeiras salvas!")
            st.rerun()
    
    # === GERENCIAMENTO DE DADOS ===
    st.markdown("---")
    st.markdown("### 📁 Gerenciamento de Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Status dos Dados")
        
        # Verificar se existem dados
        features_csv = Path(SWAI_SETTINGS.get('FEATURES_CSV', ''))
        success_dir = Path(SWAI_SETTINGS.get('SUCCESS_CASES_DIR', ''))
        fail_dir = Path(SWAI_SETTINGS.get('FAIL_CASES_DIR', ''))
        
        if features_csv.exists():
            st.success("✅ Dados processados encontrados")
            # Mostrar informações do arquivo
            try:
                import pandas as pd
                df = pd.read_csv(features_csv)
                st.info(f"📄 {len(df)} conversas processadas")
            except:
                st.warning("⚠️ Erro ao ler dados processados")
        else:
            st.warning("⚠️ Nenhum dado processado encontrado")
        
        # Verificar diretórios de conversas
        success_count = len(list(success_dir.glob("*/")) if success_dir.exists() else [])
        fail_count = len(list(fail_dir.glob("*/")) if fail_dir.exists() else [])
        
        st.metric("Conversas de Sucesso", success_count)
        st.metric("Conversas de Falha", fail_count)
    
    with col2:
        st.markdown("#### 🔄 Ações de Dados")
        
        if st.button("🔄 Reprocessar Conversas", use_container_width=True):
            with st.spinner("Processando conversas..."):
                try:
                    extractor = SWAIConversationExtractor(SWAI_SETTINGS)
                    df = extractor.process_all_conversations()
                    
                    if not df.empty:
                        # Salvar dados processados
                        df.to_csv(features_csv, index=False)
                        st.success(f"✅ {len(df)} conversas processadas com sucesso!")
                    else:
                        st.warning("⚠️ Nenhuma conversa encontrada para processar")
                except Exception as e:
                    st.error(f"❌ Erro no processamento: {str(e)}")
        
        if st.button("🎲 Gerar Dados de Exemplo", use_container_width=True):
            with st.spinner("Gerando dados de exemplo..."):
                try:
                    sample_df = create_sample_data()
                    sample_df.to_csv(features_csv, index=False)
                    st.success(f"✅ {len(sample_df)} conversas de exemplo geradas!")
                except Exception as e:
                    st.error(f"❌ Erro ao gerar exemplos: {str(e)}")
        
        if st.button("🗑️ Limpar Cache", use_container_width=True):
            # Limpar cache do Streamlit
            st.cache_data.clear()
            st.success("✅ Cache limpo!")
    
    # === CONFIGURAÇÕES AVANÇADAS ===
    st.markdown("---")
    st.markdown("### 🔧 Configurações Avançadas")
    
    with st.expander("🎨 Personalização Visual"):
        st.markdown("#### Esquema de Cores")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_primary = st.color_picker(
                "Cor Primária",
                value=SWAI_SETTINGS['PRIMARY_COLOR'],
                help="Cor principal da interface"
            )
            
            new_secondary = st.color_picker(
                "Cor Secundária", 
                value=SWAI_SETTINGS['SECONDARY_COLOR'],
                help="Cor secundária para destaques"
            )
        
        with col2:
            new_success = st.color_picker(
                "Cor de Sucesso",
                value=SWAI_SETTINGS['SUCCESS_COLOR'],
                help="Cor para indicar sucesso"
            )
            
            new_error = st.color_picker(
                "Cor de Erro",
                value=SWAI_SETTINGS['ERROR_COLOR'],
                help="Cor para indicar erros"
            )
        
        if st.button("🎨 Aplicar Cores Personalizadas"):
            update_setting('PRIMARY_COLOR', new_primary)
            update_setting('SECONDARY_COLOR', new_secondary)
            update_setting('SUCCESS_COLOR', new_success)
            update_setting('ERROR_COLOR', new_error)
            st.success("✅ Cores personalizadas aplicadas!")
            st.rerun()
    
    with st.expander("🔍 Palavras-chave de Análise"):
        st.markdown("#### Configurar Vocabulário de Análise")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Palavras de Agendamento**")
            agendamento_text = st.text_area(
                "Uma palavra por linha:",
                value="\n".join(SWAI_SETTINGS.get('AGENDAMENTO_KEYWORDS', [])),
                height=150,
                help="Palavras que indicam tentativa de agendamento"
            )
        
        with col2:
            st.markdown("**Palavras de Preço**")
            preco_text = st.text_area(
                "Uma palavra por linha:",
                value="\n".join(SWAI_SETTINGS.get('PRECO_KEYWORDS', [])),
                height=150,
                help="Palavras relacionadas a preço e valor"
            )
        
        if st.button("💾 Salvar Palavras-chave"):
            new_agendamento = [word.strip() for word in agendamento_text.split('\n') if word.strip()]
            new_preco = [word.strip() for word in preco_text.split('\n') if word.strip()]
            
            update_setting('AGENDAMENTO_KEYWORDS', new_agendamento)
            update_setting('PRECO_KEYWORDS', new_preco)
            st.success("✅ Palavras-chave atualizadas!")
    
    with st.expander("🐛 Configurações de Debug"):
        st.markdown("#### Modo Desenvolvedor")
        
        debug_enabled = st.checkbox(
            "Ativar Modo Debug",
            value=feature_enabled("debug_mode"),
            help="Exibe informações técnicas detalhadas"
        )
        
        if debug_enabled != feature_enabled("debug_mode"):
            toggle_feature("debug_mode", debug_enabled)
        
        performance_enabled = st.checkbox(
            "Métricas de Performance",
            value=feature_enabled("performance_metrics"),
            help="Coleta métricas de performance do sistema"
        )
        
        if performance_enabled != feature_enabled("performance_metrics"):
            toggle_feature("performance_metrics", performance_enabled)
        
        if debug_enabled:
            st.markdown("#### 🔍 Informações Técnicas")
            
            # Informações do sistema
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Configurações Atuais:**")
                st.json({
                    "features_enabled": len(get_enabled_features()),
                    "primary_color": SWAI_SETTINGS['PRIMARY_COLOR'],
                    "valor_consulta": SWAI_SETTINGS['VALOR_MEDIO_CONSULTA'],
                    "leads_diarios": SWAI_SETTINGS['LEADS_DIARIOS']
                })
            
            with col2:
                st.markdown("**Funcionalidades Ativas:**")
                for feature in get_enabled_features():
                    st.text(f"✅ {feature}")
    
    # === BACKUP E RESTORE ===
    st.markdown("---")
    st.markdown("### 💾 Backup e Restore")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📤 Exportar Configurações")
        
        if st.button("💾 Fazer Backup", use_container_width=True):
            # Criar backup das configurações
            backup_data = {
                "features": FEATURES,
                "settings": {
                    "valor_consulta": SWAI_SETTINGS['VALOR_MEDIO_CONSULTA'],
                    "leads_diarios": SWAI_SETTINGS['LEADS_DIARIOS'],
                    "dias_uteis_mes": SWAI_SETTINGS['DIAS_UTEIS_MES'],
                    "primary_color": SWAI_SETTINGS['PRIMARY_COLOR'],
                    "secondary_color": SWAI_SETTINGS['SECONDARY_COLOR'],
                    "agendamento_keywords": SWAI_SETTINGS['AGENDAMENTO_KEYWORDS'],
                    "preco_keywords": SWAI_SETTINGS['PRECO_KEYWORDS']
                },
                "backup_date": str(datetime.now())
            }
            
            backup_json = json.dumps(backup_data, indent=2, ensure_ascii=False)
            
            st.download_button(
                label="⬇️ Baixar Backup",
                data=backup_json,
                file_name="swai_backup.json",
                mime="application/json"
            )
    
    with col2:
        st.markdown("#### 📥 Restaurar Configurações")
        
        uploaded_backup = st.file_uploader(
            "Selecionar arquivo de backup",
            type=['json'],
            help="Selecione um arquivo de backup SWAI"
        )
        
        if uploaded_backup and st.button("🔄 Restaurar Backup", use_container_width=True):
            try:
                backup_data = json.load(uploaded_backup)
                
                # Restaurar features
                if "features" in backup_data:
                    from swai_features import toggle_feature
                    for key, value in backup_data["features"].items():
                        try:
                            toggle_feature(key, value)
                        except ValueError:
                            pass  # Feature não existe
                
                # Restaurar settings
                if "settings" in backup_data:
                    settings = backup_data["settings"]
                    for key, value in settings.items():
                        if key.upper() in SWAI_SETTINGS:
                            update_setting(key.upper(), value)
                
                st.success("✅ Backup restaurado com sucesso!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erro ao restaurar backup: {str(e)}")
    
    # === INFORMAÇÕES DO SISTEMA ===
    st.markdown("---")
    st.markdown("### ℹ️ Informações do Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🏗️ SWAI Factory**")
        st.caption("Versão: 1.0 MVP")
        st.caption("Modo: Simplificado")
        st.caption("Filosofia: Senna + Stark")
    
    with col2:
        st.markdown("**📊 Estatísticas**")
        st.caption(f"Features Ativas: {feature_stats['enabled']}")
        st.caption(f"Dados Processados: {'Sim' if features_csv.exists() else 'Não'}")
        st.caption(f"Cache Status: {'Ativo' if st.cache_data else 'Inativo'}")
    
    with col3:
        st.markdown("**🎯 Filosofia SWAI**")
        st.caption("Tecnologia como Libertação")
        st.caption("Preservação da Dignidade Humana")
        st.caption("Tempo Sagrado")
    
    # === RESET TOTAL ===
    st.markdown("---")
    
    with st.expander("⚠️ Reset Total do Sistema"):
        st.warning("**ATENÇÃO**: Esta ação irá restaurar todas as configurações para os valores padrão!")
        
        if st.text_input("Digite 'RESET' para confirmar:", key="reset_confirm") == "RESET":
            if st.button("🔄 RESETAR SISTEMA COMPLETO", type="primary"):
                # Reset todas as features para MVP
                from swai_features import enable_mvp_mode
                enable_mvp_mode()
                
                # Reset configurações financeiras
                update_financial_settings(800.0, 5)
                update_setting('DIAS_UTEIS_MES', 20)
                
                # Reset cores
                update_setting('PRIMARY_COLOR', "#0A1128")
                update_setting('SECONDARY_COLOR', "#FF7F11")
                
                st.success("✅ Sistema resetado para configurações padrão!")
                st.rerun()

def show_about():
    """
    Mostra informações sobre o SWAI
    """
    st.markdown("### 🧠 Sobre o SWAI WhatsApp Analyzer")
    
    st.markdown("""
    #### 🎯 Missão
    Libertar profissionais de saúde das tarefas mecânicas, permitindo foco total no cuidado humano.
    
    #### 🏛️ Filosofia
    Baseado nos ensinamentos de:
    - **Sêneca**: "Não é que temos pouco tempo, mas sim que desperdiçamos muito dele"
    - **Ayrton Senna**: Perfeição técnica que permite transcendência humana
    - **Tony Stark**: Tecnologia criada conscientemente para transformar o mundo
    
    #### 🛠️ Tecnologia
    - **Linguagem**: Python 3.11+
    - **Interface**: Streamlit
    - **Análise**: Pandas + Plotly
    - **Arquitetura**: Microserviços modulares
    - **Filosofia**: SWAI Factory - Fábrica de soluções inteligentes
    
    #### 📈 Funcionalidades
    - Dashboard executivo com métricas principais
    - Análise detalhada de padrões de conversa
    - Calculadora de custo de oportunidade
    - Sistema de funcionalidades liga-desliga
    - Configurações flexíveis e personalizáveis
    """)

if __name__ == "__main__":
    show_configuration()
