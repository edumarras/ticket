import pytest
from fastapi.testclient import TestClient
from mid.main import app

client = TestClient(app)

def test_get_open_tickets():
    print("\n[TEST] test_get_open_tickets")
    response = client.get("/tickets/open")
    print(f"Status code: {response.status_code}")
    # Ajustar se necessário: se não houver tickets, deve retornar 200 com lista vazia.
    # Aqui assumimos que retornará 200 com lista (mesmo vazia).
    assert response.status_code == 200
    print("Get open tickets test passed!\n")

def test_create_user():
    print("\n[TEST] test_create_user (mid)")
    user_data = {"Login": "testuser_mid", "Senha": "testpass_mid"}
    response = client.post("/register", json=user_data)
    print(f"Status code: {response.status_code}")
    print(f"Body: {response.text}")
    # Esperamos que, ao criar um usuário com sucesso, o mid retorne 201
    assert response.status_code == 201, "Esperava 201 ao criar usuário"
    print("User creation (mid) test passed!\n")
