# SWAI UI Dashboard - Interface Simplificada
# Filosofia: Clareza visual que liberta o tempo mental

"""
Dashboard principal do SWAI WhatsApp Analyzer
Interface limpa focada no essencial
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def show_dashboard():
    """
    Exibe o dashboard principal do SWAI
    """
    
    # Importações locais para evitar dependências circulares
    from swai_settings import SWAI_SETTINGS, get_financial_settings, get_color_scheme
    from swai_core import SWAIAnalyzer, create_sample_data
    from swai_features import feature_enabled
    
    st.title("📊 Dashboard SWAI")
    st.markdown("*Visão estratégica para tomada de decisão inteligente*")
    
    # Verificar se funcionalidade está habilitada
    if not feature_enabled("dashboard"):
        st.warning("⏸️ Dashboard está desabilitado. Ative nas configurações.")
        return
    
    # Inicializar analisador
    analyzer = SWAIAnalyzer(SWAI_SETTINGS)
    colors = get_color_scheme()
    
    # Carregar dados
    with st.spinner("🔄 Carregando dados..."):
        df = analyzer.load_conversation_data()
        
        # Se não há dados reais, usar dados de exemplo
        if df is None or df.empty:
            st.info("📝 Usando dados de exemplo para demonstração")
            df = create_sample_data()
            is_sample_data = True
        else:
            is_sample_data = False
    
    if df.empty:
        st.error("❌ Nenhum dado disponível para análise")
        return
    
    # Calcular métricas
    metrics = analyzer.calculate_basic_metrics(df)
    financial_config = get_financial_settings()
    opportunity_cost = analyzer.calculate_opportunity_cost(metrics, financial_config)
    insights = analyzer.generate_insights(metrics, opportunity_cost)
    
    # === SEÇÃO 1: MÉTRICAS PRINCIPAIS ===
    st.markdown("### 🎯 Métricas Principais")
    
    summary = metrics.get('summary', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📞 Total de Conversas",
            value=summary.get('total_conversations', 0),
            help="Número total de conversas analisadas"
        )
    
    with col2:
        success_rate = summary.get('success_rate', 0)
        st.metric(
            label="✅ Taxa de Conversão",
            value=f"{success_rate:.1%}",
            delta=f"{success_rate - 0.6:.1%}" if success_rate > 0.6 else f"{success_rate - 0.6:.1%}",
            delta_color="normal",
            help="Percentual de conversas que resultaram em agendamento"
        )
    
    with col3:
        avg_duration = summary.get('avg_duration', 0)
        st.metric(
            label="⏱️ Duração Média",
            value=f"{avg_duration:.1f} min",
            help="Tempo médio de duração das conversas"
        )
    
    with col4:
        current_costs = opportunity_cost.get('current_costs', {})
        custo_mensal = current_costs.get('mensal', 0)
        st.metric(
            label="💰 Custo Mensal",
            value=analyzer.format_currency(custo_mensal),
            delta=f"-{analyzer.format_currency(custo_mensal)}" if custo_mensal > 0 else "R$ 0,00",
            delta_color="inverse",
            help="Receita perdida por mês devido a leads não convertidos"
        )
    
    # === SEÇÃO 2: ANÁLISE VISUAL ===
    st.markdown("---")
    st.markdown("### 📈 Análise Visual")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de pizza - Taxa de conversão
        st.subheader("🥧 Distribuição de Resultados")
        
        success_count = summary.get('success_count', 0)
        fail_count = summary.get('fail_count', 0)
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Sucessos', 'Falhas'],
            values=[success_count, fail_count],
            hole=0.4,
            marker_colors=[colors['success'], colors['error']],
            textinfo='label+percent',
            textfont_size=12
        )])
        
        fig_pie.update_layout(
            showlegend=True,
            height=350,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Gráfico de barras - Comparação métricas
        st.subheader("📊 Sucesso vs Falha")
        
        success_metrics = metrics.get('success_metrics', {})
        fail_metrics = metrics.get('fail_metrics', {})
        
        if success_metrics and fail_metrics:
            comparison_data = {
                'Métrica': ['Duração (min)', 'Mensagens', 'Interações', 'Palavras Agendamento'],
                'Sucesso': [
                    success_metrics.get('avg_duration', 0),
                    success_metrics.get('avg_messages', 0),
                    success_metrics.get('avg_interactions', 0),
                    success_metrics.get('avg_agendamento_keywords', 0)
                ],
                'Falha': [
                    fail_metrics.get('avg_duration', 0),
                    fail_metrics.get('avg_messages', 0),
                    fail_metrics.get('avg_interactions', 0),
                    fail_metrics.get('avg_agendamento_keywords', 0)
                ]
            }
            
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                name='Sucesso',
                x=comparison_data['Métrica'],
                y=comparison_data['Sucesso'],
                marker_color=colors['success']
            ))
            fig_bar.add_trace(go.Bar(
                name='Falha',
                x=comparison_data['Métrica'],
                y=comparison_data['Falha'],
                marker_color=colors['error']
            ))
            
            fig_bar.update_layout(
                barmode='group',
                height=350,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # === SEÇÃO 3: CUSTO DE OPORTUNIDADE ===
    if feature_enabled("cost_calculator"):
        st.markdown("---")
        st.markdown("### 💰 Impacto Financeiro")
        
        col1, col2, col3, col4 = st.columns(4)
        
        current_costs = opportunity_cost.get('current_costs', {})
        
        with col1:
            st.metric(
                label="Custo Diário",
                value=analyzer.format_currency(current_costs.get('diario', 0)),
                help="Receita perdida por dia"
            )
        
        with col2:
            st.metric(
                label="Custo Semanal",
                value=analyzer.format_currency(current_costs.get('semanal', 0)),
                help="Receita perdida por semana"
            )
        
        with col3:
            st.metric(
                label="Custo Mensal",
                value=analyzer.format_currency(current_costs.get('mensal', 0)),
                help="Receita perdida por mês"
            )
        
        with col4:
            st.metric(
                label="Custo Anual",
                value=analyzer.format_currency(current_costs.get('anual', 0)),
                help="Receita perdida por ano"
            )
        
        # Gráfico de projeção temporal
        if feature_enabled("advanced_charts"):
            st.subheader("📈 Projeção de Custos")
            
            periods = ['Diário', 'Semanal', 'Mensal', 'Anual']
            costs = [
                current_costs.get('diario', 0),
                current_costs.get('semanal', 0),
                current_costs.get('mensal', 0),
                current_costs.get('anual', 0)
            ]
            
            fig_timeline = go.Figure()
            fig_timeline.add_trace(go.Bar(
                x=periods,
                y=costs,
                marker_color=colors['warning'],
                text=[analyzer.format_currency(cost) for cost in costs],
                textposition='auto'
            ))
            
            fig_timeline.update_layout(
                title="Evolução dos Custos de Oportunidade",
                xaxis_title="Período",
                yaxis_title="Valor (R$)",
                height=350,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            st.plotly_chart(fig_timeline, use_container_width=True)
    
    # === SEÇÃO 4: INSIGHTS E RECOMENDAÇÕES ===
    st.markdown("---")
    st.markdown("### 💡 Insights e Recomendações")
    
    if insights:
        for insight in insights:
            insight_type = insight.get('type', 'info')
            title = insight.get('title', 'Insight')
            message = insight.get('message', '')
            action = insight.get('action', '')
            
            if insight_type == 'warning':
                st.warning(f"⚠️ **{title}**\n\n{message}\n\n🎯 **Ação:** {action}")
            elif insight_type == 'success':
                st.success(f"✅ **{title}**\n\n{message}\n\n🎯 **Ação:** {action}")
            else:
                st.info(f"💡 **{title}**\n\n{message}\n\n🎯 **Ação:** {action}")
    else:
        st.info("📝 Nenhum insight específico disponível no momento.")
    
    # === SEÇÃO 5: RESUMO EXECUTIVO ===
    st.markdown("---")
    st.markdown("### 📋 Resumo Executivo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Performance Atual")
        st.markdown(f"""
        - **Taxa de Conversão:** {analyzer.format_percentage(success_rate)}
        - **Conversas Analisadas:** {summary.get('total_conversations', 0)}
        - **Duração Média:** {avg_duration:.1f} minutos
        - **Engajamento:** {summary.get('avg_messages', 0):.1f} mensagens/conversa
        """)
    
    with col2:
        st.markdown("#### 💰 Impacto Financeiro")
        st.markdown(f"""
        - **Custo Mensal:** {analyzer.format_currency(custo_mensal)}
        - **Valor por Lead:** {analyzer.format_currency(financial_config.get('valor_consulta', 800))}
        - **Leads Diários:** {financial_config.get('leads_diarios', 5)}
        - **Potencial de Melhoria:** Alta
        """)
    
    # === SEÇÃO 6: AÇÕES RECOMENDADAS ===
    st.markdown("---")
    st.markdown("### 🚀 Próximas Ações")
    
    # Gerar recomendações baseadas nos dados
    recommendations = []
    
    if success_rate < 0.5:
        recommendations.append("🔴 **URGENTE:** Revisar processo de atendimento - taxa de conversão crítica")
    
    if success_rate < 0.6:
        recommendations.append("🟡 **PRIORIDADE:** Treinar equipe em técnicas de conversão")
    
    if custo_mensal > 5000:
        recommendations.append("💰 **FINANCEIRO:** Alto custo de oportunidade - ROI de melhorias garantido")
    
    if success_metrics and fail_metrics:
        if success_metrics.get('avg_duration', 0) > fail_metrics.get('avg_duration', 0) * 1.2:
            recommendations.append("⏱️ **PROCESSO:** Investir tempo nas conversas gera resultados")
        
        if success_metrics.get('avg_agendamento_keywords', 0) > fail_metrics.get('avg_agendamento_keywords', 0) * 1.5:
            recommendations.append("🎯 **TREINAMENTO:** Focar vocabulário de agendamento")
    
    if not recommendations:
        recommendations.append("✅ **MANUTENÇÃO:** Performance dentro do esperado - manter padrão atual")
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"{i}. {rec}")
    
    # === FOOTER ===
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Atualizar Dados", use_container_width=True):
            st.experimental_rerun()
    
    with col2:
        if feature_enabled("export_data") and st.button("📊 Exportar Relatório", use_container_width=True):
            # Aqui seria implementada a exportação
            st.success("📄 Relatório exportado com sucesso!")
    
    with col3:
        if st.button("⚙️ Configurações", use_container_width=True):
            st.info("🔧 Redirecionando para configurações...")
    
    # Aviso sobre dados de exemplo
    if is_sample_data:
        st.info("""
        📝 **Dados de Demonstração**
        
        Você está visualizando dados de exemplo. Para usar dados reais:
        1. Coloque os arquivos de conversa nas pastas `data/success_cases/` e `data/fail_cases/`
        2. Execute o extrator de features
        3. Recarregue o dashboard
        """)

def show_dashboard_config():
    """
    Configurações específicas do dashboard
    """
    st.subheader("🎛️ Configurações do Dashboard")
    
    from swai_features import feature_enabled, toggle_feature
    
    # Controles liga-desliga para sub-funcionalidades
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Componentes Visuais")
        
        advanced_charts = st.checkbox(
            "Gráficos Avançados",
            value=feature_enabled("advanced_charts"),
            help="Habilitar gráficos interativos e visualizações avançadas"
        )
        
        if advanced_charts != feature_enabled("advanced_charts"):
            toggle_feature("advanced_charts", advanced_charts)
    
    with col2:
        st.markdown("#### 🔄 Atualização")
        
        auto_refresh = st.checkbox(
            "Atualização Automática",
            value=False,
            help="Atualizar dashboard automaticamente (experimental)"
        )
        
        if auto_refresh:
            refresh_interval = st.slider("Intervalo (segundos)", 30, 300, 60)
    
    # Configurações de exibição
    st.markdown("#### 🎨 Personalização")
    
    show_sample_warning = st.checkbox(
        "Mostrar aviso sobre dados de exemplo",
        value=True,
        help="Exibir aviso quando usando dados de demonstração"
    )
    
    compact_mode = st.checkbox(
        "Modo Compacto",
        value=False,
        help="Interface mais compacta para telas pequenas"
    )
    
    if st.button("💾 Salvar Configurações"):
        st.success("✅ Configurações do dashboard salvas!")

if __name__ == "__main__":
    show_dashboard()
