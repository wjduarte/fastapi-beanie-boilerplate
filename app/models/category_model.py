from beanie import Document
from uuid import UUID, uuid4
from pydantic import Field
from typing import Optional

class Category(Document):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    name: str
    color: str = Field(default="#3498db") # Cor padrão (azul)
    owner: UUID # Referência ao usuário dono da categoria

    class Settings:
        name = "categories"