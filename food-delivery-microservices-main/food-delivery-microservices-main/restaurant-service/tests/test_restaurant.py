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
    assert response.data == b"Restaurant Service is running"


def test_get_all_restaurants(client):
    response = client.get("/restaurants")

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) >= 2

    assert data[0]["restaurant_id"] == 101
    assert data[0]["name"] == "Pizza House"


def test_get_specific_restaurant(client):
    response = client.get("/restaurants/101")

    assert response.status_code == 200

    data = response.get_json()

    assert data["restaurant_id"] == 101
    assert data["name"] == "Pizza House"
    assert data["location"] == "Hubli"
    assert data["available"] is True


def test_get_restaurant_menu(client):
    response = client.get("/restaurants/101/menu")

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) == 3

    assert data[0]["item_id"] == 1
    assert data[0]["name"] == "Margherita Pizza"


def test_get_menu_item(client):
    response = client.get("/restaurants/101/menu/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["item_id"] == 1
    assert data["name"] == "Margherita Pizza"
    assert data["price"] == 250
    assert data["available"] is True


def test_get_restaurant_availability(client):
    response = client.get("/restaurants/101/availability")

    assert response.status_code == 200

    data = response.get_json()

    assert data["restaurant_id"] == 101
    assert data["available"] is True


def test_get_menu_item_availability(client):
    response = client.get(
        "/restaurants/101/menu/1/availability"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["restaurant_id"] == 101
    assert data["item_id"] == 1
    assert data["available"] is True


def test_invalid_restaurant_id(client):
    response = client.get("/restaurants/999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Restaurant not found"


def test_invalid_restaurant_menu(client):
    response = client.get("/restaurants/999/menu")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Restaurant not found"


def test_invalid_menu_item(client):
    response = client.get("/restaurants/101/menu/999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Menu item not found"


def test_invalid_restaurant_availability(client):
    response = client.get("/restaurants/999/availability")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Restaurant not found"


def test_invalid_menu_item_availability(client):
    response = client.get(
        "/restaurants/101/menu/999/availability"
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Menu item not found"
