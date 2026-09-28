from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_restaurant():
    response = client.post(
        "/restaurants/",
        json={
            "name": "Test Restaurant",
            "address": "Mumbai",
            "phone": "9999999999"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test Restaurant"
    assert data["address"] == "Mumbai"
    assert data["phone"] == "9999999999"


def test_get_restaurants():
    response = client.get("/restaurants/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_restaurant():
    response = client.get("/restaurants/1")

    assert response.status_code in [200, 404]