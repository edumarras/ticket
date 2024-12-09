import pytest
import requests

MIDDLEWARE_URL = "http://localhost:8000"  # Ajuste caso necessário

@pytest.mark.integration
def test_register_and_login_user():
    # Dados do novo usuário
    new_user = {
        "Login": "usuario_integra",
        "Senha": "senha_integra"
    }

    # 1. Registrar o usuário via middleware
    # O endpoint esperado do middleware para registrar um usuário, conforme sua implementação, é /register (POST)
    resp_register = requests.post(f"{MIDDLEWARE_URL}/register", json=new_user)

    # Esperamos 201 de criação ou 400 se já existir, dependendo da lógica
    assert resp_register.status_code in [201, 400], f"Falha ao registrar usuário: status {resp_register.status_code}"

    # Se foi criado com sucesso (201), verificamos se o retorno foi positivo
    if resp_register.status_code == 201:
        # 2. Tentar logar com o usuário recém-criado
        login_data = {"Login": new_user["Login"], "Senha": new_user["Senha"]}
        resp_login = requests.post(f"{MIDDLEWARE_URL}/login", json=login_data)

        # Se o usuário existe e a senha está correta, espera-se status 200
        assert resp_login.status_code == 200, f"Login falhou: status {resp_login.status_code}"

        user_data = resp_login.json()
        # Aqui usamos "Login" e não "login", pois o backend retorna "Login" com L maiúsculo
        assert user_data["Login"] == new_user["Login"], "Login retornado difere do esperado"
        assert user_data["Senha"] == new_user["Senha"], "Senha retornada difere do esperado"
    else:
        # Caso o status seja 400, significa que o usuário já existe (ou outra falha de registro)
        # Opcionalmente, poderíamos tentar logar assim mesmo, mas não é necessário se não faz parte da lógica.
        pass
