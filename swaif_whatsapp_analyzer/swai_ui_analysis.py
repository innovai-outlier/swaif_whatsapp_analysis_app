# SWAI UI Analysis - Análise Detalhada
# Filosofia: Profundidade com simplicidade

"""
Módulo de análise detalhada das conversas
Interface focada em insights práticos
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def show_analysis():
    """
    Exibe a página de análise detalhada
    """
    
    from swai_settings import SWAI_SETTINGS, get_color_scheme
    from swai_core import SWAIAnalyzer, create_sample_data
    from swai_features import feature_enabled
    
    st.title("🔍 Análise Detalhada")
    st.markdown("*Mergulhe fundo nos padrões que fazem a diferença*")
    
    # Verificar se funcionalidade está habilitada
    if not feature_enabled("analysis"):
        st.warning("⏸️ Análise está desabilitada. Ative nas configurações.")
        return
    
    # Inicializar
    analyzer = SWAIAnalyzer(SWAI_SETTINGS)
    colors = get_color_scheme()
    
    # Carregar dados
    df = analyzer.load_conversation_data()
    if df is None or df.empty:
        st.info("📝 Usando dados de exemplo para demonstração")
        df = create_sample_data()
        is_sample_data = True
    else:
        is_sample_data = False
    
    if df.empty:
        st.error("❌ Nenhum dado disponível para análise")
        return
    
    # === CONTROLES DE FILTRO ===
    st.markdown("### 🎛️ Filtros de Análise")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Filtro por tipo de conversa
        chat_types = ['Todos'] + list(df['chat_type'].unique())
        selected_type = st.selectbox("Tipo de Conversa", chat_types)
    
    with col2:
        # Filtro por duração
        min_duration = st.slider(
            "Duração Mínima (min)",
            min_value=0,
            max_value=int(df['duration_minutes'].max()),
            value=0
        )
    
    with col3:
        # Filtro por número de mensagens
        min_messages = st.slider(
            "Mensagens Mínimas",
            min_value=0,
            max_value=int(df['total_messages'].max()),
            value=0
        )
    
    # Aplicar filtros
    filtered_df = df.copy()
    
    if selected_type != 'Todos':
        filtered_df = filtered_df[filtered_df['chat_type'] == selected_type]
    
    filtered_df = filtered_df[
        (filtered_df['duration_minutes'] >= min_duration) &
        (filtered_df['total_messages'] >= min_messages)
    ]
    
    st.info(f"📊 Analisando {len(filtered_df)} de {len(df)} conversas")
    
    # === DISTRIBUIÇÕES ===
    st.markdown("---")
    st.markdown("### 📈 Distribuições dos Dados")
    
    tab1, tab2, tab3 = st.tabs(["⏱️ Duração", "💬 Mensagens", "🔑 Palavras-chave"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Histograma de duração
            fig_hist_duration = px.histogram(
                filtered_df,
                x='duration_minutes',
                color='chat_type',
                nbins=20,
                title="Distribuição da Duração das Conversas",
                color_discrete_map={'success': colors['success'], 'fail': colors['error']}
            )
            fig_hist_duration.update_layout(height=400)
            st.plotly_chart(fig_hist_duration, use_container_width=True)
        
        with col2:
            # Box plot de duração por tipo
            fig_box_duration = px.box(
                filtered_df,
                x='chat_type',
                y='duration_minutes',
                color='chat_type',
                title="Duração por Tipo de Conversa",
                color_discrete_map={'success': colors['success'], 'fail': colors['error']}
            )
            fig_box_duration.update_layout(height=400)
            st.plotly_chart(fig_box_duration, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Scatter plot mensagens vs duração
            fig_scatter = px.scatter(
                filtered_df,
                x='duration_minutes',
                y='total_messages',
                color='chat_type',
                size='num_interactions',
                title="Mensagens vs Duração",
                color_discrete_map={'success': colors['success'], 'fail': colors['error']},
                hover_data=['secretary_messages', 'patient_messages']
            )
            fig_scatter.update_layout(height=400)
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col2:
            # Proporção secretária vs paciente
            filtered_df['secretary_ratio'] = filtered_df['secretary_messages'] / filtered_df['total_messages']
            
            fig_ratio = px.histogram(
                filtered_df,
                x='secretary_ratio',
                color='chat_type',
                nbins=15,
                title="Proporção de Mensagens da Secretária",
                color_discrete_map={'success': colors['success'], 'fail': colors['error']}
            )
            fig_ratio.update_layout(height=400)
            st.plotly_chart(fig_ratio, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Palavras de agendamento
            fig_agend = px.box(
                filtered_df,
                x='chat_type',
                y='agendamento_keywords',
                color='chat_type',
                title="Palavras de Agendamento por Tipo",
                color_discrete_map={'success': colors['success'], 'fail': colors['error']}
            )
            fig_agend.update_layout(height=400)
            st.plotly_chart(fig_agend, use_container_width=True)
        
        with col2:
            # Palavras de preço
            fig_preco = px.box(
                filtered_df,
                x='chat_type',
                y='preco_keywords',
                color='chat_type',
                title="Palavras de Preço por Tipo",
                color_discrete_map={'success': colors['success'], 'fail': colors['error']}
            )
            fig_preco.update_layout(height=400)
            st.plotly_chart(fig_preco, use_container_width=True)
    
    # === ANÁLISE DE CORRELAÇÃO ===
    if feature_enabled("advanced_charts"):
        st.markdown("---")
        st.markdown("### 🔗 Análise de Correlações")
        
        # Preparar dados numéricos para correlação
        numeric_cols = [
            'duration_minutes', 'total_messages', 'secretary_messages',
            'patient_messages', 'num_interactions', 'agendamento_keywords',
            'preco_keywords', 'patient_questions', 'secretary_questions'
        ]
        
        # Criar variável binária para sucesso
        correlation_df = filtered_df[numeric_cols].copy()
        correlation_df['success'] = (filtered_df['chat_type'] == 'success').astype(int)
        
        # Calcular matriz de correlação
        corr_matrix = correlation_df.corr()
        
        # Heatmap de correlação
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.round(2).values,
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig_corr.update_layout(
            title="Matriz de Correlação entre Variáveis",
            height=600,
            margin=dict(l=100, r=50, t=80, b=100)
        )
        
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Top correlações com sucesso
        success_corr = corr_matrix['success'].abs().sort_values(ascending=False)[1:]  # Remover autocorrelação
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Fatores Mais Correlacionados com Sucesso")
            for var, corr in success_corr.head(5).items():
                direction = "positiva" if corr_matrix.loc['success', var] > 0 else "negativa"
                st.markdown(f"- **{var}**: {corr:.3f} ({direction})")
        
        with col2:
            # Gráfico de barras das correlações
            fig_corr_bar = go.Figure(go.Bar(
                x=success_corr.head(8).values,
                y=success_corr.head(8).index,
                orientation='h',
                marker_color=colors['info']
            ))
            
            fig_corr_bar.update_layout(
                title="Top Correlações com Sucesso",
                xaxis_title="Correlação (valor absoluto)",
                height=300
            )
            
            st.plotly_chart(fig_corr_bar, use_container_width=True)
    
    # === ANÁLISE ESTATÍSTICA ===
    st.markdown("---")
    st.markdown("### 📊 Análise Estatística")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Estatísticas Descritivas")
        
        # Tabela de estatísticas por tipo
        stats_table = filtered_df.groupby('chat_type')[numeric_cols[:4]].agg(['mean', 'median', 'std']).round(2)
        st.dataframe(stats_table, use_container_width=True)
    
    with col2:
        st.markdown("#### 🔍 Testes de Diferença")
        
        if len(filtered_df[filtered_df['chat_type'] == 'success']) > 0 and len(filtered_df[filtered_df['chat_type'] == 'fail']) > 0:
            
            success_data = filtered_df[filtered_df['chat_type'] == 'success']
            fail_data = filtered_df[filtered_df['chat_type'] == 'fail']
            
            # Comparações simples (média)
            comparisons = []
            for col in ['duration_minutes', 'total_messages', 'agendamento_keywords']:
                success_mean = success_data[col].mean()
                fail_mean = fail_data[col].mean()
                diff_percent = ((success_mean - fail_mean) / fail_mean * 100) if fail_mean != 0 else 0
                
                comparisons.append({
                    'Métrica': col.replace('_', ' ').title(),
                    'Sucesso': f"{success_mean:.1f}",
                    'Falha': f"{fail_mean:.1f}",
                    'Diferença %': f"{diff_percent:+.1f}%"
                })
            
            comparison_df = pd.DataFrame(comparisons)
            st.dataframe(comparison_df, use_container_width=True)
    
    # === INSIGHTS ESPECÍFICOS ===
    st.markdown("---")
    st.markdown("### 💡 Insights da Análise")
    
    # Gerar insights baseados nos dados filtrados
    insights = []
    
    if len(filtered_df) > 0:
        success_df = filtered_df[filtered_df['chat_type'] == 'success']
        fail_df = filtered_df[filtered_df['chat_type'] == 'fail']
        
        if len(success_df) > 0 and len(fail_df) > 0:
            # Insight sobre duração
            success_duration = success_df['duration_minutes'].mean()
            fail_duration = fail_df['duration_minutes'].mean()
            
            if success_duration > fail_duration * 1.2:
                insights.append(f"⏱️ **Tempo Importa**: Conversas bem-sucedidas duram em média {success_duration:.1f} minutos, {((success_duration/fail_duration-1)*100):.0f}% mais que as falhas")
            
            # Insight sobre mensagens
            success_messages = success_df['total_messages'].mean()
            fail_messages = fail_df['total_messages'].mean()
            
            if success_messages > fail_messages * 1.3:
                insights.append(f"💬 **Engajamento**: Sucessos têm {success_messages:.1f} mensagens vs {fail_messages:.1f} das falhas - mais conversa = mais conversão")
            
            # Insight sobre palavras-chave
            success_agend = success_df['agendamento_keywords'].mean()
            fail_agend = fail_df['agendamento_keywords'].mean()
            
            if success_agend > fail_agend * 1.5:
                insights.append(f"🎯 **Vocabulário de Sucesso**: {success_agend:.1f} palavras de agendamento em sucessos vs {fail_agend:.1f} em falhas")
    
    if insights:
        for insight in insights:
            st.info(insight)
    else:
        st.info("📊 Continue explorando os filtros para descobrir padrões específicos!")
    
    # === EXPLORADOR DE CONVERSAS ===
    st.markdown("---")
    st.markdown("### 🔎 Explorador de Conversas")
    
    # Tabela interativa com as conversas
    st.markdown("#### 📋 Lista de Conversas Analisadas")
    
    # Preparar dados para exibição
    display_df = filtered_df.copy()
    display_df['Duração'] = display_df['duration_minutes'].round(1).astype(str) + ' min'
    display_df['Taxa Secretária'] = (display_df['secretary_messages'] / display_df['total_messages']).round(2)
    display_df['Tipo'] = display_df['chat_type'].map({'success': '✅ Sucesso', 'fail': '❌ Falha'})
    
    # Colunas para exibir
    display_columns = [
        'chat_name', 'Tipo', 'Duração', 'total_messages', 
        'Taxa Secretária', 'agendamento_keywords', 'preco_keywords'
    ]
    
    display_names = [
        'Nome da Conversa', 'Resultado', 'Duração', 'Total Mensagens',
        'Taxa Secretária', 'Palavras Agendamento', 'Palavras Preço'
    ]
    
    # Renomear colunas para exibição
    show_df = display_df[display_columns].copy()
    show_df.columns = display_names
    
    # Permitir seleção de conversa para detalhes
    selected_rows = st.dataframe(
        show_df,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row"
    )
    
    # Mostrar detalhes da conversa selecionada
    if selected_rows and len(selected_rows.selection.rows) > 0:
        selected_idx = selected_rows.selection.rows[0]
        selected_conversation = filtered_df.iloc[selected_idx]
        
        st.markdown("#### 🔍 Detalhes da Conversa Selecionada")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Nome", selected_conversation['chat_name'])
            st.metric("Tipo", selected_conversation['chat_type'].title())
            st.metric("Duração", f"{selected_conversation['duration_minutes']:.1f} min")
        
        with col2:
            st.metric("Total Mensagens", int(selected_conversation['total_messages']))
            st.metric("Mensagens Secretária", int(selected_conversation['secretary_messages']))
            st.metric("Mensagens Paciente", int(selected_conversation['patient_messages']))
        
        with col3:
            st.metric("Interações", int(selected_conversation['num_interactions']))
            st.metric("Palavras Agendamento", int(selected_conversation['agendamento_keywords']))
            st.metric("Palavras Preço", int(selected_conversation['preco_keywords']))
    
    # === EXPORTAÇÃO ===
    if feature_enabled("export_data"):
        st.markdown("---")
        st.markdown("### 📤 Exportação de Dados")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Exportar Dados Filtrados", use_container_width=True):
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Baixar CSV",
                    data=csv,
                    file_name="analise_conversas_filtradas.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📈 Exportar Estatísticas", use_container_width=True):
                stats_df = filtered_df.groupby('chat_type')[numeric_cols].describe()
                stats_csv = stats_df.to_csv()
                st.download_button(
                    label="⬇️ Baixar Estatísticas",
                    data=stats_csv,
                    file_name="estatisticas_analise.csv",
                    mime="text/csv"
                )
        
        with col3:
            if st.button("💡 Exportar Insights", use_container_width=True):
                insights_text = "\n".join([f"- {insight}" for insight in insights])
                st.download_button(
                    label="⬇️ Baixar Insights",
                    data=insights_text,
                    file_name="insights_analise.txt",
                    mime="text/plain"
                )
    
    # Aviso sobre dados de exemplo
    if is_sample_data:
        st.markdown("---")
        st.info("""
        📝 **Dados de Demonstração**
        
        Esta análise usa dados sintéticos para demonstração. 
        Para análise real, adicione seus arquivos de conversa do WhatsApp.
        """)

def show_conversation_details(conversation_data):
    """
    Mostra detalhes de uma conversa específica
    """
    st.subheader(f"📱 {conversation_data['chat_name']}")
    
    # Métricas da conversa
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Resultado", conversation_data['chat_type'].title())
        st.metric("Duração", f"{conversation_data['duration_minutes']:.1f} min")
    
    with col2:
        st.metric("Total Mensagens", int(conversation_data['total_messages']))
        st.metric("Interações", int(conversation_data['num_interactions']))
    
    with col3:
        st.metric("Agendamento", int(conversation_data['agendamento_keywords']))
        st.metric("Preço", int(conversation_data['preco_keywords']))
    
    # Gráfico de distribuição de mensagens
    categories = ['Secretária', 'Paciente']
    values = [conversation_data['secretary_messages'], conversation_data['patient_messages']]
    
    fig = go.Figure(data=[go.Pie(
        labels=categories,
        values=values,
        hole=0.3
    )])
    
    fig.update_layout(
        title="Distribuição de Mensagens",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    show_analysis()
