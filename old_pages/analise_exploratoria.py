# Renomeado de 🔍 Análise Exploratória.py
# Código original deve ser movido para cá
import streamlit as st
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))

from modules.utils import load_data
from modules.constants import PRIMARY_COLOR, SECONDARY_COLOR

st.set_page_config(page_title="Análise Exploratória", page_icon="🔍", layout="wide")

st.title("🔍 Análise Exploratória")
st.markdown("Gráficos e estatísticas detalhadas dos dados")

# Load data
df = load_data()

if df is None:
    st.error("❌ Dados não encontrados. Execute primeiro o script de extração de features.")
    st.stop()

# Sidebar filters
st.sidebar.header("🎛️ Filtros")

# Chat type filter
chat_types = st.sidebar.multiselect(
    "Tipo de Conversa",
    options=df['chat_type'].unique(),
    default=df['chat_type'].unique()
)

# Filter data
filtered_df = df[df['chat_type'].isin(chat_types)]

if filtered_df.empty:
    st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

# Main analysis
tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribuições", "🔗 Correlações", "📈 Comparações", "📋 Estatísticas"])

with tab1:
    st.subheader("📊 Distribuições das Features")
    
    # Select feature to analyze
    numeric_columns = [
        'duration_minutes', 'total_messages', 'secretary_messages', 
        'patient_messages', 'num_interactions', 'agendamento_keywords',
        'preco_keywords', 'patient_questions', 'secretary_questions'
    ]
    
    selected_feature = st.selectbox(
        "Selecione a feature para análise:",
        numeric_columns,
        format_func=lambda x: {
            'duration_minutes': 'Duração (minutos)',
            'total_messages': 'Total de Mensagens',
            'secretary_messages': 'Mensagens da Secretária',
            'patient_messages': 'Mensagens do Paciente',
            'num_interactions': 'Número de Interações',
            'agendamento_keywords': 'Palavras-chave de Agendamento',
            'preco_keywords': 'Palavras-chave de Preço',
            'patient_questions': 'Perguntas do Paciente',
            'secretary_questions': 'Perguntas da Secretária'
        }.get(x, x)
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Histogram
        fig_hist = px.histogram(
            filtered_df,
            x=selected_feature,
            color='chat_type',
            color_discrete_map={'success': '#28a745', 'fail': '#dc3545'},
            title=f"Distribuição: {selected_feature}",
            nbins=20
        )
        fig_hist.update_layout(height=400)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # Box plot
        fig_box = px.box(
            filtered_df,
            x='chat_type',
            y=selected_feature,
            color='chat_type',
            color_discrete_map={'success': '#28a745', 'fail': '#dc3545'},
            title=f"Box Plot: {selected_feature}"
        )
        fig_box.update_layout(height=400)
        st.plotly_chart(fig_box, use_container_width=True)
    
    # Statistics summary
    st.subheader("📈 Estatísticas Resumidas")
    
    stats_summary = filtered_df.groupby('chat_type')[selected_feature].describe()
    st.dataframe(stats_summary, use_container_width=True)

with tab2:
    st.subheader("🔗 Matriz de Correlação")
    
    # Calculate correlation matrix
    correlation_data = filtered_df[numeric_columns].corr()
    
    # Create heatmap
    fig_corr = px.imshow(
        correlation_data,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title="Matriz de Correlação das Features"
    )
    
    fig_corr.update_layout(height=600)
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Top correlations
    st.subheader("🔝 Principais Correlações")
    
    # Get correlation pairs
    corr_pairs = []
    for i in range(len(correlation_data.columns)):
        for j in range(i+1, len(correlation_data.columns)):
            corr_pairs.append({
                'Feature 1': correlation_data.columns[i],
                'Feature 2': correlation_data.columns[j],
                'Correlação': correlation_data.iloc[i, j]
            })
    
    # Sort by absolute correlation
    corr_pairs = sorted(corr_pairs, key=lambda x: abs(x['Correlação']), reverse=True)
    
    # Display top 10
    st.dataframe(corr_pairs[:10], use_container_width=True)

with tab3:
    st.subheader("📈 Comparações Sucesso vs Falha")
    
    # Select features for comparison
    features_to_compare = st.multiselect(
        "Selecione features para comparar:",
        numeric_columns,
        default=['total_messages', 'duration_minutes', 'secretary_questions']
    )
    
    if features_to_compare:
        # Create subplots
        fig = make_subplots(
            rows=len(features_to_compare),
            cols=1,
            subplot_titles=features_to_compare,
            vertical_spacing=0.1
        )
        
        for i, feature in enumerate(features_to_compare):
            # Success data
            success_data = filtered_df[filtered_df['chat_type'] == 'success'][feature]
            fail_data = filtered_df[filtered_df['chat_type'] == 'fail'][feature]
            
            fig.add_trace(
                go.Box(y=success_data, name='Sucesso', marker_color='#28a745'),
                row=i+1, col=1
            )
            
            fig.add_trace(
                go.Box(y=fail_data, name='Falha', marker_color='#dc3545'),
                row=i+1, col=1
            )
        
        fig.update_layout(height=300 * len(features_to_compare), showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistical comparison
        st.subheader("📊 Comparação Estatística")
        
        comparison_data = []
        for feature in features_to_compare:
            success_mean = filtered_df[filtered_df['chat_type'] == 'success'][feature].mean()
            fail_mean = filtered_df[filtered_df['chat_type'] == 'fail'][feature].mean()
            difference = success_mean - fail_mean
            
            comparison_data.append({
                'Feature': feature,
                'Média Sucesso': f"{success_mean:.2f}",
                'Média Falha': f"{fail_mean:.2f}",
                'Diferença': f"{difference:.2f}",
                'Diferença %': f"{(difference/fail_mean*100):.1f}%" if fail_mean != 0 else "N/A"
            })
        
        st.dataframe(comparison_data, use_container_width=True)

with tab4:
    st.subheader("📋 Estatísticas Detalhadas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Conversas de Sucesso")
        success_stats = filtered_df[filtered_df['chat_type'] == 'success'][numeric_columns].describe()
        st.dataframe(success_stats, use_container_width=True)
    
    with col2:
        st.markdown("### ❌ Conversas de Falha")
        fail_stats = filtered_df[filtered_df['chat_type'] == 'fail'][numeric_columns].describe()
        st.dataframe(fail_stats, use_container_width=True)
    
    # Overall statistics
    st.markdown("### 📊 Estatísticas Gerais")
    overall_stats = filtered_df[numeric_columns].describe()
    st.dataframe(overall_stats, use_container_width=True)
    
    # Data quality check
    st.subheader("🔍 Qualidade dos Dados")
    
    quality_data = []
    for col in numeric_columns:
        quality_data.append({
            'Feature': col,
            'Valores Únicos': filtered_df[col].nunique(),
            'Valores Nulos': filtered_df[col].isnull().sum(),
            'Valor Mínimo': filtered_df[col].min(),
            'Valor Máximo': filtered_df[col].max()
        })
    
    st.dataframe(quality_data, use_container_width=True)

# Export options
st.markdown("---")
st.subheader("📥 Exportar Dados")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Exportar Estatísticas"):
        stats_export = filtered_df.describe()
        csv = stats_export.to_csv()
        st.download_button(
            label="💾 Download CSV",
            data=csv,
            file_name="estatisticas_conversas.csv",
            mime="text/csv"
        )

with col2:
    if st.button("🔗 Exportar Correlações"):
        corr_export = filtered_df[numeric_columns].corr()
        csv = corr_export.to_csv()
        st.download_button(
            label="💾 Download CSV",
            data=csv,
            file_name="correlacoes_features.csv",
            mime="text/csv"
        )

with col3:
    if st.button("📋 Exportar Dados Filtrados"):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="💾 Download CSV",
            data=csv,
            file_name="dados_filtrados.csv",
            mime="text/csv"
        )

