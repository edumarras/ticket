import os
import tempfile
import pytest
import sqlite3
from backend.api import app

@pytest.fixture
def test_client():
    # Cria um DB temporário para testes
    db_fd, db_path = tempfile.mkstemp()
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE IF NOT EXISTS Ticket (ID INTEGER PRIMARY KEY, Titulo TEXT, Descricao TEXT, Prioridade INT, Status INT, ID_pessoa INT);")
    # Tabela de Pessoas usada na auth
    conn.execute("CREATE TABLE IF NOT EXISTS Pessoas (ID INTEGER PRIMARY KEY, Login TEXT UNIQUE, Senha TEXT, ADM INT);")
    conn.commit()
    conn.close()

    def test_connect_db():
        c = sqlite3.connect(db_path)
        c.row_factory = sqlite3.Row
        return c

    # Monkeypatch se necessário
    original_connect_db = getattr(app, 'connect_db', None)
    setattr(app, 'connect_db', test_connect_db)

    with app.test_client() as client:
        yield client

    if original_connect_db:
        setattr(app, 'connect_db', original_connect_db)

    os.close(db_fd)
    os.remove(db_path)

def test_get_all_tickets_empty(test_client):
    print("\n[TEST] test_get_all_tickets_empty (backend)")
    response = test_client.get('/tickets')
    print(f"Status code: {response.status_code}")
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 200
    assert response.get_json() == []
    print("Get all tickets empty test passed!\n")

def test_create_user_backend(test_client):
    print("\n[TEST] test_create_user_backend")
    user_data = {"Login": "backenduser", "Senha": "backendpass"}
    # Criando usuário direto no backend
    response = test_client.post('/usuarios', json=user_data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.get_json()}")
    assert response.status_code == 201
    print("User creation backend test passed!\n")
