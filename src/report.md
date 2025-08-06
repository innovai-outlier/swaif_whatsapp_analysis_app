# Relatório de Análise de Conversas de WhatsApp

## 1. Introdução

Este relatório apresenta uma análise das conversas de WhatsApp de uma clínica médica, com o objetivo de identificar características que diferenciam casos de sucesso (agendamentos) de falha, fornecer scripts para extração de features e análise exploratória, e calcular o custo de oportunidade.

## 2. Metodologia

As conversas foram divididas em dois grupos: sucesso (agendamentos realizados) e falha (agendamentos não realizados). Foram extraídas diversas features de cada conversa, abrangendo aspectos gerais, de conteúdo e estruturais. Em seguida, foi realizada uma análise exploratória dos dados para identificar padrões e diferenças significativas entre os grupos.

## 3. Lista de Features que se Destacam em Casos de Sucesso e Falha

Com base na análise inicial e exploratória, as seguintes features foram consideradas relevantes:

*   **Duração da Conversa:** Conversas mais longas podem indicar maior engajamento e, consequentemente, maior probabilidade de sucesso.
*   **Número Total de Mensagens:** Um maior volume de mensagens pode estar correlacionado com a duração da conversa e o nível de detalhe da interação.
*   **Número de Mensagens por Parte (Secretária vs. Paciente):** A proporção de mensagens trocadas pode indicar o equilíbrio da interação e o nível de proatividade de cada parte.
*   **Número de Interações:** Mais interações (trocas de turno) podem sugerir um diálogo mais dinâmico e eficaz.
*   **Presença de Palavras-Chave de Agendamento:** A frequência de termos relacionados a agendamento é um indicador direto da intenção do paciente e da secretária em concretizar a consulta.
*   **Presença de Palavras-Chave de Preço:** A discussão sobre valores pode ser um ponto crítico, e a forma como é abordada pode influenciar o resultado.
*   **Presença de Áudios/Mídias:** O uso de áudios ou outras mídias pode impactar a clareza da comunicação e o engajamento.
*   **Perguntas do Paciente/Lead e Secretária:** A quantidade de perguntas feitas por cada parte pode indicar o nível de interesse e a busca por informações.

Para uma lista mais detalhada e a definição de cada feature, consulte o arquivo `features.md`.

## 4. Script Python para Extração de Features

O script `extract_features.py` é responsável por processar os arquivos de chat do WhatsApp e extrair as features listadas acima. Ele lê as conversas, identifica remetentes, timestamps e mensagens, e calcula as métricas para cada chat. O resultado é salvo em um arquivo CSV (`extracted_features.csv`).

```python
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


```

## 5. Script Python para Análise Exploratória de Dados (EDA)

O script `analyze_features.py` realiza uma análise exploratória dos dados extraídos, gerando estatísticas descritivas, comparações entre os grupos de sucesso e falha, e visualizações para facilitar a compreensão dos padrões. Os gráficos gerados são salvos como `feature_distributions.png` e `correlation_matrix.png`.

