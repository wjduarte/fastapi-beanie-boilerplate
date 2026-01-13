from uuid import UUID
from typing import Optional

# AJUSTES DE IMPORT (Padrão absoluto para evitar 'ModuleNotFoundError')
from app.models.user_model import User
from app.schemas.user_schema import UserAuth 
from app.core.security import hash_password, verify_password

class UserService:
    @staticmethod
    async def create_user(data: UserAuth) -> User:
        # Verifica se o usuário já existe pelo e-mail
        user_exists = await User.find_one(User.email == data.email)
        if user_exists:            
            raise ValueError("Usuário com este e-mail já existe")
        
        user = User(
            username=data.username,
            email=data.email,
            hash_password=hash_password(data.password)
        )
        await user.insert()
        return user
    
    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[User]:
        user = await User.find_one(User.email == email)
        
        if user and verify_password(password, user.hash_password):
            return user
        return None
    
    @staticmethod
    async def get_user_by_id(user_id: UUID) -> Optional[User]:
        # Como o ID é UUID no model, pode ser usado diretamente o UUID aqui.
        return await User.get(user_id)