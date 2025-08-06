import os
import re
import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from modules.constants import ALIGNED_CONTENT_FILE, SUCCESS_CASES_DIR, FAIL_CASES_DIR, EXTRACTED_FEATURES_CSV, DETAILED_ANALYSIS_JSON

def parse_whatsapp_chat(file_path):
    """Parse WhatsApp chat file and return DataFrame with messages"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    chat_data = []
    for line in lines:
        # Regex para capturar data, hora, remetente e mensagem
        match = re.match(r'\[(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2}:\d{2})\] (.*?): (.*)', line)
        if match:
            date_str, time_str, sender, message = match.groups()
            timestamp = datetime.strptime(f'{date_str} {time_str}', '%d/%m/%Y %H:%M:%S')
            chat_data.append({'timestamp': timestamp, 'sender': sender.strip(), 'message': message.strip()})
        else:
            # Se a linha não corresponder ao padrão, pode ser uma continuação da mensagem anterior
            if chat_data:
                chat_data[-1]['message'] += '\n' + line.strip()
    return pd.DataFrame(chat_data)

def load_aligned_content(file_path=ALIGNED_CONTENT_FILE):
    """Load aligned content from file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        return content if content else None
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado. Grau de alinhamento não será calculado.")
        return None

def generate_daily_summary(chat_df):
    """Generate a daily summary of the conversation"""
    if chat_df.empty:
        return "Conversa vazia"
    
    # Identificar participantes
    participants = chat_df['sender'].unique()
    secretary_senders = ['Dra Cristal Endocrinologista', 'Sol']
    secretary = [p for p in participants if p in secretary_senders]
    patients = [p for p in participants if p not in secretary_senders]
    
    # Extrair tópicos principais
    all_messages = ' '.join(chat_df['message'].str.lower())
    
    # Identificar tópicos principais
    topics = []
    if any(word in all_messages for word in ['agendar', 'consulta', 'horário']):
        topics.append('agendamento')
    if any(word in all_messages for word in ['valor', 'preço', 'custo', 'reais']):
        topics.append('preços')
    if any(word in all_messages for word in ['sintoma', 'dor', 'problema', 'saúde']):
        topics.append('sintomas')
    if any(word in all_messages for word in ['exame', 'resultado', 'bioimpedância']):
        topics.append('exames')
    
    # Determinar status final
    status = "indefinido"
    if any(word in all_messages for word in ['dados', 'cpf', 'nome completo']):
        status = "agendamento em andamento"
    elif 'agendamento' in topics:
        status = "interesse em agendamento"
    
    # Gerar resumo
    date_str = chat_df['timestamp'].dt.date.iloc[0].strftime('%d/%m/%Y')
    summary = f"Conversa de {date_str} entre {', '.join(secretary)} e {', '.join(patients)}. "
    summary += f"Tópicos discutidos: {', '.join(topics) if topics else 'conversa inicial'}. "
    summary += f"Status: {status}."
    
    return summary

def extract_pendencies(chat_df):
    """Extract pendencies from the conversation"""
    pendencies = []
    secretary_senders = ['Dra Cristal Endocrinologista', 'Sol']
    
    # Padrões para detectar pendências
    patterns = {
        'agendamento': [
            r'vou agendar',
            r'podemos agendar',
            r'disponibilidade para',
            r'marcar para'
        ],
        'informacao': [
            r'vou te passar',
            r'preciso que',
            r'me passa',
            r'pode me enviar',
            r'preciso de',
            r'vou te explicar'
        ],
        'exame': [
            r'solicitar exames',
            r'pedidos de exames',
            r'levar exames',
            r'bioimpedância'
        ],
        'pagamento': [
            r'pagamento',
            r'valor',
            r'pix',
            r'cartão'
        ]
    }
    
    for _, row in chat_df.iterrows():
        message = row['message'].lower()
        sender = row['sender']
        
        for pend_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, message):
                    responsible = 'secretaria' if sender in secretary_senders else 'paciente'
                    pendencies.append({
                        'descricao': row['message'][:100] + '...' if len(row['message']) > 100 else row['message'],
                        'responsavel': responsible,
                        'tipo': pend_type,
                        'status': 'pendente'
                    })
                    break
    
    return pendencies

def calculate_alignment_score(chat_df, aligned_content):
    """Calculate alignment score between secretary behavior and aligned content"""
    if aligned_content is None:
        return {
            'score_similaridade': 0,
            'score_cobertura': 0,
            'score_sequencia': 0,
            'score_geral': 0,
            'detalhes': 'Conteúdo alinhado não fornecido'
        }
    
    secretary_senders = ['Dra Cristal Endocrinologista', 'Sol']
    secretary_messages = chat_df[chat_df['sender'].isin(secretary_senders)]['message'].tolist()
    
    if not secretary_messages:
        return {
            'score_similaridade': 0,
            'score_cobertura': 0,
            'score_sequencia': 0,
            'score_geral': 0,
            'detalhes': 'Nenhuma mensagem da secretária encontrada'
        }
    
    # Combinar todas as mensagens da secretária
    secretary_text = ' '.join(secretary_messages)
    
    # Calcular similaridade usando TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
    try:
        tfidf_matrix = vectorizer.fit_transform([secretary_text, aligned_content])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        score_similaridade = similarity * 100
    except:
        score_similaridade = 0
    
    # Calcular cobertura de tópicos (simplificado)
    aligned_words = set(aligned_content.lower().split())
    secretary_words = set(secretary_text.lower().split())
    
    if aligned_words:
        coverage = len(aligned_words.intersection(secretary_words)) / len(aligned_words)
        score_cobertura = coverage * 100
    else:
        score_cobertura = 0
    
    # Score de sequência (simplificado - baseado na ordem das mensagens)
    score_sequencia = 75  # Valor padrão, pode ser refinado
    
    # Score geral (média ponderada)
    score_geral = (score_similaridade * 0.4 + score_cobertura * 0.4 + score_sequencia * 0.2)
    
    return {
        'score_similaridade': round(score_similaridade, 2),
        'score_cobertura': round(score_cobertura, 2),
        'score_sequencia': round(score_sequencia, 2),
        'score_geral': round(score_geral, 2),
        'detalhes': f'Similaridade semântica: {score_similaridade:.1f}%, Cobertura de tópicos: {score_cobertura:.1f}%'
    }

