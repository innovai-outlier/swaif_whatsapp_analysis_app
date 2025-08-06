### APIs Necessárias

#### Endpoints RESTful
```python
# Ingesta de conversas
POST /api/conversations/ingest
POST /api/conversations/batch-ingest

# Análise e processamento
POST /api/analyze/conversation/{conversation_id}
GET /api/analyze/batch/{batch_id}/status

# Relatórios
GET /api/reports/qualitative-summary
GET /api/reports/conversion-funnel
GET /api/reports/pending-actions
GET /api/reports/technical-metrics

# Dashboard data
GET /api/dashboard/overview
GET /api/dashboard/filters
GET /api/dashboard/kpis
```

#### WebSockets (Tempo Real)
```python
# Atualizações em tempo real
ws://localhost:8000/ws/analysis-progress
ws://localhost:8000/ws/new-conversations
ws://localhost:8000/ws/urgent-alerts
```

#### Integrações Externas
- **Evolution API**: Recebimento de mensagens WhatsApp
- **N8N Webhook**: Pipeline de dados automatizado
- **OpenAI API**: Análise conversacional e classificação
- **Streamlit**: Interface de dashboard

#### Exemplo de Payload - Ingesta de Conversa
```json
{
  "whatsapp_contact_id": "5511999999999@c.us",
  "contact_name": "Maria Silva",
  "contact_phone": "11999999999",
  "conversation_start_date": "2024-01-15T10:30:00Z",
  "messages": [
    {
      "timestamp": "2024-01-15T10:30:00Z",
      "sender": "patient",
      "sender_name": "Maria Silva",
      "message": "Oi, gostaria de agendar uma consulta",
      "message_type": "text"
    },
    {
      "timestamp": "2024-01-15T10:35:00Z",
      "sender": "secretary",
      "sender_name": "Ana (Secretária)",
      "message": "Olá Maria! Claro, vou te ajudar. Qual especialidade você precisa?",
      "message_type": "text"
    }
  ],
  "metadata": {
    "source": "evolution_api",
    "n8n_workflow_id": "workflow_123",
    "webhook_timestamp": "2024-01-15T10:45:00Z"
  }
}
```