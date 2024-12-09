import requests

def test_mid_to_back_integration():
    print("\n[TEST] test_mid_to_back_integration")

    # Criar um usuário direto no mid para ter alguém para atribuir tickets se necessário
    user_data = {"Login": "midtobackuser", "Senha": "testpass"}
    print("Criando usuário via mid (POST /register)")
    r_user = requests.post("http://localhost:8000/register", json=user_data)
    print(f"Status code (user creation mid): {r_user.status_code}")
    assert r_user.status_code == 201, "Esperava 201 ao criar usuário no mid"

    # Criar um ticket via mid
    ticket_data = {
        "Titulo": "Ticket Integração",
        "Descricao": "Teste de integração mid->back",
        "Prioridade": 1
    }
    print("Criando ticket via mid (POST /tickets)")
    r_ticket = requests.post("http://localhost:8000/tickets", json=ticket_data)
    print(f"Status code (ticket creation): {r_ticket.status_code}")
    assert r_ticket.status_code == 201, f"Esperava 201 ao criar ticket no mid, obtido {r_ticket.status_code}"

    # Buscar todos os tickets via mid
    print("Buscando todos os tickets via mid (GET /tickets)")
    r_all = requests.get("http://localhost:8000/tickets")
    print(f"Status code (get all tickets): {r_all.status_code}")
    print(f"Response JSON: {r_all.json()}")
    assert r_all.status_code == 200
    tickets = r_all.json()
    assert any(t['Titulo'] == "Ticket Integração" for t in tickets), "Não encontrou o ticket criado via mid->back"

    print("Mid to back integration test passed!\n")
