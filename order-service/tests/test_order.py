from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, Mock

client = TestClient(app)


def test_create_order():
    customer_response = Mock()
    customer_response.status_code = 200
    customer_response.json.return_value = {
        "id": 1,
        "name": "Test Customer",
        "email": "test@example.com",
        "phone": "9999999999"
    }

    menu_response = Mock()
    menu_response.status_code = 200
    menu_response.json.return_value = {
        "id": 1,
        "restaurant_id": 1,
        "name": "Paneer Tikka",
        "category": "Starter",
        "price": 250,
        "available": True
    }

    def mock_get(url, *args, **kwargs):
        if "customer-service" in url or ":8003" in url:
            return customer_response
        elif "menu-service" in url or ":8002" in url:
            return menu_response

        return Mock(status_code=404)

    with patch("app.routes.httpx.get", side_effect=mock_get):
        response = client.post(
            "/orders/",
            json={
                "customer_id": 1,
                "menu_item_id": 1,
                "quantity": 2
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["customer_id"] == 1
    assert data["menu_item_id"] == 1
    assert data["quantity"] == 2
    assert data["total_price"] == 500
    assert data["status"] == "PLACED"


def test_get_orders():
    response = client.get("/orders/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_order():
    response = client.get("/orders/1")

    assert response.status_code in [200, 404]