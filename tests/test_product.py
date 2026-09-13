from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# def test_root():
#     response = client.get("/")

#     assert response.status_code == 200
#     assert response.json()["message"] == "AI Product Intelligence API is running"
    
def test_create_product(client):
    response = client.post(
        "/products/",
        json={
            "name": "iPhone 15",
            "description": "Smartphone Apple dengan kamera berkualitas tinggi",
            "category": "Smartphone",
            "brand": "Apple",
            "price": 15000000,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "iPhone 15"
    assert data["brand"] == "Apple"
    assert data["price"] == 15000000
    assert "id" in data


def test_get_products(client):
    client.post(
        "/products/",
        json={
            "name": "iPhone 15",
            "description": "Smartphone Apple",
            "category": "Smartphone",
            "brand": "Apple",
            "price": 15000000,
        },
    )

    response = client.get("/products/")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "iPhone 15"