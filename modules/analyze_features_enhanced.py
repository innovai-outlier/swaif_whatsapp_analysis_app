import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from modules.constants import EXTRACTED_FEATURES_CSV, ASSETS_DIR

def perform_eda(df):
    print("\n--- Análise Exploratória de Dados Aprimorada ---")

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
    plt.figure(figsize=(18, 12))

    # Duração da Conversa
    plt.subplot(2, 4, 1)
    sns.boxplot(x="chat_type", y="duration_minutes", data=df)
    plt.title("Duração da Conversa (Minutos)")

    # Número Total de Mensagens
    plt.subplot(2, 4, 2)
    sns.boxplot(x="chat_type", y="total_messages", data=df)
    plt.title("Número Total de Mensagens")

    # Mensagens da Secretária
    plt.subplot(2, 4, 3)
    sns.boxplot(x="chat_type", y="secretary_messages", data=df)
    plt.title("Mensagens da Secretária")

    # Mensagens do Paciente
    plt.subplot(2, 4, 4)
    sns.boxplot(x="chat_type", y="patient_messages", data=df)
    plt.title("Mensagens do Paciente")

    # Palavras-chave de Agendamento
    plt.subplot(2, 4, 5)
    sns.boxplot(x="chat_type", y="agendamento_keywords", data=df)
    plt.title("Frequência de Palavras-chave de Agendamento")

    # Palavras-chave de Preço
    plt.subplot(2, 4, 6)
    sns.boxplot(x="chat_type", y="preco_keywords", data=df)
    plt.title("Frequência de Palavras-chave de Preço")

    # Score Geral de Alinhamento (se disponível)
    if 'alignment_overall' in df.columns:
        plt.subplot(2, 4, 7)
        sns.boxplot(x="chat_type", y="alignment_overall", data=df)
        plt.title("Score Geral de Alinhamento")

    plt.tight_layout()
    plt.savefig(f"{ASSETS_DIR}/feature_distributions_enhanced.png")
    plt.close()
    print(f"Gráfico \'{ASSETS_DIR}/feature_distributions_enhanced.png\' gerado.")

    # Matriz de Correlação
    plt.figure(figsize=(12, 10))
    correlation_matrix = df.drop(columns=["chat_type"], errors='ignore').corr()
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Matriz de Correlação das Features")
    plt.savefig(f"{ASSETS_DIR}/correlation_matrix_enhanced.png")
    plt.close()
    print(f"Gráfico \'{ASSETS_DIR}/correlation_matrix_enhanced.png\' gerado.")


if __name__ == "__main__":
    try:
        features_df = pd.read_csv(EXTRACTED_FEATURES_CSV)
        perform_eda(features_df)
        print("Análise exploratória aprimorada concluída.")
    except FileNotFoundError:
        print(f"Erro: \'{EXTRACTED_FEATURES_CSV}\' não encontrado. Por favor, execute \'extract_features_enhanced.py\' primeiro.")


