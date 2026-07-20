from functools import lru_cache

from pydantic import Field 
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(env_file="../../.env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")
    
    APP_NAME: str = "AI Atlas Platform"
    ENVIRONMENT : str = "development"
    DEBUG: bool = True
    
    API_V1_PREFIX: str = "/api/v1"
    
    POSTGRES_DB : str = Field(default="ai_atlas")
    POSTGRES_USER : str = Field(default="postgres")
    POSTGRES_PASSWORD : str = Field(default="postgres")
    POSTGRES_HOST : str = Field(default="localhost")
    POSTGRES_PORT : int = Field(default=5432)
    
    DATABASE_URL : str = "postgresql+psycopg://postgres:postgres@localhost:5432/ai_atlas"
    
    REDIS_URL : str = "redis://localhost:6379"
    
    LLM_PROVIDER: str = ""
    LLM_MODEL: str = ""
    LLM_API_KEY: str = ""

    EMBEDDING_PROVIDER: str = ""
    EMBEDDING_MODEL: str = ""
    
    GNEWS_API_KEY : str = ""
    NEWS_SCHEDULER_ENABLED: bool = False
    NEWS_REFRESH_INTERVAL_MINUTES: int = 360
    
    JWT_SECRET : str = "change-me"
    JWT_ALGORITHM : str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 60
    
@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
