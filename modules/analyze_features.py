
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
    print("Gráfico 'feature_distributions.png' gerado.")

    # Matriz de Correlação
    plt.figure(figsize=(10, 8))
    correlation_matrix = df.drop(columns=["chat_type"]).corr()
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Matriz de Correlação das Features")
    plt.savefig("correlation_matrix.png")
    plt.close()
    print("Gráfico 'correlation_matrix.png' gerado.")


if __name__ == "__main__":
    try:
        features_df = pd.read_csv("extracted_features.csv")
        perform_eda(features_df)
        print("Análise exploratória concluída.")
    except FileNotFoundError:
        print("Erro: 'extracted_features.csv' não encontrado. Por favor, execute 'extract_features.py' primeiro.")



