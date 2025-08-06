# 💬 Sistema de Análise de Conversas de WhatsApp

Um aplicativo Streamlit completo para análise de conversas de WhatsApp entre secretárias de clínicas médicas e pacientes/leads, com foco na identificação de padrões de sucesso e falha, cálculo de custo de oportunidade e otimização do processo de conversão.

## 🎯 Objetivo

Este sistema foi desenvolvido para ajudar médicos e secretárias a:

- **Identificar padrões** que levam ao sucesso ou falha nas conversas
- **Calcular o custo de oportunidade** de leads não convertidos
- **Analisar o alinhamento** entre as práticas da secretária e as diretrizes da médica
- **Gerar resumos automáticos** das conversas
- **Rastrear pendências** e tarefas
- **Tomar decisões baseadas em dados** para melhorar a taxa de conversão

## 🚀 Funcionalidades Principais

### 📊 Dashboard
- Visão geral dos dados e métricas principais
- Taxa de conversão e distribuição de sucessos/falhas
- Métricas de duração e mensagens
- Recomendações baseadas nos dados

### 🔍 Análise Exploratória
- Gráficos interativos e estatísticas detalhadas
- Matriz de correlação entre features
- Comparações entre casos de sucesso e falha
- Filtros e exportação de dados

### 💰 Custo de Oportunidade
- Cálculo detalhado do impacto financeiro
- Simulação de cenários e análise de ROI
- Projeções diárias, semanais, mensais e anuais
- Plano de ação baseado nos resultados

### 📝 Resumos e Pendências
- Resumos automáticos das conversas
- Rastreamento de pendências por tipo e responsável
- Análise de alinhamento com diretrizes
- Busca e filtros avançados

### ⚙️ Configurações
- Configuração do conteúdo alinhado
- Parâmetros financeiros personalizáveis
- Gerenciamento de dados
- Configurações do sistema

## 📁 Estrutura do Projeto

```
whatsapp_analysis_app/
├── app.py                          # Aplicativo principal
├── requirements.txt                # Dependências
├── README.md                      # Documentação
├── assets/                        # Recursos visuais
│   ├── image.png                  # Logo/ícone
│   ├── feature_distributions_enhanced.png
│   └── correlation_matrix_enhanced.png
├── data/                          # Dados processados
│   ├── success_cases/             # Conversas de sucesso
│   ├── fail_cases/               # Conversas de falha
│   ├── extracted_features_enhanced.csv
│   └── detailed_analysis_results.json
├── modules/                       # Módulos Python
│   ├── constants.py              # Constantes e configurações
│   ├── utils.py                  # Funções utilitárias
│   ├── extract_features_enhanced.py  # Extração de features
│   └── analyze_features_enhanced.py  # Análise exploratória
├── pages/                         # Páginas do Streamlit
│   ├── 1_📊_Dashboard.py
│   ├── 2_🔍_Análise_Exploratória.py
│   ├── 3_💰_Custo_de_Oportunidade.py
│   ├── 4_📝_Resumos_e_Pendências.py
│   └── 5_⚙️_Configurações.py
└── src/                          # Documentação e templates
    ├── features.md
    ├── new_features_definition.md
    ├── aligned_content_template.txt
    └── report_enhanced.md
```

## 🛠️ Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone ou baixe o projeto**
   ```bash
   # Se usando git
   git clone <repository-url>
   cd whatsapp_analysis_app
   
   # Ou extraia o arquivo ZIP baixado
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare os dados**
   - Coloque os arquivos de chat do WhatsApp nas pastas `data/success_cases/` e `data/fail_cases/`
   - Cada conversa deve estar em um arquivo `_chat.txt`
   - Formato esperado: `[DD/MM/AAAA, HH:MM:SS] Nome: Mensagem`

4. **Execute a extração de features**
   ```bash
   python modules/extract_features_enhanced.py
   ```

5. **Inicie o aplicativo**
   ```bash
   streamlit run app.py
   ```

6. **Acesse no navegador**
   - O aplicativo estará disponível em `http://localhost:8501`

## 📊 Como Usar

### Primeira Configuração

1. **Acesse a página Configurações** (⚙️)
2. **Configure o Alinhamento**: Insira as diretrizes que a médica treina a secretária
3. **Ajuste os Parâmetros**: Defina o valor médio da consulta e número de leads diários
4. **Reprocesse os Dados**: Execute novamente a extração de features

### Análise Diária

1. **Dashboard**: Comece sempre pelo dashboard para uma visão geral
2. **Análise Exploratória**: Explore padrões e correlações nos dados
3. **Custo de Oportunidade**: Monitore o impacto financeiro
4. **Resumos e Pendências**: Acompanhe conversas específicas

### Tomada de Decisão

- Use as **recomendações do dashboard** como ponto de partida
- Analise as **métricas de alinhamento** para identificar gaps de treinamento
- Monitore o **custo de oportunidade** para priorizar melhorias
- Acompanhe **pendências** para garantir follow-up adequado

## 🔧 Features Técnicas

### Features Extraídas

**Métricas Básicas:**
- Duração da conversa (minutos)
- Número total de mensagens
- Mensagens da secretária vs paciente
- Número de interações (trocas de turno)

**Análise de Conteúdo:**
- Frequência de palavras-chave de agendamento
- Frequência de palavras-chave de preço
- Número de perguntas do paciente e secretária
- Mensagens de áudio/mídia

**Análise Avançada:**
- Resumo automático da conversa
- Lista de pendências por tipo e responsável
- Score de alinhamento com diretrizes (similaridade, cobertura, sequência)