```python




import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def perform_eda(df):
    print("\n--- Análise Exploratória de Dados ---")

    # 1. Estatísticas Descritivas por Tipo de Chat
    print("\n1. Estatísticas Descritivas por Tipo de Chat:")
    print(df.groupby("chat_type").describe().transpose())

    # 2. Comparação de Médias entre Sucesso e Falha
    print("\n2. Comparação de Médias entre Sucesso e Falha:")
    print(df.groupby("chat_type").mean())

    # 3. Visualizações
    print("\n3. Gerando Visualizações...")

    # Configurações de estilo para os gráficos
    sns.set_style("whitegrid")
    plt.figure(figsize=(15, 10))

    # Duração da Conversa
    plt.subplot(2, 3, 1)
    sns.boxplot(x="chat_type", y="duration_minutes", data=df)
    plt.title("Duração da Conversa (Minutos)")

    # Número Total de Mensagens
    plt.subplot(2, 3, 2)
    sns.boxplot(x="chat_type", y="total_messages", data=df)
    plt.title("Número Total de Mensagens")

    # Mensagens da Secretária
    plt.subplot(2, 3, 3)
    sns.boxplot(x="chat_type", y="secretary_messages", data=df)
    plt.title("Mensagens da Secretária")

    # Mensagens do Paciente
    plt.subplot(2, 3, 4)
    sns.boxplot(x="chat_type", y="patient_messages", data=df)
    plt.title("Mensagens do Paciente")

    # Palavras-chave de Agendamento
    plt.subplot(2, 3, 5)
    sns.boxplot(x="chat_type", y="agendamento_keywords", data=df)
    plt.title("Frequência de Palavras-chave de Agendamento")

    # Palavras-chave de Preço
    plt.subplot(2, 3, 6)
    sns.boxplot(x="chat_type", y="preco_keywords", data=df)
    plt.title("Frequência de Palavras-chave de Preço")

    plt.tight_layout()
    plt.savefig("feature_distributions.png")
    plt.close()
    print("Gráfico \'feature_distributions.png\' gerado.")

    # Matriz de Correlação
    plt.figure(figsize=(10, 8))
    correlation_matrix = df.drop(columns=["chat_type"]).corr()
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Matriz de Correlação das Features")
    plt.savefig("correlation_matrix.png")
    plt.close()
    print("Gráfico \'correlation_matrix.png\' gerado.")


if __name__ == "__main__":
    try:
        features_df = pd.read_csv("extracted_features.csv")
        perform_eda(features_df)
        print("Análise exploratória concluída.")
    except FileNotFoundError:
        print("Erro: \'extracted_features.csv\' não encontrado. Por favor, execute \'extract_features.py\' primeiro.")


```

## 6. Cálculo do Custo de Oportunidade

Com base nas informações fornecidas:

*   **Valor médio da consulta:** R$ 800,00
*   **Média de leads diários:** 5

Para calcular o custo de oportunidade, precisamos determinar a taxa de conversão dos leads em agendamentos. A partir dos dados extraídos, podemos calcular a proporção de casos de sucesso e falha.

### Métricas Relevantes

Para calcular o custo de oportunidade, precisamos das seguintes métricas:

*   **Número total de leads:** 5 leads/dia
*   **Taxa de Sucesso (Conversão):** (Número de Casos de Sucesso / Número Total de Casos) * 100
*   **Taxa de Falha:** (Número de Casos de Falha / Número Total de Casos) * 100
*   **Custo de Oportunidade Diário:** (Número de Leads Diários * Taxa de Falha) * Valor Médio da Consulta
*   **Custo de Oportunidade Semanal:** Custo de Oportunidade Diário * 5 (considerando 5 dias úteis)
*   **Custo de Oportunidade Mensal:** Custo de Oportunidade Diário * 20 (considerando 20 dias úteis)
*   **Custo de Oportunidade Anual:** Custo de Oportunidade Diário * 240 (considerando 240 dias úteis)

### Resultados do Cálculo

Para realizar o cálculo, vamos usar os dados de `extracted_features.csv`.



*   **Número Total de Casos Analisados:** 15
*   **Casos de Sucesso:** 7 (46.67%)
*   **Casos de Falha:** 8 (53.33%)

Com base nesses dados, o custo de oportunidade estimado é:

*   **Custo de Oportunidade Diário:** R$ 2133.33
*   **Custo de Oportunidade Semanal:** R$ 10666.67
*   **Custo de Oportunidade Mensal:** R$ 42666.67
*   **Custo de Oportunidade Anual:** R$ 512000.00

Esses valores representam a receita potencial que a clínica está perdendo devido aos leads que não se convertem em agendamentos, com base nos dados analisados.

## 7. Conclusão

Este relatório forneceu uma análise inicial das conversas de WhatsApp, identificando features relevantes e quantificando o custo de oportunidade. As features identificadas e os scripts fornecidos podem ser utilizados para aprofundar a análise e desenvolver estratégias para melhorar a taxa de conversão de leads em agendamentos.

