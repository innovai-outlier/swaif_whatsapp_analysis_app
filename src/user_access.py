import json
import os

class UserAccess:
    def __init__(self, db_path="data/databases/users.json"):
        """
        Inicializa a classe de acesso do usuário com o caminho do banco de dados JSON.
        """
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """
        Garante que o arquivo de banco de dados JSON exista.
        """
        try:
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
            if not os.path.exists(self.db_path):
                with open(self.db_path, 'w') as db_file:
                    json.dump([], db_file)
        except Exception as e:
            raise Exception(f"Erro ao garantir a existência do banco de dados: {str(e)}")

    def register_user(self, name, phone, email, password):
        """
        Registra um novo usuário no banco de dados.
        """
        try:
            with open(self.db_path, 'r') as db_file:
                users = json.load(db_file)

            # Verifica se o email ou telefone já está cadastrado
            for user in users:
                if user['email'] == email or user['phone'] == phone:
                    return "Usuário já cadastrado com este email ou telefone."

            # Adiciona o novo usuário
            new_user = {
                "name": name,
                "phone": phone,
                "email": email,
                "password": password  # Em um sistema real, a senha deve ser criptografada
            }
            users.append(new_user)

            with open(self.db_path, 'w') as db_file:
                json.dump(users, db_file, indent=4)

            return "Usuário cadastrado com sucesso."
        except json.JSONDecodeError:
            return "Erro ao processar o banco de dados. O arquivo pode estar corrompido."
        except Exception as e:
            return f"Erro ao registrar usuário: {str(e)}"

    def login_user(self, email, password):
        """
        Realiza o login do usuário verificando email e senha.
        """
        try:
            with open(self.db_path, 'r') as db_file:
                users = json.load(db_file)

            if not users:
                return "Email ou senha incorretos."

            for user in users:
                if user['email'] == email and user['password'] == password:
                    return f"Bem-vindo, {user['name']}!"

            return "Email ou senha incorretos."
        except json.JSONDecodeError:
            return "Erro ao processar o banco de dados. O arquivo pode estar corrompido."
        except Exception as e:
            return f"Erro ao realizar login: {str(e)}"

    def logout_user(self):
        """
        Realiza o logout do usuário.
        """
        try:
            return "Logout realizado com sucesso."
        except Exception as e:
            return f"Erro ao realizar logout: {str(e)}"

# Exemplo de uso
if __name__ == "__main__":
    user_access = UserAccess()

    # Cadastro de usuário
    print(user_access.register_user("João Silva", "+5511999999999", "joao@email.com", "senha123"))

    # Tentativa de login
    print(user_access.login_user("joao@email.com", "senha123"))

    # Logout
    print(user_access.logout_user())
