from pydantic_settings import BaseSettings, SettingsConfigDict,SecretStr
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int
    #========================Vector Database Config=====================
    VECTORDATABASE_BACKEND: str
    VECTORDATABASE_DISTANCE_METHOD: str
    VECTORDATABASE_QDRANT_DB_PATH: Path
    #========================MongoDB Config=====================
    MONGODB_URL: str
    MONGODB_DATABASE : str
    #========================LLM Config=====================
    GENERATION_BACKEND:str
    EMBEDDING_BACKEND:str

    OPENAI_API_KEY:SecretStr=None
    OPENAI_API_URL:str=None
    CHOHERE_API_KEY:SecretStr=None

    GENERATION_MODEL_ID:str=None
    EMBEDDING_MODEL_ID:str=None
    EMBEDDING_MODEL_SIZE:int=None
    #========================Input Config=====================
    INPUT_DEFAULT_MAX_CHARACTERS:int=None
    GENERATION_DEFAULT_MAX_TOKENS:int=None
    GENERATION_DEFAULT_TEMPRATURE:float=None

        
    class Config:
        env_file = ".env"

def get_settings():
    return Settings()