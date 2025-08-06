
import os
import re
import pandas as pd
from datetime import datetime

def parse_whatsapp_chat(file_path):
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

def extract_features(chat_df, chat_type):
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
            'secretary_questions': 0
        }

    # Feature: Duração da Conversa
    duration = (chat_df['timestamp'].max() - chat_df['timestamp'].min()).total_seconds() / 60
    features['duration_minutes'] = duration

    # Feature: Número Total de Mensagens
    features['total_messages'] = len(chat_df)

    # Feature: Número de Mensagens por Parte (Secretária vs. Paciente)
    # Assumindo que 'Dra Cristal Endocrinologista' e 'Sol' são a secretária
    secretary_senders = ['Dra Cristal Endocrinologista', 'Sol']
    features['secretary_messages'] = chat_df[chat_df['sender'].isin(secretary_senders)].shape[0]
    features['patient_messages'] = chat_df[~chat_df['sender'].isin(secretary_senders)].shape[0]

    # Feature: Número de Interações (simplificado: mudança de remetente)
    # Isso pode ser mais complexo, mas para começar, uma mudança de remetente indica uma interação
    if not chat_df.empty:
        features['num_interactions'] = (chat_df['sender'] != chat_df['sender'].shift()).sum()
    else:
        features['num_interactions'] = 0

    # Features de Conteúdo (Análise de Texto)
    all_messages_lower = ' '.join(chat_df['message'].str.lower().tolist())

    # Palavras-chave de Agendamento
    agendamento_keywords = ['agendar', 'consulta', 'horário', 'disponibilidade', 'marcar']
    features['agendamento_keywords'] = sum(all_messages_lower.count(kw) for kw in agendamento_keywords)

    # Palavras-chave de Preço
    preco_keywords = ['valor', 'preço', 'custo', 'investimento', 'reais']
    features['preco_keywords'] = sum(all_messages_lower.count(kw) for kw in preco_keywords)

    # Presença de Áudios/Mídias
    features['audio_media_messages'] = chat_df['message'].str.contains('áudio ocultado|imagem ocultada|vídeo ocultado', case=False).sum()

    # Perguntas do Paciente/Lead e Secretária
    features['patient_questions'] = chat_df[~chat_df['sender'].isin(secretary_senders)]['message'].str.contains('\?').sum()
    features['secretary_questions'] = chat_df[chat_df['sender'].isin(secretary_senders)]['message'].str.contains('\?').sum()

    features['chat_type'] = chat_type

    return features


if __name__ == '__main__':
    success_dir = 'success_cases'
    fail_dir = 'fail_cases'

    all_features = []

    # Processar casos de sucesso
    for root, _, files in os.walk(success_dir):
        for file in files:
            if file.endswith('_chat.txt'):
                file_path = os.path.join(root, file)
                chat_df = parse_whatsapp_chat(file_path)
                features = extract_features(chat_df, 'success')
                all_features.append(features)

    # Processar casos de falha
    for root, _, files in os.walk(fail_dir):
        for file in files:
            if file.endswith('_chat.txt'):
                file_path = os.path.join(root, file)
                chat_df = parse_whatsapp_chat(file_path)
                features = extract_features(chat_df, 'fail')
                all_features.append(features)

    features_df = pd.DataFrame(all_features)
    features_df.to_csv('extracted_features.csv', index=False)
    print('Extração de features concluída. Dados salvos em extracted_features.csv')



