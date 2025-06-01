# core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # General
    ENV: str = "development"

    # Model inference
    MODEL_BACKEND: str = "openrouter"
    OPENROUTER_API_KEY: str = ""
    DEFAULT_MODEL: str = "openai/gpt-4o"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # Postgres
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "agentnet"
    POSTGRES_USER: str = "agent"
    POSTGRES_PASSWORD: str = "secret"

    # Logging
    LOG_LEVEL: str = "INFO"

    # GitHub Integration
    GITHUB_APP_ID: str = ""
    GITHUB_APP_PRIVATE_KEY: str = ""
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""
    GITHUB_ACCESS_TOKEN: str = ""
    GITHUB_REPO_OWNER: str = ""
    GITHUB_REPO_NAME: str = ""

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
