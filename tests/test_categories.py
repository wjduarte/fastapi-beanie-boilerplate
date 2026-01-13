import pytest
from httpx import AsyncClient
import uuid

@pytest.fixture
async def auth_token(client: AsyncClient):
    unique_id = uuid.uuid4().hex
    user_data = {"username": f"cat_user_{unique_id}", "email": f"cat_{unique_id}@test.com", "password": "password123"}
    await client.post("/api/v1/users/create", json=user_data)
    login_res = await client.post("/api/v1/auth/login", data={"username": user_data["email"], "password": "password123"})
    return login_res.json()["access_token"]

async def test_create_category(client: AsyncClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {"name": "Trabalho", "color": "#FF5733"}
    
    response = await client.post("/api/v1/categories/create", json=payload, headers=headers)
    
    assert response.status_code == 201
    assert response.json()["name"] == "Trabalho"
    assert "id" in response.json() or "_id" in response.json()