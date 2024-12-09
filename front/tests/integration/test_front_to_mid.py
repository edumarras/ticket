import requests

def test_front_to_mid_integration():
    print("\n[TEST] test_front_to_mid_integration")
    # Primeiro registrar um usuário via front (o front chama o mid, que chama o back)
    user_data = {"login": "integuser_front", "senha": "integpass_front"}
    print("Criando usuário via front (POST /register)")
    r = requests.post("http://localhost:5000/register", data=user_data) 
    # Observação: O front espera 'login' e 'senha' no form-data (pois no app.py está request.form)
    # Ajustar conforme necessário. Se precisar json, mudar app.py para request.json.
    print(f"Status code (user creation): {r.status_code}")
    # O front redireciona em caso de sucesso, então status 302 é esperado.
    # Após redirecionamento, checar se a flash message é de sucesso.
    assert r.status_code in [200,302], f"Esperava redirecionamento ao criar usuário pelo front, obtido: {r.status_code}"

    # Tentar logar no front (POST / com login e senha)
    print("Logando via front (POST /)")
    resp = requests.post("http://localhost:5000/", data=user_data)
    print(f"Status code (login): {resp.status_code}")
    # Ao logar com sucesso, o front deve redirecionar para dashboard (302) ou retornar 200
    assert resp.status_code in [200,302], f"Esperava sucesso no login, obtido: {resp.status_code}"

    print("Front to mid integration test passed!\n")
