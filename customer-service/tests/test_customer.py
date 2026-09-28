from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_customer():
    response = client.post(
        "/customers/",
        json={
            "name": "Test Customer",
            "email": "jenkins-test-customer-001@example.com",
            "phone": "9999999999"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test Customer"
    assert data["email"] == "jenkins-test-customer-001@example.com"
    assert data["phone"] == "9999999999"


def test_get_customers():
    response = client.get("/customers/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_customer():
    response = client.get("/customers/1")

    assert response.status_code in [200, 404]