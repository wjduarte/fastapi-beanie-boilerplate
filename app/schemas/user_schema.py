from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from typing import Optional
from datetime import datetime

class UserAuth(BaseModel): 
    email: EmailStr = Field(..., description="User e-mail")
    username: str = Field(..., min_length=5, max_length=50)
    password: str = Field(..., min_length=5, max_length=20)

class UserDetail(BaseModel):
    # O Pydantic V2 vai ler o '_id' do banco e entregar como 'id' no JSON
    id: UUID = Field(..., validation_alias="_id", serialization_alias="id")
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime

    # MIGRADO PARA V2:
    model_config = ConfigDict(
        from_attributes=True, # Substitui orm_mode
        populate_by_name=True # Permite o uso de 'id' em vez de '_id' na saída
    )
class Token(BaseModel):
    access_token: str
    refresh_token: str  # Adicionado para validar o novo retorno
    token_type: str

    model_config = ConfigDict(from_attributes=True)
    
class TokenData(BaseModel):
    user_id: Optional[UUID] = None