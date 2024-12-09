import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_page_loads(client):
    print("\n[TEST] test_login_page_loads")
    response = client.get('/')
    print(f"Status code: {response.status_code}")
    assert response.status_code == 200
    assert b'Login' in response.data
    print("Login page loads test passed!\n")