### Algoritmos Utilizados

- **TF-IDF**: Para análise de similaridade semântica
- **Cosine Similarity**: Para cálculo de alinhamento
- **Regex**: Para extração de padrões e pendências
- **Análise Estatística**: Para comparações e correlações

## 📈 Métricas e KPIs

### Principais Indicadores

- **Taxa de Conversão**: % de leads que se tornam agendamentos
- **Custo de Oportunidade**: Receita perdida por leads não convertidos
- **Score de Alinhamento**: Aderência às diretrizes (0-100)
- **Tempo Médio de Resposta**: Eficiência no atendimento
- **Pendências por Conversa**: Qualidade do follow-up

### Benchmarks Sugeridos

- **Taxa de Conversão**: > 60% (boa), > 40% (aceitável), < 40% (crítica)
- **Score de Alinhamento**: > 80% (excelente), > 60% (bom), < 60% (necessita treinamento)
- **Duração Média**: Conversas de sucesso tendem a ser mais longas
- **Interações**: Mais trocas de turno indicam engajamento

## 🎨 Personalização

### Cores e Visual

O sistema utiliza um esquema de cores baseado no material fornecido:
- **Cor Primária**: #0A1128 (Azul escuro)
- **Cor Secundária**: #FF7F11 (Laranja)
- **Sucesso**: #28a745 (Verde)
- **Falha**: #dc3545 (Vermelho)

### Customização

Para personalizar o sistema:

1. **Cores**: Edite `modules/constants.py`
2. **Textos**: Modifique as constantes em `modules/constants.py`
3. **Métricas**: Ajuste os cálculos em `modules/utils.py`
4. **Features**: Adicione novas features em `modules/extract_features_enhanced.py`

## 🔍 Solução de Problemas

### Problemas Comuns

**Erro: "Dados não encontrados"**
- Verifique se os arquivos estão nas pastas corretas
- Execute `python modules/extract_features_enhanced.py`
- Confirme o formato dos arquivos de chat

**Score de alinhamento sempre 0**
- Configure o conteúdo alinhado na página Configurações
- Reprocesse os dados após configurar

**Gráficos não aparecem**
- Verifique se todas as dependências estão instaladas
- Execute `python modules/analyze_features_enhanced.py`

**Performance lenta**
- Reduza o número de conversas para teste
- Use filtros nas páginas de análise
- Limpe o cache nas Configurações

### Logs e Debug

Para debug avançado:
1. Acesse a página Configurações
2. Marque "Mostrar informações técnicas"
3. Verifique os logs no terminal onde o Streamlit está rodando

## 📚 Documentação Adicional

### Para Médicos

- **Foque no Dashboard**: Métricas principais e recomendações
- **Monitore o Custo**: Impacto financeiro das melhorias
- **Use Cenários**: Simule diferentes taxas de conversão
- **Acompanhe Alinhamento**: Verifique se a secretária segue as diretrizes

### Para Secretárias

- **Analise Resumos**: Entenda padrões de conversas bem-sucedidas
- **Acompanhe Pendências**: Garanta follow-up adequado
- **Estude Alinhamento**: Compare suas práticas com as diretrizes
- **Use Filtros**: Foque em tipos específicos de conversa

### Para Administradores

- **Configure Parâmetros**: Mantenha valores atualizados
- **Gerencie Dados**: Adicione novas conversas regularmente
- **Monitore Sistema**: Verifique status e performance
- **Faça Backups**: Preserve dados importantes

## 🤝 Suporte e Contribuição

### Suporte Técnico

Para dúvidas ou problemas:
1. Consulte esta documentação
2. Verifique a seção "Solução de Problemas"
3. Entre em contato com o suporte técnico

### Melhorias Futuras

Funcionalidades planejadas:
- [ ] Análise de sentimento das mensagens
- [ ] Integração com APIs do WhatsApp
- [ ] Alertas automáticos por email
- [ ] Dashboard executivo
- [ ] Análise preditiva
- [ ] Exportação para PowerBI

### Contribuindo

Para contribuir com o projeto:
1. Documente bugs encontrados
2. Sugira melhorias
3. Teste novas funcionalidades
4. Compartilhe casos de uso

# Projeto WhatsApp Analysis App

## Descrição
Este projeto implementa uma solução modular para análise de mensagens do WhatsApp Business, integrando uma camada Lite (Python) e uma camada Heavy (N8N). O objetivo é criar uma fábrica de software eficiente e escalável.

## Configuração Inicial
1. Certifique-se de ter o Python 3.9 ou superior instalado.
2. Instale as dependências listadas no arquivo `requirements.txt`.
3. Execute o comando `streamlit run lite/app.py` para iniciar a interface Lite.

## Uso
- A camada Lite consome dados processados pela camada Heavy e apresenta insights ao usuário.
- A camada Heavy utiliza o N8N para automação de workflows e processamento de mensagens.

## Estrutura do Projeto
- `lite/`: Contém a aplicação Python e seus módulos.
- `heavy/`: Contém os workflows e scripts relacionados ao N8N.
- `docs/`: Documentação do projeto.
- `tests/`: Testes automatizados.

## 📄 Licença e Créditos

**Desenvolvido para:** Análise de conversas médicas
**Versão:** 1.0
**Data:** 2024

**Tecnologias utilizadas:**
- Streamlit (Interface)
- Pandas (Manipulação de dados)
- Plotly (Visualizações)
- Scikit-learn (Machine Learning)
- Python (Linguagem principal)

---

💡 **Dica**: Mantenha os dados sempre atualizados e configure o alinhamento regularmente para obter os melhores insights!

