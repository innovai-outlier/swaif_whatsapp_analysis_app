# Arquivo de Inicialização da Plataforma

class PlatformInitialization:
    def __init__(self):
        """
        Inicializa as configurações da plataforma e carrega as funcionalidades disponíveis.
        """
        self.configurations = {}
        self.features = {}

    def load_features(self):
        """
        Carrega todas as funcionalidades disponíveis na plataforma.
        """
        self.features = {
            "exploratory_analysis": "pages/🔍 Análise Exploratória.py",
            "summaries_and_tasks": "pages/📝 Resumos e Pendências.py",
            "dashboard": "pages/📊 Dashboard.py",
            "opportunity_cost": "pages/💰 Custo de Oportunidade.py",
            "settings": "pages/⚙️ Configurações.py",
            "feature_extraction": [
                "modules/extract_features.py",
                "modules/extract_features_enhanced.py"
            ],
            "feature_analysis": [
                "modules/analyze_features.py",
                "modules/analyze_features_enhanced.py"
            ],
            "trello_integration": "lite/modules/trello_integration/",
            "landing_page": "src/landing_page.py",
            "utilities": "modules/utils.py"
        }

    def initialize_session(self):
        """
        Configura as variáveis de sessão para a plataforma.
        """
        self.configurations = {
            "session_active": True,
            "user_preferences": {},
            "loaded_features": list(self.features.keys())
        }

    def clear_session(self):
        """
        Limpa as configurações de sessão ao final do uso.
        """
        self.configurations = {}

# Exemplo de uso
if __name__ == "__main__":
    platform = PlatformInitialization()
    platform.load_features()
    platform.initialize_session()

    print("Funcionalidades carregadas:", platform.features)
    print("Configurações de sessão:", platform.configurations)

    # Simula o encerramento da sessão
    platform.clear_session()
    print("Configurações após limpar a sessão:", platform.configurations)
