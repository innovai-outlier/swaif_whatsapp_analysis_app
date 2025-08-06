# SWAI Core - Núcleo de Análise Simplificado
# Filosofia: Máxima eficiência, mínima complexidade

"""
Módulo core do SWAI WhatsApp Analyzer
Implementa a análise principal de conversas seguindo os princípios SWAI
"""

import pandas as pd
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SWAIAnalyzer:
    """
    Analisador principal SWAI
    Baseado no princípio Senna: simplicidade que transcende complexidade
    """
    
    def __init__(self, settings: dict):
        self.settings = settings
        self.agendamento_keywords = settings.get("AGENDAMENTO_KEYWORDS", [])
        self.preco_keywords = settings.get("PRECO_KEYWORDS", [])
        
    def load_conversation_data(self) -> Optional[pd.DataFrame]:
        """
        Carrega dados das conversas processadas
        
        Returns:
            pd.DataFrame: Dados carregados ou None se não encontrar
        """
        try:
            csv_path = self.settings.get("FEATURES_CSV")
            if csv_path and Path(csv_path).exists():
                df = pd.read_csv(csv_path)
                logger.info(f"✅ Dados carregados: {len(df)} conversas")
                return df
            else:
                logger.warning("❌ Arquivo de dados não encontrado")
                return None
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            return None
    
    def calculate_basic_metrics(self, df: pd.DataFrame) -> Dict:
        """
        Calcula métricas básicas das conversas
        
        Args:
            df (pd.DataFrame): DataFrame com dados das conversas
            
        Returns:
            Dict: Métricas calculadas
        """
        if df is None or df.empty:
            return {}
        
        # Contadores básicos
        total_conversations = len(df)
        success_count = len(df[df['chat_type'] == 'success'])
        fail_count = len(df[df['chat_type'] == 'fail'])
        
        # Taxas
        success_rate = success_count / total_conversations if total_conversations > 0 else 0
        failure_rate = fail_count / total_conversations if total_conversations > 0 else 0
        
        # Médias gerais
        avg_duration = df['duration_minutes'].mean()
        avg_messages = df['total_messages'].mean()
        avg_secretary_messages = df['secretary_messages'].mean()
        avg_patient_messages = df['patient_messages'].mean()
        
        # Médias por tipo
        success_df = df[df['chat_type'] == 'success']
        fail_df = df[df['chat_type'] == 'fail']
        
        success_metrics = {}
        fail_metrics = {}
        
        if not success_df.empty:
            success_metrics = {
                'avg_duration': success_df['duration_minutes'].mean(),
                'avg_messages': success_df['total_messages'].mean(),
                'avg_secretary_messages': success_df['secretary_messages'].mean(),
                'avg_patient_messages': success_df['patient_messages'].mean(),
                'avg_interactions': success_df['num_interactions'].mean(),
                'avg_agendamento_keywords': success_df['agendamento_keywords'].mean(),
                'avg_preco_keywords': success_df['preco_keywords'].mean()
            }
        
        if not fail_df.empty:
            fail_metrics = {
                'avg_duration': fail_df['duration_minutes'].mean(),
                'avg_messages': fail_df['total_messages'].mean(),
                'avg_secretary_messages': fail_df['secretary_messages'].mean(),
                'avg_patient_messages': fail_df['patient_messages'].mean(),
                'avg_interactions': fail_df['num_interactions'].mean(),
                'avg_agendamento_keywords': fail_df['agendamento_keywords'].mean(),
                'avg_preco_keywords': fail_df['preco_keywords'].mean()
            }
        
        return {
            'summary': {
                'total_conversations': total_conversations,
                'success_count': success_count,
                'fail_count': fail_count,
                'success_rate': success_rate,
                'failure_rate': failure_rate,
                'avg_duration': avg_duration,
                'avg_messages': avg_messages,
                'avg_secretary_messages': avg_secretary_messages,
                'avg_patient_messages': avg_patient_messages
            },
            'success_metrics': success_metrics,
            'fail_metrics': fail_metrics
        }
    
    def calculate_opportunity_cost(self, metrics: Dict, financial_config: Dict) -> Dict:
        """
        Calcula custo de oportunidade baseado nas métricas
        
        Args:
            metrics (Dict): Métricas básicas
            financial_config (Dict): Configurações financeiras
            
        Returns:
            Dict: Cálculos de custo de oportunidade
        """
        if not metrics or 'summary' not in metrics:
            return {}
        
        summary = metrics['summary']
        failure_rate = summary.get('failure_rate', 0)
        
        valor_consulta = financial_config.get('valor_consulta', 800)
        leads_diarios = financial_config.get('leads_diarios', 5)
        dias_uteis_mes = financial_config.get('dias_uteis_mes', 20)
        dias_uteis_ano = financial_config.get('dias_uteis_ano', 240)
        
        # Cálculos de custo
        custo_diario = (leads_diarios * failure_rate) * valor_consulta
        custo_semanal = custo_diario * 5  # 5 dias úteis
        custo_mensal = custo_diario * dias_uteis_mes
        custo_anual = custo_diario * dias_uteis_ano
        
        # Potencial de melhoria
        current_success_rate = summary.get('success_rate', 0)
        target_success_rate = 0.8  # Meta de 80%
        improvement_potential = target_success_rate - current_success_rate
        
        potential_daily_gain = (leads_diarios * improvement_potential) * valor_consulta
        potential_monthly_gain = potential_daily_gain * dias_uteis_mes
        potential_annual_gain = potential_daily_gain * dias_uteis_ano
        
        return {
            'current_costs': {
                'diario': custo_diario,
                'semanal': custo_semanal,
                'mensal': custo_mensal,
                'anual': custo_anual
            },
            'improvement_potential': {
                'current_rate': current_success_rate,
                'target_rate': target_success_rate,
                'improvement_needed': improvement_potential,
                'potential_daily_gain': potential_daily_gain,
                'potential_monthly_gain': potential_monthly_gain,
                'potential_annual_gain': potential_annual_gain
            },
            'roi_analysis': {
                'break_even_conversations': valor_consulta / custo_diario if custo_diario > 0 else 0,
                'cost_per_failed_lead': valor_consulta,
                'value_per_success': valor_consulta
            }
        }
    
    def generate_insights(self, metrics: Dict, opportunity_cost: Dict) -> List[Dict]:
        """
        Gera insights e recomendações baseados nos dados
        
        Args:
            metrics (Dict): Métricas básicas
            opportunity_cost (Dict): Análise de custo
            
        Returns:
            List[Dict]: Lista de insights
        """
        insights = []
        
        if not metrics or 'summary' not in metrics:
            return insights
        
        summary = metrics['summary']
        success_metrics = metrics.get('success_metrics', {})
        fail_metrics = metrics.get('fail_metrics', {})
        
        # Insight sobre taxa de conversão
        success_rate = summary.get('success_rate', 0)
        if success_rate < 0.4:
            insights.append({
                'type': 'warning',
                'title': 'Taxa de Conversão Baixa',
                'message': f'Taxa atual de {success_rate:.1%} está abaixo do ideal (60%+)',
                'action': 'Revisar processo de atendimento e treinamento da equipe'
            })
        elif success_rate > 0.7:
            insights.append({
                'type': 'success',
                'title': 'Excelente Taxa de Conversão',
                'message': f'Taxa de {success_rate:.1%} está acima da média do mercado',
                'action': 'Manter padrão atual e documentar melhores práticas'
            })
        
        # Insight sobre duração das conversas
        if success_metrics and fail_metrics:
            success_duration = success_metrics.get('avg_duration', 0)
            fail_duration = fail_metrics.get('avg_duration', 0)
            
            if success_duration > fail_duration * 1.2:
                insights.append({
                    'type': 'info',
                    'title': 'Conversas Longas = Mais Sucesso',
                    'message': f'Sucessos duram {success_duration:.1f}min vs {fail_duration:.1f}min das falhas',
                    'action': 'Investir tempo na qualidade do atendimento paga'
                })
        
        # Insight sobre palavras-chave
        if success_metrics and fail_metrics:
            success_agendamento = success_metrics.get('avg_agendamento_keywords', 0)
            fail_agendamento = fail_metrics.get('avg_agendamento_keywords', 0)
            
            if success_agendamento > fail_agendamento * 1.5:
                insights.append({
                    'type': 'info',
                    'title': 'Foco em Agendamento Funciona',
                    'message': f'Sucessos usam {success_agendamento:.1f} vs {fail_agendamento:.1f} palavras de agendamento',
                    'action': 'Treinar equipe para direcionar conversas ao agendamento'
                })
        
        # Insight sobre custo de oportunidade
        if opportunity_cost and 'current_costs' in opportunity_cost:
            custo_mensal = opportunity_cost['current_costs'].get('mensal', 0)
            if custo_mensal > 10000:  # R$ 10k
                insights.append({
                    'type': 'warning',
                    'title': 'Alto Custo de Oportunidade',
                    'message': f'Perdendo R$ {custo_mensal:,.0f} por mês em leads não convertidos',
                    'action': 'Priorizar melhoria do processo - ROI garantido'
                })
        
        return insights
    
    def format_currency(self, value: float) -> str:
        """Formata valor como moeda brasileira"""
        return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    def format_percentage(self, value: float) -> str:
        """Formata valor como percentual"""
        return f"{value:.1%}"

