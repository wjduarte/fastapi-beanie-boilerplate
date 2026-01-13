from pydantic import BaseModel, Field, ConfigDict # Adicione ConfigDict
from uuid import UUID
from typing import Optional

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    color: Optional[str] = Field("#3498db")

class CategoryOut(BaseModel):
    # Usamos o alias para mapear _id do banco para id no JSON
    id: UUID = Field(alias="_id", serialization_alias="id")
    name: str
    color: str

    model_config = ConfigDict(
        from_attributes=True, 
        populate_by_name=True  # Permite que 'id' ou '_id' sejam usados
    )