import unittest
import os
import json
import shutil
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.user_access import UserAccess

class TestUserAccess(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Configura um banco de dados de teste antes de todos os testes.
        """
        cls.test_db_path = "data/databases/test_users.json"
        cls.user_access = UserAccess(db_path=cls.test_db_path)

    def setUp(self):
        """
        Garante que o banco de dados de teste esteja limpo antes de cada teste.
        """
        with open(self.test_db_path, 'w') as db_file:
            json.dump([], db_file)

    def test_register_user(self):
        """
        Testa o registro de um novo usuário.
        """
        response = self.user_access.register_user("Test User", "+5511999999999", "testuser@email.com", "password123")
        self.assertEqual(response, "Usuário cadastrado com sucesso.")

        # Verifica se o usuário foi adicionado ao banco de dados
        with open(self.test_db_path, 'r') as db_file:
            users = json.load(db_file)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]['email'], "testuser@email.com")

    def test_register_duplicate_user(self):
        """
        Testa o registro de um usuário com email ou telefone duplicado.
        """
        self.user_access.register_user("Test User", "+5511999999999", "testuser@email.com", "password123")
        response = self.user_access.register_user("Another User", "+5511999999999", "testuser@email.com", "password456")
        self.assertEqual(response, "Usuário já cadastrado com este email ou telefone.")

    def test_login_user(self):
        """
        Testa o login de um usuário com credenciais corretas.
        """
        self.user_access.register_user("Test User", "+5511999999999", "testuser@email.com", "password123")
        response = self.user_access.login_user("testuser@email.com", "password123")
        self.assertIn("Bem-vindo", response)

    def test_login_invalid_user(self):
        """
        Testa o login com credenciais incorretas.
        """
        response = self.user_access.login_user("invalid@email.com", "wrongpassword")
        self.assertEqual(response, "Email ou senha incorretos.")

    def test_creates_missing_directory(self):
        """Garante que diretórios inexistentes sejam criados automaticamente."""
        temp_dir = "data/temp_databases"
        temp_db_path = os.path.join(temp_dir, "users.json")

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

        UserAccess(db_path=temp_db_path)
        self.assertTrue(os.path.exists(temp_db_path))

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

    @classmethod
    def tearDownClass(cls):
        """
        Remove o banco de dados de teste após todos os testes.
        """
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

if __name__ == "__main__":
    unittest.main()
