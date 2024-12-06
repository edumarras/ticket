# test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app
from httpx import AsyncClient
import pytest_asyncio

client = TestClient(app)

@pytest.mark.asyncio
async def test_get_open_tickets():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.get("/tickets/open")
        assert response.status_code == 200
        tickets = response.json()
        assert isinstance(tickets, list)
        for ticket in tickets:
            assert "Titulo" in ticket
            assert "Prioridade" in ticket
            assert ticket["Status"] == 0

@pytest.mark.asyncio
async def test_create_ticket():
    ticket_data = {
        "Titulo": "Test Ticket",
        "Descricao": "Test Description",
        "Prioridade": 1
    }
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.post("/tickets", json=ticket_data)
        assert response.status_code == 201
        assert "message" in response.json()

@pytest.mark.asyncio
async def test_register_user():
    user_data = {
        "Login": "testuser",
        "Senha": "testpass"
    }
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.post("/register", json=user_data)
        assert response.status_code in [201, 400]  # 400 if user exists

@pytest.mark.asyncio
async def test_login():
    user_data = {
        "Login": "testuser",
        "Senha": "testpass"
    }
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.post("/login", json=user_data)
        if response.status_code == 200:
            user = response.json()
            assert "ID" in user
            assert "Login" in user
            assert "ADM" in user
