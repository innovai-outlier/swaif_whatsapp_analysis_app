import pandas as pd
import json
import os
from modules.constants import EXTRACTED_FEATURES_CSV, DETAILED_ANALYSIS_JSON, VALOR_MEDIO_CONSULTA, LEADS_DIARIOS

def load_data():
    """Load extracted features data"""
    try:
        df = pd.read_csv(EXTRACTED_FEATURES_CSV)
        return df
    except FileNotFoundError:
        return None

def load_detailed_analysis():
    """Load detailed analysis results"""
    try:
        with open(DETAILED_ANALYSIS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return None

def calculate_opportunity_cost(df, valor_consulta=VALOR_MEDIO_CONSULTA, leads_diarios=LEADS_DIARIOS):
    """Calculate opportunity cost based on conversion rates"""
    if df is None or df.empty:
        return None
    
    success_count = df[df['chat_type'] == 'success'].shape[0]
    fail_count = df[df['chat_type'] == 'fail'].shape[0]
    total_cases = success_count + fail_count
    
    if total_cases == 0:
        return None
    
    success_rate = success_count / total_cases
    failure_rate = fail_count / total_cases
    
    custo_oportunidade_diario = (leads_diarios * failure_rate) * valor_consulta
    custo_oportunidade_semanal = custo_oportunidade_diario * 5  # 5 dias úteis
    custo_oportunidade_mensal = custo_oportunidade_diario * 20  # 20 dias úteis
    custo_oportunidade_anual = custo_oportunidade_diario * 240  # 240 dias úteis
    
    return {
        'total_cases': total_cases,
        'success_count': success_count,
        'fail_count': fail_count,
        'success_rate': success_rate,
        'failure_rate': failure_rate,
        'custo_oportunidade_diario': custo_oportunidade_diario,
        'custo_oportunidade_semanal': custo_oportunidade_semanal,
        'custo_oportunidade_mensal': custo_oportunidade_mensal,
        'custo_oportunidade_anual': custo_oportunidade_anual
    }

def format_currency(value):
    """Format value as Brazilian currency"""
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def format_percentage(value):
    """Format value as percentage"""
    return f"{value:.1%}"

def get_summary_stats(df):
    """Get summary statistics for the dataset"""
    if df is None or df.empty:
        return None
    
    stats = {}
    
    # Basic stats
    stats['total_conversations'] = len(df)
    stats['success_conversations'] = len(df[df['chat_type'] == 'success'])
    stats['fail_conversations'] = len(df[df['chat_type'] == 'fail'])
    
    # Average metrics
    stats['avg_duration'] = df['duration_minutes'].mean()
    stats['avg_messages'] = df['total_messages'].mean()
    stats['avg_secretary_messages'] = df['secretary_messages'].mean()
    stats['avg_patient_messages'] = df['patient_messages'].mean()
    
    # Success vs Fail comparison
    success_df = df[df['chat_type'] == 'success']
    fail_df = df[df['chat_type'] == 'fail']
    
    if not success_df.empty and not fail_df.empty:
        stats['success_avg_duration'] = success_df['duration_minutes'].mean()
        stats['fail_avg_duration'] = fail_df['duration_minutes'].mean()
        stats['success_avg_messages'] = success_df['total_messages'].mean()
        stats['fail_avg_messages'] = fail_df['total_messages'].mean()
    
    return stats

def check_file_exists(filepath):
    """Check if file exists"""
    return os.path.exists(filepath)

