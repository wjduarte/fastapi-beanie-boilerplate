from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user_model import User 
from app.schemas.user_schema import UserAuth, UserDetail 
from app.core.security import hash_password 
from app.api.api_v1.dependencies.user_deps import get_current_user 

user_router = APIRouter()

@user_router.post("/create", response_model=UserDetail, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserAuth):
    # 1. Verifica se usuário existe
    user_exists = await User.by_email(data.email)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="The user with this email already exists."
        )
    
    # 2. Cria o novo usuário (Pydantic V2 cuidará da conversão de tipos)
    user = User(
        username=data.username,
        email=data.email,
        hash_password=hash_password(data.password) 
    )

    await user.insert()
    return user

# NOVA ROTA: Essencial para o gerenciamento do usuário
@user_router.get("/me", response_model=UserDetail)
async def get_me(user: User = Depends(get_current_user)):
    """
    Retorna o usuário atual autenticado pelo Token.
    O Pydantic V2 transforma o _id em id automaticamente aqui.
    """
    return user

# Rota adicional para listar todos os usuários (apenas para fins de teste)
# @user_router.get("/", response_model=list[UserDetail])
# async def list_users():
#     users = await User.find_all().to_list()
#     return users