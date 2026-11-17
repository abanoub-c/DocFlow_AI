"""App settings, loaded from environment variables (prefix DOCFLOW_) or .env."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="DOCFLOW_", extra="ignore"
    )

    app_name: str = "DocFlow AI"
    version: str = "0.1.0"
    environment: str = "development"  # development | production
    debug: bool = False
    log_level: str = "INFO"

    # Env var format for lists is JSON: DOCFLOW_CORS_ORIGINS='["https://app.example.com"]'
    cors_origins: list[str] = ["http://localhost:5173"]

    # Upload limits (enforced in documents.service, not in the router)
    max_upload_mb: int = 20
    max_pages: int = 20


@lru_cache
def get_settings() -> Settings:
    return Settings()