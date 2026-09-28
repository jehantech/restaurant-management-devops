from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, Mock

client = TestClient(app)


def test_create_menu_item():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "id": 1,
            "name": "Spice Garden",
            "address": "Andheri, Mumbai",
            "phone": "9876543210"
        }
    ]

    with patch("app.routes.httpx.get", return_value=mock_response):
        response = client.post(
            "/",
            json={
                "restaurant_id": 1,
                "name": "Paneer Tikka Test",
                "category": "Starter",
                "price": 250,
                "available": True
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Paneer Tikka Test"
    assert data["category"] == "Starter"
    assert data["price"] == 250
    assert data["restaurant_id"] == 1


def test_get_menu_items():
    response = client.get("/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_menu_item():
    response = client.get("/1")

    assert response.status_code in [200, 404]