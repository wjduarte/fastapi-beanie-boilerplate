import pytest
from httpx import AsyncClient

# Teste 1: Criar Usuário com sucesso
async def test_create_user_success(client: AsyncClient):
    response = await client.post(
        "/api/v1/users/create",
        json={
            "username": "new_dev",
            "email": "dev@test.com",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    assert response.json()["email"] == "dev@test.com"

# Teste 2: Tentar criar usuário com e-mail duplicado
async def test_create_user_duplicate_email(client: AsyncClient):
    payload = {
        "username": "primeiro",
        "email": "duplicate@test.com",
        "password": "password123"
    }
    # Criamos o primeiro
    await client.post("/api/v1/users/create", json=payload)
    
    # Tentamos criar o segundo com o mesmo e-mail
    response = await client.post("/api/v1/users/create", json=payload)
    
    assert response.status_code == 400 
    assert "email" in response.json()["detail"].lower()


async def test_login_success(client: AsyncClient):
    user_data = {
        "username": "login_user",
        "email": "login@test.com",
        "password": "password123"
    }
    # Criamos o usuário para ele existir no banco deste teste
    await client.post("/api/v1/users/create", json=user_data)
    
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    
    response = await client.post("/api/v1/auth/login", data=login_data)
    
    assert response.status_code == 200
    assert "access_token" in response.json()