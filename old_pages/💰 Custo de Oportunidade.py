import streamlit as st
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))

from modules.utils import load_data, calculate_opportunity_cost, format_currency, format_percentage
from modules.constants import VALOR_MEDIO_CONSULTA, LEADS_DIARIOS, PRIMARY_COLOR, SECONDARY_COLOR

st.set_page_config(page_title="Custo de Oportunidade", page_icon="💰", layout="wide")

st.title("💰 Custo de Oportunidade")
st.markdown("Análise do impacto financeiro dos leads não convertidos")

# Load data
df = load_data()

if df is None:
    st.error("❌ Dados não encontrados. Execute primeiro o script de extração de features.")
    st.stop()

# Sidebar for parameters
st.sidebar.header("⚙️ Parâmetros")

valor_consulta = st.sidebar.number_input(
    "Valor médio da consulta (R$)",
    min_value=0.0,
    value=float(VALOR_MEDIO_CONSULTA),
    step=50.0,
    help="Valor médio em reais de uma consulta bem-sucedida"
)

leads_diarios = st.sidebar.number_input(
    "Leads diários",
    min_value=1,
    value=LEADS_DIARIOS,
    step=1,
    help="Número médio de leads recebidos por dia"
)

dias_uteis_mes = st.sidebar.number_input(
    "Dias úteis por mês",
    min_value=1,
    value=20,
    step=1,
    help="Número de dias úteis considerados por mês"
)

dias_uteis_ano = st.sidebar.number_input(
    "Dias úteis por ano",
    min_value=1,
    value=240,
    step=1,
    help="Número de dias úteis considerados por ano"
)

# Calculate opportunity cost with custom parameters
opportunity_cost = calculate_opportunity_cost(df, valor_consulta, leads_diarios)

if opportunity_cost is None:
    st.error("❌ Erro ao calcular custo de oportunidade.")
    st.stop()

# Recalculate with custom parameters
custo_oportunidade_diario = (leads_diarios * opportunity_cost['failure_rate']) * valor_consulta
custo_oportunidade_semanal = custo_oportunidade_diario * 5
custo_oportunidade_mensal = custo_oportunidade_diario * dias_uteis_mes
custo_oportunidade_anual = custo_oportunidade_diario * dias_uteis_ano

# Main metrics
st.subheader("📊 Métricas Principais")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Taxa de Conversão",
        value=format_percentage(opportunity_cost['success_rate']),
        delta=f"{opportunity_cost['success_count']} sucessos",
        help="Porcentagem de leads que se convertem em agendamentos"
    )

with col2:
    st.metric(
        label="Taxa de Falha",
        value=format_percentage(opportunity_cost['failure_rate']),
        delta=f"{opportunity_cost['fail_count']} falhas",
        delta_color="inverse",
        help="Porcentagem de leads que não se convertem"
    )

with col3:
    st.metric(
        label="Leads Perdidos/Dia",
        value=f"{leads_diarios * opportunity_cost['failure_rate']:.1f}",
        help="Número médio de leads perdidos por dia"
    )

with col4:
    st.metric(
        label="Receita Potencial/Lead",
        value=format_currency(valor_consulta),
        help="Valor médio de cada lead convertido"
    )

# Cost breakdown
st.markdown("---")
st.subheader("💸 Breakdown do Custo de Oportunidade")

cost_data = {
    'Período': ['Diário', 'Semanal', 'Mensal', 'Anual'],
    'Custo': [
        custo_oportunidade_diario,
        custo_oportunidade_semanal,
        custo_oportunidade_mensal,
        custo_oportunidade_anual
    ],
    'Leads Perdidos': [
        leads_diarios * opportunity_cost['failure_rate'],
        leads_diarios * opportunity_cost['failure_rate'] * 5,
        leads_diarios * opportunity_cost['failure_rate'] * dias_uteis_mes,
        leads_diarios * opportunity_cost['failure_rate'] * dias_uteis_ano
    ]
}

col1, col2 = st.columns(2)

