import streamlit as st
import sys
import os
import pandas as pd
import json

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))

from modules.utils import load_detailed_analysis
from modules.constants import PRIMARY_COLOR, SECONDARY_COLOR

st.set_page_config(page_title="Resumos e Pendências", page_icon="📝", layout="wide")

st.title("📝 Resumos e Pendências")
st.markdown("Análise detalhada das conversas individuais")

# Load detailed analysis
detailed_data = load_detailed_analysis()

if detailed_data is None:
    st.error("❌ Dados detalhados não encontrados. Execute primeiro o script de extração de features.")
    st.stop()

# Sidebar filters
st.sidebar.header("🎛️ Filtros")

# Chat type filter
chat_types = list(set([item['chat_type'] for item in detailed_data]))
selected_chat_type = st.sidebar.selectbox(
    "Tipo de Conversa",
    options=['Todos'] + chat_types,
    index=0
)

# Filter data
if selected_chat_type != 'Todos':
    filtered_data = [item for item in detailed_data if item['chat_type'] == selected_chat_type]
else:
    filtered_data = detailed_data

# Search functionality
search_term = st.sidebar.text_input(
    "🔍 Buscar no resumo",
    placeholder="Digite palavras-chave..."
)

if search_term:
    filtered_data = [
        item for item in filtered_data 
        if search_term.lower() in item.get('resumo_diario', '').lower()
    ]

st.sidebar.markdown(f"**{len(filtered_data)}** conversas encontradas")

# Main content
tab1, tab2, tab3 = st.tabs(["📋 Resumos", "⏳ Pendências", "📊 Análise Geral"])

