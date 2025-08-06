# SWAI UI Cost - Calculadora de Custo de Oportunidade
# Filosofia: Transformar dados em decisões financeiras conscientes

"""
Módulo de cálculo e visualização de custo de oportunidade
Interface focada no impacto financeiro das melhorias
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def show_cost_calculator():
    """
    Exibe a calculadora de custo de oportunidade
    """
    
    from swai_settings import SWAI_SETTINGS, get_financial_settings, update_financial_settings, get_color_scheme
    from swai_core import SWAIAnalyzer, create_sample_data
    from swai_features import feature_enabled
    
    st.title("💰 Custo de Oportunidade")
    st.markdown("*Quantificando o valor das melhorias no atendimento*")
    
    # Verificar se funcionalidade está habilitada
    if not feature_enabled("cost_calculator"):
        st.warning("⏸️ Calculadora de custo está desabilitada. Ative nas configurações.")
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
        st.error("❌ Nenhum dado disponível para cálculo")
        return
    
    # === CONFIGURAÇÕES FINANCEIRAS ===
    st.markdown("### ⚙️ Parâmetros Financeiros")
    
    financial_config = get_financial_settings()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        valor_consulta = st.number_input(
            "💵 Valor Médio da Consulta (R$)",
            min_value=100.0,
            max_value=5000.0,
            value=financial_config['valor_consulta'],
            step=50.0,
            help="Valor médio que cada consulta gera de receita"
        )
    
    with col2:
        leads_diarios = st.number_input(
            "📞 Leads por Dia",
            min_value=1,
            max_value=50,
            value=financial_config['leads_diarios'],
            step=1,
            help="Número médio de leads que entram em contato por dia"
        )
    
    with col3:
        dias_uteis_mes = st.number_input(
            "📅 Dias Úteis por Mês",
            min_value=15,
            max_value=25,
            value=financial_config['dias_uteis_mes'],
            step=1,
            help="Número de dias úteis trabalhados por mês"
        )
    
    # Atualizar configurações se mudaram
    if (valor_consulta != financial_config['valor_consulta'] or 
        leads_diarios != financial_config['leads_diarios']):
        update_financial_settings(valor_consulta, leads_diarios)
        financial_config = get_financial_settings()
    
    # === MÉTRICAS ATUAIS ===
    metrics = analyzer.calculate_basic_metrics(df)
    opportunity_cost = analyzer.calculate_opportunity_cost(metrics, {
        'valor_consulta': valor_consulta,
        'leads_diarios': leads_diarios,
        'dias_uteis_mes': dias_uteis_mes,
        'dias_uteis_ano': dias_uteis_mes * 12
    })
    
    st.markdown("---")
    st.markdown("### 📊 Situação Atual")
    
    summary = metrics.get('summary', {})
    current_costs = opportunity_cost.get('current_costs', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        success_rate = summary.get('success_rate', 0)
        st.metric(
            label="Taxa de Conversão Atual",
            value=f"{success_rate:.1%}",
            delta=f"{success_rate - 0.6:.1%}" if success_rate != 0.6 else None,
            help="Percentual atual de conversões"
        )
    
    with col2:
        st.metric(
            label="Leads Perdidos/Dia",
            value=f"{leads_diarios * (1 - success_rate):.1f}",
            delta=f"-{leads_diarios * (1 - success_rate):.1f}",
            delta_color="inverse",
            help="Número de leads perdidos por dia"
        )
    
    with col3:
        st.metric(
            label="Custo por Lead Perdido",
            value=analyzer.format_currency(valor_consulta),
            help="Valor de cada oportunidade perdida"
        )
    
    with col4:
        st.metric(
            label="Impacto Diário",
            value=analyzer.format_currency(current_costs.get('diario', 0)),
            delta=f"-{analyzer.format_currency(current_costs.get('diario', 0))}",
            delta_color="inverse",
            help="Receita perdida por dia"
        )
    
    # === SIMULADOR SIMPLES ===
    st.markdown("---")
    st.markdown("### 🎮 Simulador de Melhorias")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Meta de Melhoria")
        
        target_rate = st.slider(
            "Taxa de Conversão Desejada",
            min_value=success_rate,
            max_value=0.95,
            value=min(0.8, success_rate + 0.2),
            step=0.05,
            format="%.0%%"
        )
        
        improvement_needed = target_rate - success_rate
        additional_conversions = leads_diarios * improvement_needed
        monthly_gain = additional_conversions * valor_consulta * dias_uteis_mes
        annual_gain = monthly_gain * 12
        
    with col2:
        st.markdown("#### 💰 Potencial de Ganho")
        
        st.metric("Melhoria Necessária", f"+{improvement_needed:.1%}")
        st.metric("Conversões Extras/Dia", f"+{additional_conversions:.1f}")
        st.metric("Ganho Mensal", analyzer.format_currency(monthly_gain))
        st.metric("Ganho Anual", analyzer.format_currency(annual_gain))
    
    # === GRÁFICO DE IMPACTO ===
    if feature_enabled("advanced_charts"):
        st.markdown("---")
        st.markdown("### 📈 Visualização de Impacto")
        
        # Dados para o gráfico
        periods = ['Diário', 'Semanal', 'Mensal', 'Anual']
        current_losses = [
            current_costs.get('diario', 0),
            current_costs.get('semanal', 0),
            current_costs.get('mensal', 0),
            current_costs.get('anual', 0)
        ]
        
        potential_gains = [
            additional_conversions * valor_consulta,
            additional_conversions * valor_consulta * 5,
            monthly_gain,
            annual_gain
        ]
        
        # Criar gráfico comparativo
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Custo Atual',
            x=periods,
            y=current_losses,
            marker_color=colors['error'],
            text=[analyzer.format_currency(loss) for loss in current_losses],
            textposition='auto'
        ))
        
        fig.add_trace(go.Bar(
            name='Ganho Potencial',
            x=periods,
            y=potential_gains,
            marker_color=colors['success'],
            text=[analyzer.format_currency(gain) for gain in potential_gains],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Custo Atual vs Ganho Potencial",
            xaxis_title="Período",
            yaxis_title="Valor (R$)",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # === RECOMENDAÇÕES ===
    st.markdown("---")
    st.markdown("### 💡 Recomendações Financeiras")
    
    recommendations = []
    
    if current_costs.get('mensal', 0) > 5000:
        recommendations.append("🔴 **URGENTE**: Alto custo mensal - priorize melhorias imediatas")
    
    if success_rate < 0.5:
        recommendations.append("⚠️ **CRÍTICO**: Taxa de conversão muito baixa - ROI de melhorias garantido")
    
    if annual_gain > 50000:
        recommendations.append("💰 **OPORTUNIDADE**: Potencial de +R$ 50k anuais - investir em melhorias vale muito a pena")
    
    if improvement_needed < 0.1:
        recommendations.append("✅ **MANUTENÇÃO**: Performance boa - foque em manter qualidade")
    
    for rec in recommendations:
        st.info(rec)
    
    # === ROI DE MELHORIAS ===
    st.markdown("---")
    st.markdown("### 📊 ROI de Investimentos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💸 Custos de Melhoria")
        
        training_investment = st.number_input(
            "Investimento em Treinamento (R$)",
            min_value=0.0,
            value=3000.0,
            step=500.0
        )
        
        system_investment = st.number_input(
            "Investimento em Ferramentas (R$)",
            min_value=0.0,
            value=2000.0,
            step=500.0
        )
        
        total_investment = training_investment + system_investment
        
    with col2:
        st.markdown("#### 📈 Retorno Esperado")
        
        if total_investment > 0 and monthly_gain > 0:
            payback_months = total_investment / monthly_gain
            roi_percentage = ((annual_gain - total_investment) / total_investment) * 100
            
            st.metric("Payback (meses)", f"{payback_months:.1f}")
            st.metric("ROI Anual", f"{roi_percentage:.1f}%")
            
            if payback_months <= 6:
                st.success("🚀 Excelente! ROI em menos de 6 meses")
            elif payback_months <= 12:
                st.info("👍 Bom ROI - retorno em menos de 1 ano")
            else:
                st.warning("⚠️ ROI longo - considere outras estratégias")
    
    # === TABELA RESUMO ===
    st.markdown("---")
    st.markdown("### 📋 Resumo Executivo")
    
    summary_data = {
        'Métrica': [
            'Situação Atual',
            'Taxa de Conversão',
            'Custo Mensal Atual',
            'Meta de Conversão',
            'Ganho Mensal Potencial',
            'Investimento Sugerido',
            'ROI Esperado'
        ],
        'Valor': [
            f"{summary.get('total_conversations', 0)} conversas analisadas",
            f"{success_rate:.1%}",
            analyzer.format_currency(current_costs.get('mensal', 0)),
            f"{target_rate:.1%}",
            analyzer.format_currency(monthly_gain),
            analyzer.format_currency(total_investment),
            f"{roi_percentage:.1f}%" if 'roi_percentage' in locals() and roi_percentage > 0 else "N/A"
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    # === EXPORTAR ANÁLISE ===
    if feature_enabled("export_data"):
        st.markdown("---")
        
        if st.button("📤 Exportar Análise Financeira", use_container_width=True):
            # Criar relatório
            report = f"""