class SWAIConversationExtractor:
    """
    Extrator simplificado de features das conversas
    Foco na essência: o que realmente importa para o negócio
    """
    
    def __init__(self, settings: dict):
        self.settings = settings
        self.agendamento_keywords = settings.get("AGENDAMENTO_KEYWORDS", [])
        self.preco_keywords = settings.get("PRECO_KEYWORDS", [])
    
    def extract_features_from_file(self, file_path: str, chat_type: str) -> Dict:
        """
        Extrai features de um arquivo de conversa individual
        
        Args:
            file_path (str): Caminho para o arquivo
            chat_type (str): Tipo da conversa (success/fail)
            
        Returns:
            Dict: Features extraídas
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            return self._analyze_conversation_content(content, chat_type)
            
        except Exception as e:
            logger.error(f"Erro ao processar {file_path}: {e}")
            return {}
    
    def _analyze_conversation_content(self, content: str, chat_type: str) -> Dict:
        """
        Analisa o conteúdo da conversa e extrai features
        
        Args:
            content (str): Conteúdo da conversa
            chat_type (str): Tipo da conversa
            
        Returns:
            Dict: Features extraídas
        """
        lines = content.strip().split('\n')
        
        # Extração de mensagens
        messages = []
        for line in lines:
            # Regex para capturar mensagens do WhatsApp
            # Formato: [DD/MM/AAAA, HH:MM:SS] Nome: Mensagem
            match = re.match(r'\[(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2}:\d{2})\] ([^:]+): (.+)', line)
            if match:
                date_str, time_str, sender, message = match.groups()
                messages.append({
                    'datetime': f"{date_str} {time_str}",
                    'sender': sender.strip(),
                    'message': message.strip()
                })
        
        if not messages:
            return {}
        
        # Features básicas
        total_messages = len(messages)
        
        # Identificar secretária (assume que é quem mais manda mensagens ou primeiro nome)
        senders = [msg['sender'] for msg in messages]
        sender_counts = {}
        for sender in senders:
            sender_counts[sender] = sender_counts.get(sender, 0) + 1
        
        # Secretária = quem mais manda mensagens
        secretary_name = max(sender_counts, key=sender_counts.get) if sender_counts else ""
        
        secretary_messages = sum(1 for msg in messages if msg['sender'] == secretary_name)
        patient_messages = total_messages - secretary_messages
        
        # Análise temporal
        try:
            first_time = datetime.strptime(messages[0]['datetime'], '%d/%m/%Y %H:%M:%S')
            last_time = datetime.strptime(messages[-1]['datetime'], '%d/%m/%Y %H:%M:%S')
            duration_minutes = (last_time - first_time).total_seconds() / 60
        except:
            duration_minutes = 0
        
        # Contagem de interações (mudanças de remetente)
        interactions = 0
        last_sender = ""
        for msg in messages:
            if msg['sender'] != last_sender:
                interactions += 1
                last_sender = msg['sender']
        
        # Análise de conteúdo
        full_text = " ".join([msg['message'].lower() for msg in messages])
        
        agendamento_count = sum(1 for keyword in self.agendamento_keywords 
                               if keyword.lower() in full_text)
        
        preco_count = sum(1 for keyword in self.preco_keywords 
                         if keyword.lower() in full_text)
        
        # Contagem de perguntas (aproximada)
        patient_questions = sum(1 for msg in messages 
                               if msg['sender'] != secretary_name and '?' in msg['message'])
        
        secretary_questions = sum(1 for msg in messages 
                                 if msg['sender'] == secretary_name and '?' in msg['message'])
        
        # Contagem de mensagens de áudio/mídia
        audio_messages = sum(1 for msg in messages 
                            if any(term in msg['message'].lower() for term in ['áudio', 'audio', '<mídia', 'media']))
        
        return {
            'chat_name': Path(file_path).parent.name,
            'chat_type': chat_type,
            'duration_minutes': duration_minutes,
            'total_messages': total_messages,
            'secretary_messages': secretary_messages,
            'patient_messages': patient_messages,
            'num_interactions': interactions,
            'agendamento_keywords': agendamento_count,
            'preco_keywords': preco_count,
            'patient_questions': patient_questions,
            'secretary_questions': secretary_questions,
            'audio_messages': audio_messages,
            'secretary_name': secretary_name
        }
    
    def process_all_conversations(self) -> pd.DataFrame:
        """
        Processa todas as conversas nas pastas success_cases e fail_cases
        
        Returns:
            pd.DataFrame: DataFrame com features extraídas
        """
        all_features = []
        
        # Processar casos de sucesso
        success_dir = Path(self.settings.get("SUCCESS_CASES_DIR", ""))
        if success_dir.exists():
            for conversation_dir in success_dir.iterdir():
                if conversation_dir.is_dir():
                    chat_file = conversation_dir / "_chat.txt"
                    if chat_file.exists():
                        features = self.extract_features_from_file(str(chat_file), "success")
                        if features:
                            all_features.append(features)
        
        # Processar casos de falha
        fail_dir = Path(self.settings.get("FAIL_CASES_DIR", ""))
        if fail_dir.exists():
            for conversation_dir in fail_dir.iterdir():
                if conversation_dir.is_dir():
                    chat_file = conversation_dir / "_chat.txt"
                    if chat_file.exists():
                        features = self.extract_features_from_file(str(chat_file), "fail")
                        if features:
                            all_features.append(features)
        
        if all_features:
            df = pd.DataFrame(all_features)
            logger.info(f"✅ Processadas {len(df)} conversas")
            return df
        else:
            logger.warning("❌ Nenhuma conversa encontrada para processar")
            return pd.DataFrame()

# Funções auxiliares simplificadas
def create_sample_data() -> pd.DataFrame:
    """
    Cria dados de exemplo para demonstração
    
    Returns:
        pd.DataFrame: DataFrame com dados de exemplo
    """
    import numpy as np
    
    np.random.seed(42)
    
    # Gerar dados sintéticos realistas
    n_conversations = 50
    
    data = []
    for i in range(n_conversations):
        chat_type = 'success' if np.random.random() > 0.4 else 'fail'  # 60% success rate
        
        if chat_type == 'success':
            # Conversas de sucesso tendem a ser mais longas e engajadas
            duration = np.random.normal(45, 15)  # 45 min média
            total_messages = int(np.random.normal(25, 8))
            agendamento_keywords = int(np.random.poisson(4))
            preco_keywords = int(np.random.poisson(2))
        else:
            # Conversas de falha tendem a ser mais curtas
            duration = np.random.normal(20, 10)  # 20 min média
            total_messages = int(np.random.normal(12, 5))
            agendamento_keywords = int(np.random.poisson(1))
            preco_keywords = int(np.random.poisson(3))
        
        # Garantir valores positivos
        duration = max(1, duration)
        total_messages = max(1, total_messages)
        agendamento_keywords = max(0, agendamento_keywords)
        preco_keywords = max(0, preco_keywords)
        
        secretary_messages = int(total_messages * np.random.uniform(0.4, 0.7))
        patient_messages = total_messages - secretary_messages
        
        data.append({
            'chat_name': f'Conversa_{i+1}',
            'chat_type': chat_type,
            'duration_minutes': duration,
            'total_messages': total_messages,
            'secretary_messages': secretary_messages,
            'patient_messages': patient_messages,
            'num_interactions': int(total_messages * np.random.uniform(0.3, 0.8)),
            'agendamento_keywords': agendamento_keywords,
            'preco_keywords': preco_keywords,
            'patient_questions': int(np.random.poisson(3)),
            'secretary_questions': int(np.random.poisson(2)),
            'audio_messages': int(np.random.poisson(1))
        })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Teste básico das funcionalidades
    from swai_settings import SWAI_SETTINGS
    
    analyzer = SWAIAnalyzer(SWAI_SETTINGS)
    
    # Criar dados de exemplo se não existirem dados reais
    sample_df = create_sample_data()
    
    # Calcular métricas
    metrics = analyzer.calculate_basic_metrics(sample_df)
    print("📊 Métricas básicas calculadas")
    
    # Calcular custo de oportunidade
    financial_config = {
        'valor_consulta': 800,
        'leads_diarios': 5,
        'dias_uteis_mes': 20,
        'dias_uteis_ano': 240
    }
    
    opportunity_cost = analyzer.calculate_opportunity_cost(metrics, financial_config)
    print("💰 Custo de oportunidade calculado")
    
    # Gerar insights
    insights = analyzer.generate_insights(metrics, opportunity_cost)
    print(f"💡 {len(insights)} insights gerados")
    
    print("✅ SWAI Core funcionando corretamente!")
