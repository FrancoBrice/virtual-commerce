import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app 


client = TestClient(app)

@pytest.fixture
def mock_traeloya_success():
    return {
        "estimateId": "abc123",
        "deliveryOffers": {
            "deliveryOfferId": "xyz789",
            "confirmationTimeLimit": "2025-01-01T00:00:00Z",
            "deliveryMode": "standard",
            "pricing": {"total": 5990}
        },
        "route": {"distance": 10},
        "waypoints": [
            {"type": "PICK_UP", "latitude": -33.45, "longitude": -70.65},
            {"type": "DROP_OFF", "latitude": -33.46, "longitude": -70.66}
        ]
    }

@pytest.fixture
def mock_traeloya_no_rate():
    return {"error": "No hay tarifas disponibles para el envío solicitado."}

@pytest.fixture
def mock_uder_success():
    return {"fee": 4990, "tracking_url": "https://tracking.example.com"}

@patch("services.shipping_service.requests.post")
def test_get_shipping_rate_success(mock_post, mock_traeloya_success):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = mock_traeloya_success

    response = client.post("/api/cart", json={
        "products": [
            {"productId": 22, "price": 50, "quantity": 3},
            {"productId": 2, "price": 15, "quantity": 12}
        ],
        "customer_data": {
            "name": "Juan Pérez",
            "shipping_street": "Calle Falsa 123",
            "commune": "Vita",
            "phone": "+56900000000"
        }
    })

    assert response.status_code == 200
    assert response.json()["courier"] == "TraeloYa"
    assert response.json()["price"] == 5990

@patch("services.shipping_service.requests.post")
def test_get_shipping_rate_no_rate(mock_post, mock_traeloya_no_rate):
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = mock_traeloya_no_rate

    response = client.post("/api/cart", json={
        "products": [
            {"productId": 22, "price": 50, "quantity": 3}
        ],
        "customer_data": {
            "name": "Juan Pérez",
            "shipping_street": "Calle Falsa 123",
            "commune": "Vita",
            "phone": "+56900000000"
        }
    })

    assert response.status_code == 400
    assert "No available shipping rates from any courier." in response.json()["detail"]

