import pytest
import requests
import time

BASE_URL = "http://localhost:3000"

# Como este teste é apenas para checar endpoints em uma nova imagem,
# não restauraremos o DB ou manipularemos o estado.
# Supondo que o container já esteja rodando quando o teste iniciar no Actions.

def test_get_all_tickets():
    resp = requests.get(f"{BASE_URL}/tickets")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)  # Apenas verifica se retorna uma lista.

def test_create_ticket():
    new_ticket = {
        "Titulo": "Teste Ticket Endpoint",
        "Descricao": "Checando endpoint POST",
        "Prioridade": 2
    }
    resp = requests.post(f"{BASE_URL}/tickets", json=new_ticket)
    # Se a criação é permitida deve ser 201, caso já exista título e impeça duplicatas, pode ser 400
    assert resp.status_code in [201, 400]

def test_update_ticket():
    # Tentativa de atualizar um ticket (ID=1 por exemplo)
    update_data = {"Status": 1}
    resp = requests.put(f"{BASE_URL}/tickets/1", json=update_data)
    # Se o ticket existir e for atualizável, 200; se não existe, pode ser 404
    assert resp.status_code in [200, 404]

def test_get_open_tickets():
    resp = requests.get(f"{BASE_URL}/tickets/abertos")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)

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
    resp = requests.get(f"{BASE_URL}/tickets/usuario/1")
    assert resp.status_code in [200, 404]
    # Se 200, espera lista, se 404, significa que nenhum ticket encontrado ou rota não encontrada
    if resp.status_code == 200:
        data = resp.json()
        assert isinstance(data, list)

def test_get_all_users():
    resp = requests.get(f"{BASE_URL}/usuarios")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)

def test_get_user_by_id():
    resp = requests.get(f"{BASE_URL}/usuarios/1")
    # Se existir usuário com ID=1, 200, senão 404
    assert resp.status_code in [200, 404]
    if resp.status_code == 200:
        data = resp.json()
        assert "Login" in data

def test_get_user_by_login():
    # Supondo que possa haver user1
    resp = requests.get(f"{BASE_URL}/usuarios/login/user1")
    assert resp.status_code in [200, 404]
    if resp.status_code == 200:
        data = resp.json()
        assert "Login" in data

def test_create_user():
    new_user = {
        "Login": "user_test_endpoint",
        "Senha": "pass_test"
    }
    resp = requests.post(f"{BASE_URL}/usuarios", json=new_user)
    # Se o login já existe, pode dar 400. Se não, 201.
    assert resp.status_code in [201, 400]