with col1:
    # Bar chart for costs
    fig_cost = px.bar(
        x=cost_data['Período'],
        y=cost_data['Custo'],
        title="Custo de Oportunidade por Período",
        labels={'x': 'Período', 'y': 'Custo (R$)'},
        color=cost_data['Custo'],
        color_continuous_scale='Reds'
    )
    
    fig_cost.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_cost, use_container_width=True)

with col2:
    # Pie chart for cost distribution
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Receita Atual', 'Oportunidade Perdida'],
        values=[
            custo_oportunidade_anual / opportunity_cost['failure_rate'] * opportunity_cost['success_rate'],
            custo_oportunidade_anual
        ],
        hole=0.4,
        marker_colors=['#28a745', '#dc3545']
    )])
    
    fig_pie.update_layout(
        title="Receita Atual vs Oportunidade Perdida (Anual)",
        height=400
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

# Detailed cost table
st.subheader("📋 Tabela Detalhada de Custos")

cost_df = pd.DataFrame({
    'Período': cost_data['Período'],
    'Leads Perdidos': [f"{x:.1f}" for x in cost_data['Leads Perdidos']],
    'Custo de Oportunidade': [format_currency(x) for x in cost_data['Custo']],
    'Receita Potencial Total': [
        format_currency(x / opportunity_cost['failure_rate']) for x in cost_data['Custo']
    ]
})

st.dataframe(cost_df, use_container_width=True)

# Scenario analysis
st.markdown("---")
st.subheader("🎯 Análise de Cenários")

st.markdown("**Simule diferentes taxas de conversão para ver o impacto no custo de oportunidade:**")

col1, col2 = st.columns(2)

with col1:
    target_conversion_rate = st.slider(
        "Taxa de conversão alvo (%)",
        min_value=0,
        max_value=100,
        value=int(opportunity_cost['success_rate'] * 100),
        step=5,
        help="Simule uma taxa de conversão diferente"
    ) / 100
    
    target_failure_rate = 1 - target_conversion_rate
    target_cost_daily = (leads_diarios * target_failure_rate) * valor_consulta
    target_cost_monthly = target_cost_daily * dias_uteis_mes
    target_cost_annual = target_cost_daily * dias_uteis_ano
    
    # Calculate savings
    savings_daily = custo_oportunidade_diario - target_cost_daily
    savings_monthly = custo_oportunidade_mensal - target_cost_monthly
    savings_annual = custo_oportunidade_anual - target_cost_annual

with col2:
    st.markdown("### 💡 Impacto da Melhoria")
    
    st.metric(
        "Economia Diária",
        format_currency(savings_daily),
        delta=f"{format_percentage(savings_daily/custo_oportunidade_diario if custo_oportunidade_diario > 0 else 0)} de redução"
    )
    
    st.metric(
        "Economia Mensal",
        format_currency(savings_monthly),
        delta=f"{format_percentage(savings_monthly/custo_oportunidade_mensal if custo_oportunidade_mensal > 0 else 0)} de redução"
    )
    
    st.metric(
        "Economia Anual",
        format_currency(savings_annual),
        delta=f"{format_percentage(savings_annual/custo_oportunidade_anual if custo_oportunidade_anual > 0 else 0)} de redução"
    )

# Comparison chart
scenario_data = {
    'Cenário': ['Atual', 'Meta'],
    'Taxa de Conversão': [opportunity_cost['success_rate'], target_conversion_rate],
    'Custo Anual': [custo_oportunidade_anual, target_cost_annual]
}

fig_scenario = px.bar(
    x=scenario_data['Cenário'],
    y=scenario_data['Custo Anual'],
    title="Comparação: Cenário Atual vs Meta",
    labels={'x': 'Cenário', 'y': 'Custo Anual (R$)'},
    color=scenario_data['Custo Anual'],
    color_continuous_scale='RdYlGn_r'
)

fig_scenario.update_layout(height=400, showlegend=False)
st.plotly_chart(fig_scenario, use_container_width=True)

# ROI Analysis
st.markdown("---")
st.subheader("📈 Análise de ROI")

st.markdown("""
**Calcule o retorno sobre investimento (ROI) de melhorias no processo de conversão:**
""")

col1, col2 = st.columns(2)

with col1:
    investment_amount = st.number_input(
        "Investimento em melhorias (R$)",
        min_value=0.0,
        value=10000.0,
        step=1000.0,
        help="Valor a ser investido em treinamento, ferramentas, etc."
    )
    
    improvement_period = st.selectbox(
        "Período para calcular ROI",
        options=[1, 3, 6, 12],
        index=3,
        format_func=lambda x: f"{x} mês{'es' if x > 1 else ''}"
    )

with col2:
    if investment_amount > 0:
        roi_savings = savings_monthly * improvement_period
        roi_percentage = ((roi_savings - investment_amount) / investment_amount) * 100
        payback_months = investment_amount / savings_monthly if savings_monthly > 0 else float('inf')
        
        st.metric(
            "ROI",
            f"{roi_percentage:.1f}%",
            help="Retorno sobre investimento no período selecionado"
        )
        
        st.metric(
            "Payback",
            f"{payback_months:.1f} meses" if payback_months != float('inf') else "N/A",
            help="Tempo para recuperar o investimento"
        )
        
        st.metric(
            "Economia Total",
            format_currency(roi_savings),
            help=f"Economia total em {improvement_period} mês{'es' if improvement_period > 1 else ''}"
        )

# Action items
st.markdown("---")
st.subheader("🎯 Plano de Ação")

if opportunity_cost['failure_rate'] > 0.6:
    st.error("🚨 **CRÍTICO**: Taxa de falha muito alta (>60%). Ação imediata necessária!")
elif opportunity_cost['failure_rate'] > 0.4:
    st.warning("⚠️ **ATENÇÃO**: Taxa de falha elevada (>40%). Melhorias recomendadas.")
else:
    st.success("✅ **BOM**: Taxa de falha dentro do esperado (<40%).")

recommendations = []

if opportunity_cost['failure_rate'] > 0.5:
    recommendations.append("🔄 Revisar processo de atendimento inicial")
    recommendations.append("📚 Investir em treinamento da equipe")

if custo_oportunidade_mensal > 5000:
    recommendations.append("💰 Priorizar melhorias - alto impacto financeiro")

if df[df['chat_type'] == 'success']['secretary_questions'].mean() > df[df['chat_type'] == 'fail']['secretary_questions'].mean():
    recommendations.append("❓ Incentivar mais perguntas da secretária")

if df[df['chat_type'] == 'success']['duration_minutes'].mean() > df[df['chat_type'] == 'fail']['duration_minutes'].mean():
    recommendations.append("⏱️ Investir mais tempo nas conversas")

if recommendations:
    st.markdown("### 📝 Recomendações:")
    for rec in recommendations:
        st.markdown(f"- {rec}")

# Export functionality
st.markdown("---")
if st.button("📊 Exportar Análise de Custo"):
    export_data = {
        'Métrica': [
            'Taxa de Conversão',
            'Taxa de Falha',
            'Custo Diário',
            'Custo Semanal',
            'Custo Mensal',
            'Custo Anual',
            'Leads Diários',
            'Valor por Consulta'
        ],
        'Valor': [
            format_percentage(opportunity_cost['success_rate']),
            format_percentage(opportunity_cost['failure_rate']),
            format_currency(custo_oportunidade_diario),
            format_currency(custo_oportunidade_semanal),
            format_currency(custo_oportunidade_mensal),
            format_currency(custo_oportunidade_anual),
            leads_diarios,
            format_currency(valor_consulta)
        ]
    }
    
    export_df = pd.DataFrame(export_data)
    csv = export_df.to_csv(index=False)
    
    st.download_button(
        label="💾 Download Relatório CSV",
        data=csv,
        file_name="analise_custo_oportunidade.csv",
        mime="text/csv"
    )

