import pytest
from httpx import AsyncClient
import uuid

@pytest.fixture
async def auth_token(client: AsyncClient):
    """Cria um utilizador e retorna o token de acesso."""
    unique_id = uuid.uuid4().hex
    user_data = {
        "username": f"user_{unique_id}",
        "email": f"owner_{unique_id}@test.com",
        "password": "password123"
    }
    await client.post("/api/v1/users/create", json=user_data)
    
    login_res = await client.post("/api/v1/auth/login", data={
        "username": user_data["email"],
        "password": "password123"
    })
    return login_res.json()["access_token"]

# 1. Testar Criação
async def test_create_task(client: AsyncClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {"title": "Tarefa de Teste", "description": "Validando CRUD", "status": False}
    
    response = await client.post("/api/v1/tasks/create", json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json()["title"] == payload["title"]

# 2. Testar Listagem de Tarefas
async def test_get_tasks(client: AsyncClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Garantir que há pelo menos uma tarefa criada
    payload = {
        "title": "Task 1",
        "description": "Descrição obrigatória",
        "status": False
    }
    await client.post("/api/v1/tasks/create", json=payload, headers=headers)

    response = await client.get("/api/v1/tasks/", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    # Assegura que há pelo menos uma tarefa na lista
    assert len(data) >= 1

async def test_delete_task_security(client: AsyncClient, auth_token: str):
    headers_owner = {"Authorization": f"Bearer {auth_token}"}
    
    # 1. Dono cria tarefa
    res_create = await client.post("/api/v1/tasks/create", 
                                   json={"title": "Privada", "description": "Desc"}, 
                                   headers=headers_owner)
    task_id = res_create.json().get("id") or res_create.json().get("_id")

    # 2. Invasor (Usando e-mail único e garantindo login correto)
    inv_email = f"inv_{uuid.uuid4().hex}@test.com"
    user_inv = {"username": "invasor_name", "email": inv_email, "password": "password123"}
    
    await client.post("/api/v1/users/create", json=user_inv)
    
    # IMPORTANTE: No login, o 'username' costuma ser o e-mail se você usa OAuth2
    login_inv = await client.post("/api/v1/auth/login", data={
        "username": inv_email, 
        "password": "password123"
    })
    
    if login_inv.status_code != 200:
        pytest.fail(f"Login do invasor falhou: {login_inv.json()}")
        
    token_inv = login_inv.json()["access_token"]
    headers_inv = {"Authorization": f"Bearer {token_inv}"}

    # 3. Tenta apagar
    res_del = await client.delete(f"/api/v1/tasks/{task_id}", headers=headers_inv)
    assert res_del.status_code in [403, 404]
    
# 4. Testar Atualização e Segurança do Update
async def test_update_task_security(client: AsyncClient, auth_token: str):
    headers_owner = {"Authorization": f"Bearer {auth_token}"}
    
    # 1. Dono cria uma tarefa
    res_create = await client.post("/api/v1/tasks/create", 
                                   json={"title": "Tarefa Original", "description": "Antes do update"}, 
                                   headers=headers_owner)
    task_id = res_create.json().get("id") or res_create.json().get("_id")

    # 2. Invasor com senha mais robusta para evitar erro de validação (422)
    inv_email = f"inv_upd_{uuid.uuid4().hex}@test.com"
    inv_pass = "password123" 
    
    await client.post("/api/v1/users/create", 
                      json={"username": "invasor_upd", "email": inv_email, "password": inv_pass})
    
    login_inv = await client.post("/api/v1/auth/login", data={"username": inv_email, "password": inv_pass})
    
    # Verifica se o login foi bem-sucedido
    if login_inv.status_code != 200:
        pytest.fail(f"Login do invasor falhou com status {login_inv.status_code}: {login_inv.json()}")
        
    token_inv = login_inv.json()["access_token"]
    headers_inv = {"Authorization": f"Bearer {token_inv}"}

    # 3. Invasor tenta editar (404 ou 403)
    res_upd_inv = await client.put(f"/api/v1/tasks/{task_id}", 
                                   json={"title": "Hackeado"}, 
                                   headers=headers_inv)
    assert res_upd_inv.status_code in [403, 404]

    # 4. Dono atualiza com sucesso
    res_upd_owner = await client.put(f"/api/v1/tasks/{task_id}", 
                                     json={"status": True, "title": "Tarefa Concluída"}, 
                                     headers=headers_owner)
    assert res_upd_owner.status_code == 200
    assert res_upd_owner.json()["status"] is True
    assert res_upd_owner.json()["title"] == "Tarefa Concluída"
    
async def test_create_task_with_category(client: AsyncClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}

    # 1. Primeiro, criamos uma categoria para vincular à tarefa
    cat_payload = {"name": "Projeto Comercial", "color": "#8e44ad"}
    cat_res = await client.post("/api/v1/categories/create", json=cat_payload, headers=headers)
    assert cat_res.status_code == 201
    category_id = cat_res.json()["id"]

    # 2. Agora, criamos a tarefa enviando o ID da categoria criada
    task_payload = {
        "title": "Configurar Banco de Dados",
        "description": "Instalar e configurar o MongoDB para produção.",
        "category": category_id # Vínculo com a categoria criada
    }
    
    task_res = await client.post("/api/v1/tasks/create", json=task_payload, headers=headers)
    
    # 3. Verificações (Asserções)
    assert task_res.status_code == 201
    task_data = task_res.json()
    assert task_data["title"] == "Configurar Banco de Dados"
    assert task_data["category"] == category_id # Garante que o vínculo foi salvo