def extract_features_enhanced(chat_df, chat_type, aligned_content=None):
    """Extract enhanced features including summary, pendencies, and alignment"""
    features = {}
    
    if chat_df.empty:
        return {
            'chat_type': chat_type,
            'total_messages': 0,
            'duration_minutes': 0,
            'secretary_messages': 0,
            'patient_messages': 0,
            'num_interactions': 0,
            'agendamento_keywords': 0,
            'preco_keywords': 0,
            'audio_media_messages': 0,
            'patient_questions': 0,
            'secretary_questions': 0,
            'resumo_diario': 'Conversa vazia',
            'pendencias': [],
            'alinhamento': calculate_alignment_score(pd.DataFrame(), aligned_content)
        }

    # Features originais
    duration = (chat_df['timestamp'].max() - chat_df['timestamp'].min()).total_seconds() / 60
    features['duration_minutes'] = duration
    features['total_messages'] = len(chat_df)

    secretary_senders = ['Dra Cristal Endocrinologista', 'Sol']
    features['secretary_messages'] = chat_df[chat_df['sender'].isin(secretary_senders)].shape[0]
    features['patient_messages'] = chat_df[~chat_df['sender'].isin(secretary_senders)].shape[0]

    if not chat_df.empty:
        features['num_interactions'] = (chat_df['sender'] != chat_df['sender'].shift()).sum()
    else:
        features['num_interactions'] = 0

    all_messages_lower = ' '.join(chat_df['message'].str.lower().tolist())

    agendamento_keywords = ['agendar', 'consulta', 'horário', 'disponibilidade', 'marcar']
    features['agendamento_keywords'] = sum(all_messages_lower.count(kw) for kw in agendamento_keywords)

    preco_keywords = ['valor', 'preço', 'custo', 'investimento', 'reais']
    features['preco_keywords'] = sum(all_messages_lower.count(kw) for kw in preco_keywords)

    features['audio_media_messages'] = chat_df['message'].str.contains('áudio ocultado|imagem ocultada|vídeo ocultado', case=False).sum()

    features['patient_questions'] = chat_df[~chat_df['sender'].isin(secretary_senders)]['message'].str.contains('\?').sum()
    features['secretary_questions'] = chat_df[chat_df['sender'].isin(secretary_senders)]['message'].str.contains('\?').sum()

    # Novas features
    features['resumo_diario'] = generate_daily_summary(chat_df)
    features['pendencias'] = extract_pendencies(chat_df)
    features['alinhamento'] = calculate_alignment_score(chat_df, aligned_content)

    features['chat_type'] = chat_type

    return features

if __name__ == '__main__':
    # Carregar conteúdo alinhado
    aligned_content = load_aligned_content()
    
    success_dir = SUCCESS_CASES_DIR
    fail_dir = FAIL_CASES_DIR

    all_features = []

    # Processar casos de sucesso
    for root, _, files in os.walk(success_dir):
        for file in files:
            if file.endswith('_chat.txt'):
                file_path = os.path.join(root, file)
                chat_df = parse_whatsapp_chat(file_path)
                features = extract_features_enhanced(chat_df, 'success', aligned_content)
                all_features.append(features)

    # Processar casos de falha
    for root, _, files in os.walk(fail_dir):
        for file in files:
            if file.endswith('_chat.txt'):
                file_path = os.path.join(root, file)
                chat_df = parse_whatsapp_chat(file_path)
                features = extract_features_enhanced(chat_df, 'fail', aligned_content)
                all_features.append(features)

    # Separar features simples das complexas para o CSV
    simple_features = []
    detailed_results = []
    
    for features in all_features:
        # Features simples para CSV
        simple_feature = {k: v for k, v in features.items() 
                         if k not in ['resumo_diario', 'pendencias', 'alinhamento']}
        
        # Adicionar scores de alinhamento como features simples
        if 'alinhamento' in features:
            simple_feature.update({
                'alignment_similarity': features['alinhamento']['score_similaridade'],
                'alignment_coverage': features['alinhamento']['score_cobertura'],
                'alignment_sequence': features['alinhamento']['score_sequencia'],
                'alignment_overall': features['alinhamento']['score_geral']
            })
        
        simple_features.append(simple_feature)
        detailed_results.append(features)

    # Salvar features simples em CSV
    features_df = pd.DataFrame(simple_features)
    features_df.to_csv(EXTRACTED_FEATURES_CSV, index=False)
    
    # Salvar resultados detalhados em arquivo separado
    import json
    with open(DETAILED_ANALYSIS_JSON, 'w', encoding='utf-8') as f:
        json.dump(detailed_results, f, ensure_ascii=False, indent=2, default=str)
    
    print('Extração de features aprimorada concluída.')
    print('Dados salvos em:')
    print(f'- {EXTRACTED_FEATURES_CSV} (features numéricas)')
    print(f'- {DETAILED_ANALYSIS_JSON} (análise completa)')
    
    if aligned_content is None:
        print(f'\nNOTA: Para calcular o grau de alinhamento, crie um arquivo "{ALIGNED_CONTENT_FILE}"')
        print('com as instruções da médica para a secretária.')


