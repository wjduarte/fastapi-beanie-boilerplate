from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Isso pega o caminho da pasta onde o config.py está, sobe duas vezes (core -> app -> raiz) 
# e aponta para o .env na raiz do projeto.
ROOT = Path(__file__).resolve().parent.parent.parent
ENV_PATH = ROOT / ".env"

class Settings(BaseSettings):
    # Configuração robusta para achar o .env em qualquer lugar
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, # Usa o caminho calculado dinamicamente
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore'
    )

    API_V1_STR: str = '/api/v1'
    PROJECT_NAME: str = 'TODOFast'
    
    JWT_SECRET_KEY: str  
    JWT_REFRESH_SECRET_KEY: str 
    ALGORITHM: str = 'HS256'
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 
    
    BACKEND_CORS_ORIGINS: List[str] = []
    MONGO_CONNECTION_STRING: str 
        
settings = Settings()