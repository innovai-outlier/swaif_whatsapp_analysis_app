### Regras de Negócio

#### Automação Permitida (Reino da Techne)
- **Classificação de Sentimentos**: IA analisa tom das conversas automaticamente
- **Extração de Palavras-chave**: Identificação automática de temas e padrões
- **Scoring de Qualidade**: Pontuação baseada em critérios objetivos pré-definidos
- **Categorização de Pendências**: Classificação automática por tipo e responsável
- **Cálculos Estatísticos**: Métricas de conversão e performance em tempo real
- **Detecção de Padrões**: Correlações e tendências identificadas automaticamente
- **Alertas Automáticos**: Notificações baseadas em regras pré-configuradas
- **Relatórios Padronizados**: Geração automática de dashboards e métricas

#### Preservação Humana (Reino da Psyche)
- **Decisões Clínicas**: Jamais sugerir diagnósticos, tratamentos ou medicamentos
- **Avaliação Ética**: Situações delicadas devem ser sempre sinalizadas para humanos
- **Relacionamento Médico-Paciente**: Preservar confidencialidade e emppatia
- **Decisões Estratégicas**: IA informa dados, mas gestor decide as ações
- **Interpretação Contextual**: Nuances culturais e pessoais requerem julgamento humano
- **Responsabilidade Final**: Profissional sempre responsável pelas decisões tomadas
- **Comunicação Sensível**: Mensagens sobre saúde mental ou emergências
- **Avaliação de Casos Complexos**: Situações que fogem de padrões conhecidos

#### Pontos de Decisão Humana
- **Ações Urgentes**: IA alerta e prioriza, mas humano executa
- **Casos Sensíveis**: Situações de saúde mental, emergência ou risco
- **Mudanças de Processo**: IA sugere melhorias, gestor implementa
- **Comunicação com Pacientes**: IA estrutura dados, humano personaliza resposta
- **Definição de Prioridades**: IA categoriza, mas responsável define urgência final
- **Interpretação de Contexto**: Situações ambíguas ou com nuances culturais
- **Decisões Financeiras**: Valores, descontos e negociações comerciais
- **Alterações de Agenda**: Mudanças que impactem outros pacientes

#### Limites Éticos e de Segurança
```python
# Verificações obrigatórias antes de qualquer processamento
SAFETY_CHECKS = {
    "medical_emergency_keywords": [
        "emergência", "urgente", "dor forte", "sangramento", 
        "desmaio", "falta de ar", "chest pain", "emergency"
    ],
    "mental_health_keywords": [
        "suicídio", "depressão", "ansiedade severa", 
        "não quero viver", "penso em morrer"
    ],
    "prohibited_actions": [
        "diagnóstico médico",
        "prescrição de medicamentos", 
        "interpretação de exames",
        "conselhos de tratamento"
    ]
}
```

#### Escalação Automática
1. **Urgência Médica**: Alerta imediato para médica + notificação secretária
2. **Situação de Risco**: Sinalização para gestor + log de segurança
3. **Oportunidade Comercial Alta**: Notificação para gestor comercial
4. **Insatisfação do Cliente**: Alerta para atendimento personalizado
5. **Erro de Processo**: Escalação para gestor de processos