### Modelo de Dados

```sql
-- Tabela principal de conversas
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    whatsapp_contact_id VARCHAR(50) NOT NULL,
    contact_name VARCHAR(255),
    contact_phone VARCHAR(20),
    conversation_start_date TIMESTAMP NOT NULL,
    conversation_end_date TIMESTAMP,
    total_messages INTEGER DEFAULT 0,
    raw_messages JSONB NOT NULL,
    processed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Análise qualitativa
CREATE TABLE conversation_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    care_quality_score INTEGER CHECK (care_quality_score >= 1 AND care_quality_score <= 10),
    care_quality_summary TEXT,
    pre_consultation_quality TEXT,
    scheduling_quality TEXT,
    post_consultation_quality TEXT,
    overall_sentiment VARCHAR(20) CHECK (overall_sentiment IN ('positive', 'neutral', 'negative')),
    key_insights TEXT[],
    improvement_suggestions TEXT[],
    analyzed_at TIMESTAMP DEFAULT NOW()
);

-- Funil de conversão
CREATE TABLE conversion_funnel (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    showed_interest BOOLEAN DEFAULT FALSE,
    exposed_pain_points BOOLEAN DEFAULT FALSE,
    aligned_with_mission BOOLEAN DEFAULT FALSE,
    wants_to_schedule BOOLEAN DEFAULT FALSE,
    conversion_stage VARCHAR(50) CHECK (conversion_stage IN ('interest', 'pain', 'alignment', 'scheduling', 'converted')),
    pain_points TEXT[],
    alignment_indicators TEXT[],
    scheduling_intent_confidence DECIMAL(3,2) CHECK (scheduling_intent_confidence >= 0.00 AND scheduling_intent_confidence <= 1.00),
    financial_commitment_evidence TEXT,
    analyzed_at TIMESTAMP DEFAULT NOW()
);

-- Pendências operacionais
CREATE TABLE pending_actions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    action_description TEXT NOT NULL,
    responsible_role VARCHAR(50) NOT NULL CHECK (responsible_role IN ('secretaria', 'gestor_processos', 'medica')),
    priority_level VARCHAR(20) DEFAULT 'medium' CHECK (priority_level IN ('low', 'medium', 'high', 'urgent')),
    category VARCHAR(50) CHECK (category IN ('agendamento', 'financeiro', 'clinico', 'operacional')),
    due_date DATE,
    estimated_effort_minutes INTEGER CHECK (estimated_effort_minutes > 0),
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    completed_by VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Métricas técnicas diárias
CREATE TABLE technical_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_date DATE NOT NULL UNIQUE,
    total_conversations INTEGER DEFAULT 0,
    avg_response_time_minutes DECIMAL(8,2),
    conversion_rate DECIMAL(5,4),
    missed_opportunities_count INTEGER DEFAULT 0,
    missed_opportunities_value DECIMAL(10,2) DEFAULT 0.00,
    keyword_frequency JSONB,
    sentiment_distribution JSONB,
    quality_score_avg DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Palavras-chave e correlações
CREATE TABLE keyword_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    keywords JSONB NOT NULL,
    keyword_sentiment JSONB,
    correlation_matrix JSONB,
    topic_clusters TEXT[],
    analyzed_at TIMESTAMP DEFAULT NOW()
);

-- Índices otimizados para performance
CREATE INDEX idx_conversations_date ON conversations(conversation_start_date);
CREATE INDEX idx_conversations_phone ON conversations(contact_phone);
CREATE INDEX idx_conversations_processed ON conversations(processed_at);
CREATE INDEX idx_pending_actions_responsible ON pending_actions(responsible_role, priority_level);
CREATE INDEX idx_pending_actions_due_date ON pending_actions(due_date) WHERE is_completed = FALSE;
CREATE INDEX idx_technical_metrics_date ON technical_metrics(analysis_date);
CREATE INDEX idx_conversion_stage ON conversion_funnel(conversion_stage);

-- Trigger para atualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_conversations_updated_at 
    BEFORE UPDATE ON conversations 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```