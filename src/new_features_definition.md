# Definição das Novas Features

## 1. Resumo da Conversa no Dia

**Objetivo:** Gerar um resumo conciso das principais interações e tópicos discutidos em cada conversa.

**Metodologia:**
- Extrair as mensagens principais de cada conversa
- Identificar os tópicos centrais (sintomas, agendamento, preços, etc.)
- Gerar um resumo estruturado com:
  - Data da conversa
  - Participantes identificados
  - Principais tópicos discutidos
  - Status final da conversa (agendamento realizado, pendente, cancelado)

**Implementação:**
- Utilizar processamento de linguagem natural para identificar tópicos-chave
- Criar templates de resumo baseados nos padrões identificados
- Agrupar mensagens por data para resumos diários

## 2. Lista de Pendências Geradas na Conversa

**Objetivo:** Identificar e listar todas as pendências que surgem durante a conversa, tanto para a secretária quanto para o paciente.

**Metodologia:**
- Detectar frases que indicam ações futuras ou compromissos
- Identificar quem é responsável por cada pendência
- Categorizar as pendências por tipo:
  - Envio de informações (exames, documentos)
  - Agendamentos
  - Retornos/follow-ups
  - Pagamentos
  - Confirmações

**Padrões de Detecção:**
- Frases com verbos no futuro ("vou enviar", "preciso de", "você pode")
- Expressões de compromisso ("vou verificar", "te retorno", "aguardo")
- Solicitações diretas ("me passa", "preciso que", "pode me enviar")

**Implementação:**
- Usar regex e análise sintática para detectar padrões
- Classificar pendências por responsável (secretária, paciente, médica)
- Gerar lista estruturada com status (pendente, concluído, cancelado)

## 3. Grau de Alinhamento com Conteúdo da Médica

**Objetivo:** Medir o quanto o comportamento da secretária nas conversas está alinhado com as instruções/treinamentos da médica.

**Metodologia:**
- **Entrada de Dados:** Arquivo `aligned_content.txt` contendo as instruções da médica
- **Extração de Comportamento:** Análise das mensagens da secretária para identificar:
  - Tópicos abordados
  - Sequência de informações fornecidas
  - Linguagem utilizada
  - Perguntas feitas
  - Informações omitidas

**Cálculo do Alinhamento:**
1. **Similaridade Semântica:** Comparar o conteúdo das mensagens da secretária com as instruções usando:
   - TF-IDF (Term Frequency-Inverse Document Frequency)
   - Similaridade de cosseno
   - Análise de palavras-chave

2. **Cobertura de Tópicos:** Verificar se a secretária aborda todos os pontos importantes:
   - Pontuação baseada na porcentagem de tópicos cobertos
   - Peso diferenciado para tópicos críticos

3. **Sequência e Timing:** Avaliar se as informações são fornecidas na ordem e momento adequados:
   - Análise da sequência temporal das mensagens
   - Verificação de timing apropriado para diferentes tipos de informação

**Métricas de Alinhamento:**
- **Score de Similaridade:** 0-100% baseado na similaridade semântica
- **Score de Cobertura:** 0-100% baseado nos tópicos abordados
- **Score de Sequência:** 0-100% baseado na ordem e timing
- **Score Geral de Alinhamento:** Média ponderada dos três scores acima

**Implementação:**
- Preprocessamento do conteúdo alinhado (tokenização, remoção de stopwords)
- Vetorização das mensagens da secretária e do conteúdo alinhado
- Cálculo de similaridades e scores
- Geração de relatório detalhado do alinhamento

## 4. Estrutura de Saída

Cada conversa terá as seguintes informações adicionais:

```python
{
    'resumo_diario': 'Texto do resumo da conversa',
    'pendencias': [
        {
            'descricao': 'Descrição da pendência',
            'responsavel': 'secretaria/paciente/medica',
            'tipo': 'agendamento/informacao/pagamento/etc',
            'status': 'pendente/concluido/cancelado'
        }
    ],
    'alinhamento': {
        'score_similaridade': 85.5,
        'score_cobertura': 92.0,
        'score_sequencia': 78.3,
        'score_geral': 85.3,
        'detalhes': 'Análise detalhada do alinhamento'
    }
}
```

## 5. Considerações Técnicas

- **Dependências:** Será necessário instalar bibliotecas adicionais como scikit-learn para TF-IDF e cálculos de similaridade
- **Performance:** Para grandes volumes de dados, considerar otimizações como cache de vetorizações
- **Flexibilidade:** O sistema deve ser facilmente adaptável para diferentes tipos de instruções e contextos
- **Validação:** Implementar mecanismos para validar a qualidade dos resumos e detecção de pendências


