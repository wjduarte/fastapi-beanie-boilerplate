from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(
        ..., 
        min_length=3, 
        max_length=100,
        description="O título curto e claro da tarefa",
        examples=["Comprar leite e pão"]
    )
    description: str = Field(
        ...,
        max_length=500,
        description="Descrição detalhada do que precisa ser feito",
        examples=["Ir ao supermercado x e garantir que o leite seja desnatado." ]
    )

class TaskOut(BaseModel):
    id: UUID = Field(..., validation_alias="_id", serialization_alias="id")
    title: str
    description: str
    status: bool
    created_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True, 
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Exemplo de Tarefa",
                "description": "Esta é uma tarefa de exemplo retornada pela API",
                "status": False,
                "created_at": "2026-01-09T10:00:00Z"
            }
        }
    )
    
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[bool] = None