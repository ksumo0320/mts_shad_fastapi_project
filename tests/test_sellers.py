import pytest
from fastapi.testclient import TestClient
from configurations.database import global_init
from main import app

client = TestClient(app)

global_init()

@pytest.mark.asyncio
async def test_create_seller():
    seller_data = {
        "first_name": "John",
        "last_name": "Doe",
        "e_mail": "john.doe@example.com",
        "password": "password123"
    }
    response = client.post("/api/v1/sellers/", json=seller_data)
    assert response.status_code == 201
    assert response.json()["first_name"] == seller_data["first_name"]
    assert response.json()["last_name"] == seller_data["last_name"]
    assert response.json()["e_mail"] == seller_data["e_mail"]

@pytest.mark.asyncio
async def test_get_seller():
    response = client.get("/api/v1/sellers/1")
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_all_sellers():
    response = client.get("/api/v1/sellers/")
    assert response.status_code == 200
    assert len(response.json()["sellers"]) > 0

@pytest.mark.asyncio
async def test_delete_seller():
    response = client.delete("/api/v1/sellers/1")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_seller():
    seller_data = {
        "first_name": "Updated",
        "last_name": "Seller",
        "e_mail": "updated.seller@example.com",
        "password": "newpassword123"
    }
    response = client.put("/api/v1/sellers/1", json=seller_data)
    assert response.status_code == 200
    assert response.json() == 1
