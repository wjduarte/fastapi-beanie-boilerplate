import pytest
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import asyncio

from app.app import app
from app.models.category_model import Category
from app.models.user_model import User
from app.models.task_model import Task

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="function", autouse=True) # Limpa o banco de dados antes de CADA teste
async def initialize_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    
    # Inicializa Beanie
    await init_beanie(
        database=client.todofast_test,
        document_models=[User, Task, Category] 
    )
    
    yield
    
    # Limpa o banco após CADA teste (evita conflitos de e-mail duplicado)
    await client.drop_database("todofast_test")
    client.close()

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac