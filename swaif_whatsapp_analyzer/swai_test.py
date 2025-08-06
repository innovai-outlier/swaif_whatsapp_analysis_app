# SWAI System Test - Verificação Rápida do Sistema
# Filosofia: Testes simples para máxima confiança

"""
Script de teste para verificar se todos os componentes SWAI estão funcionando
Execute este script antes de usar o sistema principal
"""

import sys
import traceback
from pathlib import Path

def test_imports():
    """Testa se todas as importações estão funcionando"""
    print("🔍 Testando importações...")
    
    try:
        # Configurações
        from swai_settings import SWAI_SETTINGS, get_financial_settings
        print("✅ swai_settings - OK")
        
        # Features
        from swai_features import feature_enabled, FEATURES
        print("✅ swai_features - OK")
        
        # Core
        from swai_core import SWAIAnalyzer, create_sample_data
        print("✅ swai_core - OK")
        
        # UI Modules
        from swai_ui_dashboard import show_dashboard
        from swai_ui_analysis import show_analysis  
        from swai_ui_cost import show_cost_calculator
        from swai_ui_config import show_configuration
        print("✅ swai_ui_* - OK")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print(f"📍 Detalhes: {traceback.format_exc()}")
        return False

def test_core_functionality():
    """Testa funcionalidades básicas do core"""
    print("\n🧠 Testando funcionalidades core...")
    
    try:
        from swai_settings import SWAI_SETTINGS
        from swai_core import SWAIAnalyzer, create_sample_data
        
        # Criar analisador
        analyzer = SWAIAnalyzer(SWAI_SETTINGS)
        print("✅ Analyzer criado")
        
        # Criar dados de exemplo
        sample_df = create_sample_data()
        print(f"✅ Dados de exemplo: {len(sample_df)} conversas")
        
        # Calcular métricas
        metrics = analyzer.calculate_basic_metrics(sample_df)
        print("✅ Métricas calculadas")
        
        # Testar formatação
        formatted_currency = analyzer.format_currency(1000)
        formatted_percentage = analyzer.format_percentage(0.75)
        print(f"✅ Formatação: {formatted_currency}, {formatted_percentage}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no core: {e}")
        print(f"📍 Detalhes: {traceback.format_exc()}")
        return False

def test_features_system():
    """Testa sistema de funcionalidades liga-desliga"""
    print("\n🎛️ Testando sistema de features...")
    
    try:
        from swai_features import feature_enabled, toggle_feature, get_enabled_features, feature_count
        
        # Testar verificação de features
        dashboard_enabled = feature_enabled("dashboard")
        print(f"✅ Dashboard enabled: {dashboard_enabled}")
        
        # Testar contagem
        count = feature_count()
        print(f"✅ Feature count: {count['enabled']}/{count['total']}")
        
        # Testar lista de features ativas
        enabled_features = get_enabled_features()
        print(f"✅ Features ativas: {len(enabled_features)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema de features: {e}")
        print(f"📍 Detalhes: {traceback.format_exc()}")
        return False

def test_financial_calculations():
    """Testa cálculos financeiros"""
    print("\n💰 Testando cálculos financeiros...")
    
    try:
        from swai_settings import get_financial_settings
        from swai_core import SWAIAnalyzer, create_sample_data
        
        analyzer = SWAIAnalyzer({})
        sample_df = create_sample_data()
        
        # Calcular métricas
        metrics = analyzer.calculate_basic_metrics(sample_df)
        
        # Calcular custo de oportunidade
        financial_config = get_financial_settings()
        opportunity_cost = analyzer.calculate_opportunity_cost(metrics, financial_config)
        
        print(f"✅ Custo diário: R$ {opportunity_cost['current_costs']['diario']:.2f}")
        print(f"✅ Taxa de sucesso: {metrics['summary']['success_rate']:.1%}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos cálculos financeiros: {e}")
        print(f"📍 Detalhes: {traceback.format_exc()}")
        return False

def test_data_directories():
    """Verifica estrutura de diretórios"""
    print("\n📁 Verificando estrutura de diretórios...")
    
    try:
        from swai_settings import SWAI_SETTINGS
        
        # Verificar diretórios principais
        data_dir = Path(SWAI_SETTINGS.get('SUCCESS_CASES_DIR', 'data/success_cases')).parent
        
        if not data_dir.exists():
            print(f"📁 Criando diretório: {data_dir}")
            data_dir.mkdir(parents=True, exist_ok=True)
        
        success_dir = Path(SWAI_SETTINGS.get('SUCCESS_CASES_DIR', 'data/success_cases'))
        fail_dir = Path(SWAI_SETTINGS.get('FAIL_CASES_DIR', 'data/fail_cases'))
        
        success_dir.mkdir(parents=True, exist_ok=True)
        fail_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Diretório de sucessos: {success_dir}")
        print(f"✅ Diretório de falhas: {fail_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na estrutura de diretórios: {e}")
        print(f"📍 Detalhes: {traceback.format_exc()}")
        return False