with tab1:
    st.subheader("📋 Resumos das Conversas")
    
    if not filtered_data:
        st.warning("⚠️ Nenhuma conversa encontrada com os filtros selecionados.")
    else:
        # Pagination
        items_per_page = 10
        total_pages = (len(filtered_data) - 1) // items_per_page + 1
        
        if total_pages > 1:
            page = st.selectbox(
                "Página",
                range(1, total_pages + 1),
                format_func=lambda x: f"Página {x} de {total_pages}"
            )
        else:
            page = 1
        
        start_idx = (page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, len(filtered_data))
        
        # Display conversations
        for i, conversation in enumerate(filtered_data[start_idx:end_idx], start_idx + 1):
            with st.expander(f"💬 Conversa {i} - {conversation['chat_type'].title()}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("**📝 Resumo:**")
                    st.write(conversation.get('resumo_diario', 'Resumo não disponível'))
                    
                    # Show alignment score if available
                    if 'alinhamento' in conversation:
                        alignment = conversation['alinhamento']
                        if alignment['score_geral'] > 0:
                            st.markdown("**🎯 Alinhamento:**")
                            st.write(alignment['detalhes'])
                
                with col2:
                    st.markdown("**📊 Métricas:**")
                    st.metric("Mensagens", conversation.get('total_messages', 0))
                    st.metric("Duração", f"{conversation.get('duration_minutes', 0):.0f} min")
                    
                    # Status indicator
                    if conversation['chat_type'] == 'success':
                        st.success("✅ Sucesso")
                    else:
                        st.error("❌ Falha")
                
                # Show pendencies if available
                if conversation.get('pendencias'):
                    st.markdown("**⏳ Pendências:**")
                    for pendencia in conversation['pendencias']:
                        status_icon = "✅" if pendencia['status'] == 'concluido' else "⏳"
                        st.write(f"{status_icon} **{pendencia['tipo'].title()}** ({pendencia['responsavel']}): {pendencia['descricao']}")

with tab2:
    st.subheader("⏳ Análise de Pendências")
    
    # Collect all pendencies
    all_pendencies = []
    for conversation in filtered_data:
        if conversation.get('pendencias'):
            for pendencia in conversation['pendencias']:
                pendencia_copy = pendencia.copy()
                pendencia_copy['chat_type'] = conversation['chat_type']
                all_pendencies.append(pendencia_copy)
    
    if not all_pendencies:
        st.info("ℹ️ Nenhuma pendência encontrada nas conversas selecionadas.")
    else:
        # Pendencies overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Pendências", len(all_pendencies))
        
        with col2:
            pendentes = len([p for p in all_pendencies if p['status'] == 'pendente'])
            st.metric("Pendentes", pendentes)
        
        with col3:
            secretaria = len([p for p in all_pendencies if p['responsavel'] == 'secretaria'])
            st.metric("Secretária", secretaria)
        
        with col4:
            paciente = len([p for p in all_pendencies if p['responsavel'] == 'paciente'])
            st.metric("Paciente", paciente)
        
        # Pendencies by type
        st.subheader("📊 Pendências por Tipo")
        
        pendencies_df = pd.DataFrame(all_pendencies)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # By type
            type_counts = pendencies_df['tipo'].value_counts()
            st.bar_chart(type_counts)
        
        with col2:
            # By responsible
            responsible_counts = pendencies_df['responsavel'].value_counts()
            st.bar_chart(responsible_counts)
        
        # Detailed pendencies table
        st.subheader("📋 Lista Detalhada de Pendências")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            tipo_filter = st.selectbox(
                "Filtrar por tipo",
                options=['Todos'] + list(pendencies_df['tipo'].unique())
            )
        
        with col2:
            responsavel_filter = st.selectbox(
                "Filtrar por responsável",
                options=['Todos'] + list(pendencies_df['responsavel'].unique())
            )
        
        with col3:
            status_filter = st.selectbox(
                "Filtrar por status",
                options=['Todos'] + list(pendencies_df['status'].unique())
            )
        
        # Apply filters
        filtered_pendencies = pendencies_df.copy()
        
        if tipo_filter != 'Todos':
            filtered_pendencies = filtered_pendencies[filtered_pendencies['tipo'] == tipo_filter]
        
        if responsavel_filter != 'Todos':
            filtered_pendencies = filtered_pendencies[filtered_pendencies['responsavel'] == responsavel_filter]
        
        if status_filter != 'Todos':
            filtered_pendencies = filtered_pendencies[filtered_pendencies['status'] == status_filter]
        
        # Display filtered pendencies
        if filtered_pendencies.empty:
            st.warning("⚠️ Nenhuma pendência encontrada com os filtros selecionados.")
        else:
            # Format for display
            display_df = filtered_pendencies[['tipo', 'responsavel', 'status', 'descricao', 'chat_type']].copy()
            display_df.columns = ['Tipo', 'Responsável', 'Status', 'Descrição', 'Tipo de Chat']
            
            # Add status icons
            display_df['Status'] = display_df['Status'].apply(
                lambda x: f"✅ {x}" if x == 'concluido' else f"⏳ {x}"
            )
            
            st.dataframe(display_df, use_container_width=True)

with tab3:
    st.subheader("📊 Análise Geral")
    
    # Summary statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Estatísticas de Resumos")
        
        # Average summary length
        summary_lengths = [len(item.get('resumo_diario', '')) for item in filtered_data]
        avg_summary_length = sum(summary_lengths) / len(summary_lengths) if summary_lengths else 0
        
        st.metric("Comprimento Médio do Resumo", f"{avg_summary_length:.0f} caracteres")
        
        # Most common topics in summaries
        all_summaries = ' '.join([item.get('resumo_diario', '') for item in filtered_data])
        
        # Simple word frequency (could be enhanced with NLP)
        common_words = ['agendamento', 'preços', 'sintomas', 'exames', 'consulta']
        word_counts = {word: all_summaries.lower().count(word) for word in common_words}
        
        st.markdown("**Tópicos Mais Comuns:**")
        for word, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                st.write(f"• {word.title()}: {count} menções")
    
    with col2:
        st.markdown("### ⏳ Estatísticas de Pendências")
        
        if all_pendencies:
            # Pendencies by chat type
            success_pendencies = len([p for p in all_pendencies if p['chat_type'] == 'success'])
            fail_pendencies = len([p for p in all_pendencies if p['chat_type'] == 'fail'])
            
            st.metric("Pendências em Sucessos", success_pendencies)
            st.metric("Pendências em Falhas", fail_pendencies)
            
            # Average pendencies per conversation
            conversations_with_pendencies = len([
                conv for conv in filtered_data 
                if conv.get('pendencias')
            ])
            
            if conversations_with_pendencies > 0:
                avg_pendencies = len(all_pendencies) / conversations_with_pendencies
                st.metric("Média por Conversa", f"{avg_pendencies:.1f}")
            
            # Most common pendency types
            pendency_types = {}
            for p in all_pendencies:
                pendency_types[p['tipo']] = pendency_types.get(p['tipo'], 0) + 1
            
            st.markdown("**Tipos Mais Comuns:**")
            for ptype, count in sorted(pendency_types.items(), key=lambda x: x[1], reverse=True):
                st.write(f"• {ptype.title()}: {count}")
        else:
            st.info("Nenhuma pendência encontrada para análise.")
    
    # Alignment analysis
    if any('alinhamento' in item for item in filtered_data):
        st.markdown("---")
        st.subheader("🎯 Análise de Alinhamento")
        
        alignment_scores = []
        for item in filtered_data:
            if 'alinhamento' in item and item['alinhamento']['score_geral'] > 0:
                alignment_scores.append({
                    'chat_type': item['chat_type'],
                    'score_geral': item['alinhamento']['score_geral'],
                    'score_similaridade': item['alinhamento']['score_similaridade'],
                    'score_cobertura': item['alinhamento']['score_cobertura']
                })
        
        if alignment_scores:
            alignment_df = pd.DataFrame(alignment_scores)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Average alignment by chat type
                avg_alignment = alignment_df.groupby('chat_type')['score_geral'].mean()
                st.bar_chart(avg_alignment)
                st.caption("Score Médio de Alinhamento por Tipo")
            
            with col2:
                # Alignment distribution
                st.histogram_chart(alignment_df['score_geral'])
                st.caption("Distribuição dos Scores de Alinhamento")
        else:
            st.info("ℹ️ Dados de alinhamento não disponíveis. Configure o conteúdo alinhado nas Configurações.")

# Export functionality
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Exportar Resumos"):
        export_data = []
        for i, conv in enumerate(filtered_data, 1):
            export_data.append({
                'ID': i,
                'Tipo': conv['chat_type'],
                'Resumo': conv.get('resumo_diario', ''),
                'Mensagens': conv.get('total_messages', 0),
                'Duração': conv.get('duration_minutes', 0),
                'Score_Alinhamento': conv.get('alinhamento', {}).get('score_geral', 0)
            })
        
        export_df = pd.DataFrame(export_data)
        csv = export_df.to_csv(index=False)
        
        st.download_button(
            label="💾 Download Resumos CSV",
            data=csv,
            file_name="resumos_conversas.csv",
            mime="text/csv"
        )

with col2:
    if st.button("📋 Exportar Pendências") and all_pendencies:
        pendencies_export = pd.DataFrame(all_pendencies)
        csv = pendencies_export.to_csv(index=False)
        
        st.download_button(
            label="💾 Download Pendências CSV",
            data=csv,
            file_name="pendencias_conversas.csv",
            mime="text/csv"
        )

