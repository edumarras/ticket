import pytest
import requests
import time

MIDDLEWARE_URL = "http://localhost:8000"

def test_get_open_tickets():
    # Endpoint: GET /tickets/open
    # Espera retornar 200 e uma lista de tickets (possivelmente vazia)
    resp = requests.get(f"{MIDDLEWARE_URL}/tickets/open")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)

def test_register_user():
    # Endpoint: POST /register
    # Cria um usuário sem verificação prévia.
    new_user = {
        "Login": "teste_user_middleware",
        "Senha": "teste_pass"
    }
    resp = requests.post(f"{MIDDLEWARE_URL}/register", json=new_user)
    # Se o backend permitir criação, retorna 201
    # Se já existir, pode ser 400
    assert resp.status_code in [201,400]

def test_login():
    # Endpoint: POST /login
    # Autentica um usuário existente (ajuste login/senha conforme seu script.sql ou criação prévia)
    login_data = {
        "Login": "user1",  # Ajuste conforme seu backend
        "Senha": "pass1"   # Ajuste conforme sua config
    }
    resp = requests.post(f"{MIDDLEWARE_URL}/login", json=login_data)
    # Possíveis cenários:
    # 200 se autenticou
    # 401 se senha incorreta
    # 404 se usuário não encontrado
    assert resp.status_code in [200,401,404]

def test_assign_ticket():
    # Endpoint: PUT /tickets/{ticket_id}/assign/{user_id}
    # Tenta atribuir o ticket ID=1 a user ID=1
    resp = requests.put(f"{MIDDLEWARE_URL}/tickets/1/assign/1")
    # Possíveis cenários:
    # 200 se atualizado com sucesso
    # 404 se ticket não existe
    assert resp.status_code in [200,404]

def test_get_tickets_by_user():
    # Endpoint: GET /tickets/user/{user_id}
    # Tenta obter tickets do usuário ID=1
    resp = requests.get(f"{MIDDLEWARE_URL}/tickets/user/1")
    # Se existir, 200 com lista
    # Se não existir tickets ou user inexistente, talvez 200 com lista vazia
    # ou 404 dependendo da lógica do backend
    assert resp.status_code in [200,404]
    if resp.status_code == 200:
        data = resp.json()
        assert isinstance(data, list)

def test_get_all_tickets():
    # Endpoint: GET /tickets
    # Retorna todos os tickets, independente do status
    resp = requests.get(f"{MIDDLEWARE_URL}/tickets")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)

def test_create_ticket():
    # Endpoint: POST /tickets
    # Cria um novo ticket
    new_ticket = {
        "Titulo": "Ticket do Middleware",
        "Descricao": "Testando criação de ticket via middleware",
        "Prioridade": 2
    }
    resp = requests.post(f"{MIDDLEWARE_URL}/tickets", json=new_ticket)
    # 201 se criado com sucesso, 400 se erro
    assert resp.status_code in [201,400]

def test_complete_ticket():
    # Endpoint: PUT /tickets/complete/{ticket_id}
    # Finaliza o ticket ID=1
    resp = requests.put(f"{MIDDLEWARE_URL}/tickets/complete/1")
    # 200 se finalizado com sucesso
    # 404 se ticket inexistente
    assert resp.status_code in [200,404]
