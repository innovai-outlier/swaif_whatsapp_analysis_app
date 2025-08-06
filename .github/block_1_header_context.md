# WhatsApp Conversation Analyzer - Instructions
*Microserviço de Análise Inteligente de Conversas Clínicas*

## 🎯 Contexto Clínico

### Problema a Resolver
Secretárias de clínicas médicas de pequeno porte gastam tempo excessivo analisando manualmente centenas de conversas do WhatsApp, perdendo insights valiosos sobre:
- Qualidade do atendimento ao paciente
- Oportunidades de conversão perdidas
- Pendências operacionais dispersas
- Padrões comportamentais dos leads/pacientes

### Impacto Esperado
- **Tempo Economizado**: 4-6 horas/dia da secretária em análises manuais
- **Insights Acionáveis**: Identificação automática de melhorias no atendimento
- **Conversões Otimizadas**: Detecção precoce de leads qualificados
- **Gestão Proativa**: Lista automatizada de pendências por responsável

### Usuários-Alvo
- **Secretária**: Visualiza qualidade do atendimento e pendências
- **Gestor de Processos**: Analisa métricas operacionais e conversões
- **Médica**: Acompanha satisfação dos pacientes e oportunidades

## 🔧 Especificações Técnicas

### Funcionalidades Core
1. **Ingesta de Conversas**: Recebe dados via Evolution API → Webhook → N8N
2. **Análise Conversacional**: OpenAI Agents para processamento semântico
3. **Dashboard Interativo**: Streamlit com 4 relatórios principais
4. **Classificação Automática**: IA categoriza pendências por responsável
5. **Alertas Inteligentes**: Notificações para ações urgentes

### Arquitetura do Sistema
```
WhatsApp → Evolution API → Webhook → N8N → PostgreSQL
                                           ↓
OpenAI Agent ← FastAPI Microservice ← Database
     ↓
Streamlit Dashboard ← Processed Insights
```