def run_all_tests():
    """Executa todos os testes"""
    print("🧠 SWAI System Test - Verificação Completa")
    print("=" * 50)
    
    tests = [
        ("Importações", test_imports),
        ("Core Functionality", test_core_functionality), 
        ("Sistema de Features", test_features_system),
        ("Cálculos Financeiros", test_financial_calculations),
        ("Estrutura de Diretórios", test_data_directories)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))
    
    # Relatório final
    print("\n" + "="*50)
    print("📊 RELATÓRIO FINAL DOS TESTES")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{test_name:<25} {status}")
        if success:
            passed += 1
    
    print("-" * 50)
    print(f"Sucessos: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema SWAI está pronto para uso!")
        print("\n🚀 Para iniciar o sistema:")
        print("   streamlit run swai_app_main.py")
    else:
        print(f"\n⚠️  {total-passed} teste(s) falharam")
        print("🔧 Verifique os erros acima antes de usar o sistema")
    
    return passed == total

def create_sample_conversation_files():
    """Cria arquivos de conversa de exemplo para teste"""
    print("\n📝 Criando conversas de exemplo...")
    
    try:
        from swai_settings import SWAI_SETTINGS
        
        success_dir = Path(SWAI_SETTINGS.get('SUCCESS_CASES_DIR', 'data/success_cases'))
        fail_dir = Path(SWAI_SETTINGS.get('FAIL_CASES_DIR', 'data/fail_cases'))
        
        # Exemplo de conversa de sucesso
        success_conversation = """[15/12/2024, 09:30:00] Secretária: Bom dia! Em que posso ajudá-la?
[15/12/2024, 09:31:15] Paciente: Olá! Gostaria de agendar uma consulta com a doutora.
[15/12/2024, 09:32:00] Secretária: Claro! Temos disponibilidade na quinta-feira às 14h ou na sexta às 10h. Qual prefere?
[15/12/2024, 09:33:00] Paciente: Quinta às 14h seria perfeito! Qual o valor da consulta?
[15/12/2024, 09:34:00] Secretária: A consulta custa R$ 800,00. Posso confirmar seu agendamento?
[15/12/2024, 09:35:00] Paciente: Sim, pode agendar! Obrigada!
[15/12/2024, 09:36:00] Secretária: Agendamento confirmado para quinta às 14h. Até lá!"""
        
        # Exemplo de conversa de falha
        fail_conversation = """[16/12/2024, 14:20:00] Secretária: Boa tarde! Como posso ajudar?
[16/12/2024, 14:21:00] Paciente: Oi, queria saber o preço da consulta.
[16/12/2024, 14:22:00] Secretária: A consulta custa R$ 800,00.
[16/12/2024, 14:25:00] Paciente: Nossa, é caro. Obrigada.
[16/12/2024, 14:26:00] Secretária: De nada!"""
        
        # Criar arquivos
        success_conv_dir = success_dir / "WhatsApp Chat - Paciente Exemplo 1"
        success_conv_dir.mkdir(parents=True, exist_ok=True)
        (success_conv_dir / "_chat.txt").write_text(success_conversation, encoding='utf-8')
        
        fail_conv_dir = fail_dir / "WhatsApp Chat - Paciente Exemplo 2"  
        fail_conv_dir.mkdir(parents=True, exist_ok=True)
        (fail_conv_dir / "_chat.txt").write_text(fail_conversation, encoding='utf-8')
        
        print("✅ Conversas de exemplo criadas")
        print(f"   Sucesso: {success_conv_dir}")
        print(f"   Falha: {fail_conv_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar conversas de exemplo: {e}")
        return False

def quick_start_guide():
    """Guia rápido de inicialização"""
    print("\n" + "="*50)
    print("🚀 GUIA RÁPIDO DE INICIALIZAÇÃO")
    print("=" * 50)
    
    print("""
1. 📦 INSTALAR DEPENDÊNCIAS:
   pip install -r swai_requirements.txt

2. 🧪 EXECUTAR TESTES:
   python swai_test.py

3. 🚀 INICIAR SISTEMA:
   streamlit run swai_app_main.py

4. 🌐 ACESSAR INTERFACE:
   http://localhost:8501

5. 🎯 PRIMEIROS PASSOS:
   - Configure parâmetros financeiros
   - Gere dados de exemplo ou adicione conversas reais
   - Explore o dashboard e análises

📖 Para mais informações, consulte README_SWAI.md
    """)

if __name__ == "__main__":
    # Executar testes
    success = run_all_tests()
    
    # Criar conversas de exemplo se todos os testes passaram
    if success:
        create_sample_conversation_files()
    
    # Mostrar guia de inicialização
    quick_start_guide()
    
    # Exit code baseado no resultado dos testes
    sys.exit(0 if success else 1)