ANÁLISE FINANCEIRA - SWAI WHATSAPP ANALYZER
============================================

SITUAÇÃO ATUAL:
- Taxa de Conversão: {success_rate:.1%}
- Leads por Dia: {leads_diarios}
- Valor por Consulta: {analyzer.format_currency(valor_consulta)}
- Custo Diário: {analyzer.format_currency(current_costs.get('diario', 0))}
- Custo Mensal: {analyzer.format_currency(current_costs.get('mensal', 0))}
- Custo Anual: {analyzer.format_currency(current_costs.get('anual', 0))}

CENÁRIO DE MELHORIA:
- Meta de Conversão: {target_rate:.1%}
- Melhoria Necessária: +{improvement_needed:.1%}  
- Ganho Mensal: {analyzer.format_currency(monthly_gain)}
- Ganho Anual: {analyzer.format_currency(annual_gain)}

INVESTIMENTO E ROI:
- Investimento Total: {analyzer.format_currency(total_investment)}
- Payback: {payback_months:.1f} meses (se aplicável)
- ROI Anual: {roi_percentage:.1f}% (se aplicável)

RECOMENDAÇÕES:
"""
            for rec in recommendations:
                report += f"- {rec}\n"
            
            st.download_button(
                label="⬇️ Baixar Relatório",
                data=report,
                file_name="analise_financeira_swai.txt",
                mime="text/plain"
            )
    
    # Aviso sobre dados de exemplo
    if is_sample_data:
        st.markdown("---")
        st.info("""
        📝 **Dados de Demonstração**
        
        Esta análise usa dados sintéticos. Para cálculos precisos:
        - Configure os parâmetros financeiros corretos
        - Use dados reais de conversas
        - Monitore os resultados periodicamente
        """)

if __name__ == "__main__":
    show_cost_calculator()
