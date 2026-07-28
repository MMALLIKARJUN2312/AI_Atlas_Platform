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

    # Comma-separated list of allowed browser origins, e.g.
    # "https://ai-atlas.vercel.app,https://staging.ai-atlas.vercel.app".
    # Defaults to "*" for zero-friction local development.
    ALLOWED_ORIGINS: str = "*"

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

    # Ceiling on the agent's reason-act loop. Each iteration is one LLM call,
    # so this bounds both latency and cost per question.
    AGENT_MAX_ITERATIONS: int = 5

    # Minimum verification confidence for a discovered company to be written
    # to the directory with no human review. Below this it becomes a pending
    # candidate for an admin to approve or reject.
    DISCOVERY_AUTO_APPROVE_THRESHOLD: float = 0.90
    # Below this a candidate is not even worth a reviewer's attention.
    DISCOVERY_MIN_REVIEW_THRESHOLD: float = 0.60
    # Independent-verification web searches cost a separate, stricter Gemini
    # grounding quota, so this bounds how many candidates from one discovery
    # call get a corroboration search. Candidates beyond the cap fall back to
    # human review instead of failing the request.
    DISCOVERY_MAX_VERIFICATIONS_PER_CALL: int = 5
    
    JWT_SECRET : str = "change-me"
    JWT_ALGORITHM : str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 60

    ADMIN_EMAIL : str = "admin@aiatlas.local"
    ADMIN_PASSWORD : str = "change-me"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
