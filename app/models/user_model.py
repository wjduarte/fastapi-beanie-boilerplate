from beanie import Document, Indexed
from uuid import UUID, uuid4
from pydantic import EmailStr, Field
from typing import Optional, Annotated
from datetime import datetime, UTC


class User(Document):
    # O Pydantic V2 prefere que o ID seja explicitamente mapeado para o _id do Mongo
    id: UUID = Field(default_factory=uuid4, alias="_id")
    username: Annotated[str, Indexed(unique=True)]
    email: Annotated[EmailStr, Indexed(unique=True)]
    hash_password: str   
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[bool] = None
    
    # Adicionando a data de criação (Boa prática já que foi removido o generation_time)
    # No Python 3.13 e Pydantic V2, usamos datetime.now(UTC)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def __repr__(self) -> str:
        return f'<User {self.email}>' 
    def __str__(self) -> str:
        return self.email

    @classmethod
    async def by_email(cls, email: str) -> Optional["User"]:
        return await cls.find_one(cls.email == email)
    
    class Settings:
        name = "users" # Nome da coleção no MongoDB