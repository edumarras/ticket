import pytest
import requests
import subprocess
import time

BASE_URL = "http://localhost:3000"

@pytest.fixture(autouse=True)
def restore_db():
    # Espera um pouco caso o container esteja ainda subindo
    time.sleep(1)
    yield
    # Restaura o banco ao final de cada teste
    subprocess.run(["docker", "exec", "backend", "sh", "-c", "sqlite3 /app/data.db < /app/script.sql"], check=True)


def test_get_all_tickets():
    resp = requests.get(f"{BASE_URL}/tickets")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_create_ticket():
    new_ticket = {
        "Titulo": "Teste Ticket",
        "Descricao": "Um ticket de teste",
        "Prioridade": 2
    }
    resp = requests.post(f"{BASE_URL}/tickets", json=new_ticket)
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == "Ticket criado com sucesso!"

    # Verifica se o ticket foi criado
    resp_all = requests.get(f"{BASE_URL}/tickets")
    all_data = resp_all.json()
    assert any(t["Titulo"] == "Teste Ticket" for t in all_data)


def test_update_ticket():
    # Cria um ticket antes de atualizar
    new_ticket = {
        "Titulo": "Ticket Update",
        "Descricao": "Atualizar este ticket",
        "Prioridade": 1
    }
    create_resp = requests.post(f"{BASE_URL}/tickets", json=new_ticket)
    assert create_resp.status_code == 201

    # Atualiza o ticket ID=1 (o primeiro inserido, dependendo do script.sql)
    update_data = {"Status": 1}
    update_resp = requests.put(f"{BASE_URL}/tickets/1", json=update_data)
    assert update_resp.status_code == 200
    data = update_resp.json()
    assert data["status"] == "Ticket atualizado com sucesso!"

    # Verifica se realmente foi atualizado
    andamento_resp = requests.get(f"{BASE_URL}/tickets/andamento")
    andamento_data = andamento_resp.json()
    assert any(t["Status"] == 1 for t in andamento_data)


def test_get_open_tickets():
    resp = requests.get(f"{BASE_URL}/tickets/abertos")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    # Se o script.sql cria algum ticket aberto inicialmente, verifique aqui.
    # Caso contrário, apenas checa se é lista.


def test_get_in_progress_tickets():
    resp = requests.get(f"{BASE_URL}/tickets/andamento")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_get_completed_tickets():
    resp = requests.get(f"{BASE_URL}/tickets/completos")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_get_tickets_by_user():
    # Ajuste o usuário ID conforme o script.sql. 
    # Se script.sql não relacionar tickets a usuarios (ID_pessoa), pode ser lista vazia.
    resp = requests.get(f"{BASE_URL}/tickets/usuario/1")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_get_all_users():
    resp = requests.get(f"{BASE_URL}/usuarios")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    # Verifica se existe pelo menos um usuário, dependendo do script.sql.
    # Por ex: assert len(data) >= 1 se o script criar um usuário inicial.


def test_get_user_by_id():
    # Supondo que exista um usuário com ID=1 no script.sql
    resp = requests.get(f"{BASE_URL}/usuarios/1")
    if resp.status_code == 200:
        data = resp.json()
        assert "Login" in data
    else:
        # Caso não exista, retorna 404
        assert resp.status_code == 404


def test_get_user_by_login():
    # Ajuste o login conforme o script.sql inicial.
    # Ex: user1 criado no script.sql
    resp = requests.get(f"{BASE_URL}/usuarios/login/user1")
    if resp.status_code == 200:
        data = resp.json()
        assert data["Login"] == "user1"
    else:
        assert resp.status_code == 404


def test_create_user():
    new_user = {
        "Login": "user2",
        "Senha": "pass2"
    }
    resp = requests.post(f"{BASE_URL}/usuarios", json=new_user)
    # Pode retornar 201 (criado) ou 400 (se já existe user2)
    assert resp.status_code in [201, 400]
    if resp.status_code == 201:
        data = resp.json()
        assert data["status"] == "Usuário criado com sucesso!"
        # Verifica se realmente foi criado
        resp_all = requests.get(f"{BASE_URL}/usuarios")
        data_all = resp_all.json()
        assert any(u['Login'] == 'user2' for u in data_all)
