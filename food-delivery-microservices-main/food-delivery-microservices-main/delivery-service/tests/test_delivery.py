import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"Delivery Service is running"


def test_create_delivery(client):
    response = client.post(
        "/deliveries",
        json={
            "order_id": 6001,
            "restaurant_id": 101
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert "delivery_id" in data
    assert data["order_id"] == 6001
    assert data["restaurant_id"] == 101
    assert data["delivery_person"] is None
    assert data["status"] == "PENDING"


def test_get_delivery(client):
    response = client.get("/deliveries/9001")

    assert response.status_code == 200

    data = response.get_json()

    assert data["delivery_id"] == 9001
    assert data["order_id"] == 501
    assert data["restaurant_id"] == 101


def test_assign_delivery_person(client):
    response = client.put(
        "/deliveries/9001/assign",
        json={
            "delivery_person": "Test Rider"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["delivery_person"] == "Test Rider"
    assert data["status"] == "ASSIGNED"


def test_update_delivery_status(client):
    response = client.put(
        "/deliveries/9001/status",
        json={
            "status": "PICKED_UP"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "PICKED_UP"


def test_get_delivery_status(client):
    response = client.get("/deliveries/9001/status")

    assert response.status_code == 200

    data = response.get_json()

    assert data["delivery_id"] == 9001
    assert data["status"] == "PICKED_UP"


def test_invalid_delivery_id(client):
    response = client.get("/deliveries/99999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Delivery not found"


def test_invalid_status(client):
    response = client.put(
        "/deliveries/9001/status",
        json={
            "status": "CANCELLED"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Invalid status"


def test_invalid_status_transition(client):
    response = client.put(
        "/deliveries/9001/status",
        json={
            "status": "DELIVERED"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Invalid status transition"


def test_missing_delivery_person(client):
    response = client.put(
        "/deliveries/9001/assign",
        json={}
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "delivery_person is required"