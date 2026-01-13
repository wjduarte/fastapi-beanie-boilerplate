from fastapi import APIRouter
from app.api.auth.jwt import auth_router
from app.api.api_v1.handlers.user import user_router
from app.api.api_v1.handlers.task import task_router
from app.api.api_v1.category_routes import category_router

router = APIRouter()

# centraliza os roteadores
router.include_router(auth_router, prefix='/auth', tags=['auth'])
router.include_router(user_router, prefix='/users', tags=['users'])
router.include_router(task_router, prefix='/tasks', tags=['tasks']) 
router.include_router(category_router, prefix='/categories', tags=['categories'])

# Adicionar mais roteadores conforme necessário