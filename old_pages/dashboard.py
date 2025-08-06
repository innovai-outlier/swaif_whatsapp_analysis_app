# Renomeado de 📊 Dashboard.py
# Código original deve ser movido para cá
import streamlit as st
import sys
import os
import plotly.express as px
import plotly.graph_objects as go

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))

from modules.utils import load_data, calculate_opportunity_cost, format_currency, format_percentage, get_summary_stats
from modules.constants import PRIMARY_COLOR, SECONDARY_COLOR

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# Custom CSS
st.markdown(f"""
<style>
    .metric-card {{
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid {SECONDARY_COLOR};
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }}
    
    .success-metric {{
        border-left-color: #28a745;
    }}
    
    .fail-metric {{
        border-left-color: #dc3545;
    }}
    
    .opportunity-metric {{
        border-left-color: {SECONDARY_COLOR};
    }}
</style>
""", unsafe_allow_html=True)

st.title("📊 Dashboard")
st.markdown("Visão geral dos dados e métricas principais")

# Load data
df = load_data()

if df is None:
    st.error("❌ Dados não encontrados. Execute primeiro o script de extração de features.")
    st.info("💡 Execute o comando: `python modules/extract_features_enhanced.py`")
    st.stop()

# Calculate metrics
opportunity_cost = calculate_opportunity_cost(df)
summary_stats = get_summary_stats(df)

# Main metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>📞 Total de Conversas</h3>
        <h2>{summary_stats['total_conversations']}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card success-metric">
        <h3>✅ Sucessos</h3>
        <h2>{summary_stats['success_conversations']}</h2>
        <p>{format_percentage(opportunity_cost['success_rate'])}</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card fail-metric">
        <h3>❌ Falhas</h3>
        <h2>{summary_stats['fail_conversations']}</h2>
        <p>{format_percentage(opportunity_cost['failure_rate'])}</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card opportunity-metric">
        <h3>💰 Custo Mensal</h3>
        <h2>{format_currency(opportunity_cost['custo_oportunidade_mensal'])}</h2>
        <p>Oportunidade perdida</p>
    </div>
    """, unsafe_allow_html=True)

# Charts section
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Taxa de Conversão")
    
    # Pie chart for success/fail ratio
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Sucesso', 'Falha'],
        values=[opportunity_cost['success_count'], opportunity_cost['fail_count']],
        hole=0.4,
        marker_colors=['#28a745', '#dc3545']
    )])
    
    fig_pie.update_layout(
        title="Distribuição de Sucessos vs Falhas",
        showlegend=True,
        height=400
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("⏱️ Duração das Conversas")
    
    # Box plot for conversation duration
    fig_box = px.box(
        df, 
        x='chat_type', 
        y='duration_minutes',
        color='chat_type',
        color_discrete_map={'success': '#28a745', 'fail': '#dc3545'},
        title="Duração das Conversas por Tipo"
    )
    
    fig_box.update_layout(
        xaxis_title="Tipo de Conversa",
        yaxis_title="Duração (minutos)",
        height=400
    )
    
    st.plotly_chart(fig_box, use_container_width=True)

# Detailed metrics
st.markdown("---")
st.subheader("📋 Métricas Detalhadas")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💬 Mensagens")
    
    metrics_data = {
        'Métrica': [
            'Média de Mensagens Totais',
            'Média de Mensagens da Secretária',
            'Média de Mensagens do Paciente',
            'Média de Interações'
        ],
        'Sucesso': [
            f"{df[df['chat_type'] == 'success']['total_messages'].mean():.1f}",
            f"{df[df['chat_type'] == 'success']['secretary_messages'].mean():.1f}",
            f"{df[df['chat_type'] == 'success']['patient_messages'].mean():.1f}",
            f"{df[df['chat_type'] == 'success']['num_interactions'].mean():.1f}"
        ],
        'Falha': [
            f"{df[df['chat_type'] == 'fail']['total_messages'].mean():.1f}",
            f"{df[df['chat_type'] == 'fail']['secretary_messages'].mean():.1f}",
            f"{df[df['chat_type'] == 'fail']['patient_messages'].mean():.1f}",
            f"{df[df['chat_type'] == 'fail']['num_interactions'].mean():.1f}"
        ]
    }
    
    st.table(metrics_data)

with col2:
    st.markdown("### 🔑 Palavras-chave")
    
    keywords_data = {
        'Métrica': [
            'Palavras de Agendamento',
            'Palavras de Preço',
            'Perguntas do Paciente',
            'Perguntas da Secretária'
        ],
        'Sucesso': [
            f"{df[df['chat_type'] == 'success']['agendamento_keywords'].mean():.1f}",
            f"{df[df['chat_type'] == 'success']['preco_keywords'].mean():.1f}",
            f"{df[df['chat_type'] == 'success']['patient_questions'].mean():.1f}",
            f"{df[df['chat_type'] == 'success']['secretary_questions'].mean():.1f}"
        ],
        'Falha': [
            f"{df[df['chat_type'] == 'fail']['agendamento_keywords'].mean():.1f}",
            f"{df[df['chat_type'] == 'fail']['preco_keywords'].mean():.1f}",
            f"{df[df['chat_type'] == 'fail']['patient_questions'].mean():.1f}",
            f"{df[df['chat_type'] == 'fail']['secretary_questions'].mean():.1f}"
        ]
    }
    
    st.table(keywords_data)

# Opportunity cost breakdown
st.markdown("---")
st.subheader("💰 Análise de Custo de Oportunidade")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Custo Diário",
        value=format_currency(opportunity_cost['custo_oportunidade_diario']),
        help="Receita perdida por dia devido a leads não convertidos"
    )

with col2:
    st.metric(
        label="Custo Semanal",
        value=format_currency(opportunity_cost['custo_oportunidade_semanal']),
        help="Receita perdida por semana (5 dias úteis)"
    )

with col3:
    st.metric(
        label="Custo Mensal",
        value=format_currency(opportunity_cost['custo_oportunidade_mensal']),
        help="Receita perdida por mês (20 dias úteis)"
    )

with col4:
    st.metric(
        label="Custo Anual",
        value=format_currency(opportunity_cost['custo_oportunidade_anual']),
        help="Receita perdida por ano (240 dias úteis)"
    )

# Recommendations
st.markdown("---")
st.subheader("💡 Recomendações")

if opportunity_cost['failure_rate'] > 0.5:
    st.warning("⚠️ **Alta taxa de falha detectada!** Considere revisar o processo de atendimento.")
    
if df[df['chat_type'] == 'success']['secretary_questions'].mean() > df[df['chat_type'] == 'fail']['secretary_questions'].mean():
    st.info("💬 **Insight:** Conversas de sucesso têm mais perguntas da secretária. Incentive mais interação.")

if df[df['chat_type'] == 'success']['duration_minutes'].mean() > df[df['chat_type'] == 'fail']['duration_minutes'].mean():
    st.info("⏱️ **Insight:** Conversas mais longas tendem a ter mais sucesso. Invista tempo na qualidade do atendimento.")

st.success("✅ **Dashboard atualizado com sucesso!** Use as outras páginas para análises mais detalhadas.")

