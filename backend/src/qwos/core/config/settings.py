"""
===============================================================================
Quantum Workforce OS (QWOS)

File:
    settings.py

Description:
    Centralized application configuration.

===============================================================================
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    APP_NAME: str = "Quantum Workforce OS"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    QWOS_TENANT_ID: str 

    DATABASE_URL: str = (
        "postgresql+psycopg://richardbalabarcon@localhost/qwos_dev"
    )

    # -------------------------------------------------------------------------
    # JWT Authentication
    # -------------------------------------------------------------------------

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    # -------------------------------------------------------------------------
    # Document Storage
    # -------------------------------------------------------------------------

    DOCUMENT_STORAGE_ROOT: str = "./storage/documents"
    DOCUMENT_STORAGE_PROVIDER: str = "local"

    DATABASE_URL: str = (
        "postgresql+psycopg://richardbalabarcon@localhost/qwos_dev"
    )

    # -------------------------------------------------------------------------
    # Document Storage
    # -------------------------------------------------------------------------

    DOCUMENT_STORAGE_ROOT: str = "./storage/documents"
    DOCUMENT_STORAGE_PROVIDER: str = "local"

    # -------------------------------------------------------------------------
    # JWT Authentication
    # -------------------------------------------------------------------------

@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()


settings = get_settings()

