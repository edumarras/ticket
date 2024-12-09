import requests
import pytest

MIDDLEWARE_URL = "http://localhost:8000"

@pytest.mark.integration
def test_register_and_login_user():
    # Dados do novo usuário
    new_user = {
        "Login": "usuario_integra",
        "Senha": "senha_integra"
    }

    # 1. Registrar o usuário via middleware
    # O endpoint esperado do middleware para registrar um usuário, conforme sua implementação, é /register (POST)
    # Ajuste se necessário caso a implementação seja diferente.
    resp_register = requests.post(f"{MIDDLEWARE_URL}/register", json=new_user)

    # Esperamos 201 de criação ou 400 se já existir, dependendo da lógica
    assert resp_register.status_code in [201, 400], f"Falha ao registrar usuário: status {resp_register.status_code}"

    # Se foi criado com sucesso (201), verificamos se o retorno foi positivo
    if resp_register.status_code == 201:
        # 2. Tentar logar com o usuário recém-criado
        login_data = {"Login": new_user["Login"], "Senha": new_user["Senha"]}
        resp_login = requests.post(f"{MIDDLEWARE_URL}/login", json=login_data)

        # Se o usuário existe e a senha está correta, espera-se status 200
        # e o retorno com os dados do usuário.
        assert resp_login.status_code == 200, f"Login falhou: status {resp_login.status_code}"

        user_data = resp_login.json()
        assert user_data["login"] == new_user["Login"], "Login retornado difere do esperado"
        assert "id" in user_data, "Usuário logado não retornou ID"
    else:
        # Se já existia (400), não testaremos o login pois já falhou o registro.
        # Neste caso, poderíamos tentar logar com o usuário e senha
        # para verificar se realmente existe.
        login_data = {"Login": new_user["Login"], "Senha": new_user["Senha"]}
        resp_login = requests.post(f"{MIDDLEWARE_URL}/login", json=login_data)

        # Se já existia, significa que o login deve funcionar se a senha estiver correta.
        if resp_login.status_code == 200:
            user_data = resp_login.json()
            assert user_data["login"] == new_user["Login"], "Login retornado difere do esperado"
            assert "id" in user_data, "Usuário logado não retornou ID"
        else:
            # Caso não consiga logar (404 ou 401), há um problema na lógica ou no estado do sistema.
            pytest.fail(f"Não foi possível logar com um usuário supostamente já existente. Status: {resp_login.status_code}")
