from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from jose import jwt
from pydantic import ValidationError

from app.services.user_service import UserService
from app.schemas.user_schema import Token, UserDetail  
from app.core.security import create_access_token, create_refresh_token
from app.api.api_v1.dependencies.user_deps import get_current_user
from app.models.user_model import User
from app.core.config import settings

auth_router = APIRouter()

@auth_router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserService.authenticate_user(
        email=form_data.username, 
        password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid email or password"
        )
    
    return {
        "access_token": create_access_token(data={"sub": str(user.id)}),
        "refresh_token": create_refresh_token(data={"sub": str(user.id)}),
        "token_type": "bearer",
    }
    
@auth_router.post('/refresh', response_model=Token)
async def refresh_token(refresh_token: str = Body(..., embed=True)):
    """
    Recebe um refresh_token e gera um novo access_token válido.
    O 'embed=True' espera um JSON como {"refresh_token": "..."}
    """
    try:
        payload = jwt.decode(
            refresh_token, 
            settings.JWT_REFRESH_SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
            
        user = await User.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
            
        return {
            "access_token": create_access_token(data={"sub": str(user.id)}),
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
        
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não foi possível validar as credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )

@auth_router.post('/test-token', response_model=UserDetail)
async def test_token(user: User = Depends(get_current_user)):
    return user