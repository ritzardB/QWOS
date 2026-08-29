"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Configuration

File:
    settings.py

Description:
    Centralized application configuration.

Responsibilities:
    - Application metadata
    - Environment configuration
    - Multi-tenant configuration
    - Database configuration
    - JWT authentication configuration
    - Document storage configuration

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    and the local .env file.
    """

    # =========================================================================
    # Application
    # =========================================================================

    APP_NAME: str = "Quantum Workforce OS"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"

    # =========================================================================
    # Multi-Tenant Configuration
    # =========================================================================

    QWOS_TENANT_ID: str

    # =========================================================================
    # Database
    # =========================================================================

    DATABASE_URL: str = (
        "postgresql+psycopg://richardbalabarcon@localhost/qwos_dev"
    )

    # =========================================================================
    # JWT Authentication
    # =========================================================================

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # =========================================================================
    # Document Storage
    # =========================================================================

    DOCUMENT_STORAGE_ROOT: str = "./storage/documents"
    DOCUMENT_STORAGE_PROVIDER: str = "local"

    # =========================================================================
    # Pydantic Settings Configuration
    # =========================================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return the cached application settings.
    """

    return Settings()


settings = get_settings()