from beanie import Document, Indexed
from uuid import UUID, uuid4
from pydantic import Field
from datetime import datetime, UTC

class Task(Document):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    title: str
    description: str
    status: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    
    # RELAÇÃO: Cada tarefa pertence a um usuário
    owner: UUID 

    class Settings:
        name = "tasks"
        
        