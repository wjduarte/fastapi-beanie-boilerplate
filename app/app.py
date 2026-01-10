from contextlib import asynccontextmanager
from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

# Importamos apenas o roteador principal e as configurações
from app.api.api_v1.router import router as api_router
from app.core.config import settings
from app.models.task_model import Task
from app.models.user_model import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialização do Banco
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    await init_beanie(
        database=db_client.get_default_database(),
        document_models=[User, Task] 
    )
    yield
    db_client.close()

app = FastAPI(
    title="TODOFast API - Boilerplate Profissional com FastAPI e Pydantic V2",
    description="""
    API robusta para gerenciamento de tarefas pessoais.
    
    ## Funcionalidades
    * **Usuários**: Cadastro e gerenciamento de perfil.
    * **Autenticação**: Segurança via JWT (Access & Refresh Tokens).
    * **Tarefas**: CRUD completo com filtros e busca.
    """,
    version="1.0.0",
    contact={
        "name": "Developer Name",
        "url": "https://seulink.com",
    },
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Unindo as rotas através do agregador api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "API TODOFast está online e operando com Pydantic V2!"}
