# Lista de Features Potenciais

Com base na análise inicial das conversas, as seguintes features foram identificadas como potenciais diferenciadores entre casos de sucesso e falha:

## Features Gerais da Conversa

*   **Duração da Conversa:** Tempo total desde a primeira até a última mensagem (em minutos ou horas).
*   **Número Total de Mensagens:** Contagem total de mensagens trocadas.
*   **Número de Mensagens por Parte (Secretária vs. Paciente):** Proporção de mensagens enviadas por cada parte.
*   **Número de Interações:** Quantidade de "turnos" na conversa (pergunta e resposta).

## Features de Conteúdo (Análise de Texto)

*   **Presença de Palavras-Chave de Agendamento:** Frequência de termos como "agendar", "consulta", "horário", "disponibilidade".
*   **Presença de Palavras-Chave de Preço:** Frequência de termos como "valor", "preço", "custo", "investimento".
*   **Menções a Sintomas/Problemas de Saúde:** Detecção e contagem de termos relacionados a queixas de saúde.
*   **Menções a Especialidade/Dra. Cristal:** Frequência de menções ao nome da médica ou à especialidade.
*   **Perguntas do Paciente/Lead:** Contagem de mensagens do paciente que terminam com um ponto de interrogação ou que são identificadas como perguntas.
*   **Perguntas da Secretária:** Contagem de mensagens da secretária que terminam com um ponto de interrogação ou que são identificadas como perguntas.
*   **Tom da Conversa (Análise de Sentimento):** Classificação do sentimento geral das mensagens (positivo, negativo, neutro).
*   **Presença de Áudios/Mídias:** Indicação se a conversa contém mensagens de áudio, imagens ou vídeos.
*   **Respostas a Perguntas Chave:** Identificação se perguntas cruciais (ex: "Qual o motivo da busca?", "Qual o seu nome?") foram respondidas.
*   **Oferta de Solução/Próximo Passo pela Secretária:** Detecção de mensagens onde a secretária propõe uma solução ou um próximo passo claro (ex: "Podemos agendar para...").
*   **Objeções do Paciente/Lead:** Identificação de mensagens que expressam dúvidas, hesitações ou recusas (ex: "muito caro", "não tenho tempo", "preciso pensar").
*   **Follow-up da Secretária:** Contagem de mensagens de follow-up enviadas pela secretária após uma pausa na conversa.

## Features Estruturais

*   **Formato da Mensagem:** Análise se as mensagens são curtas, longas, se usam emojis, etc.
*   **Identificação de Remetente:** Extração do nome ou número do remetente para diferenciar secretária de paciente.

Essas features servirão de base para a criação do script de extração e para a análise exploratória dos dados.

