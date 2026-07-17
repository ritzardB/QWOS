"""
===============================================================================
Quantum Workforce OS (QWOS)

Test:
    settings.py

===============================================================================
"""

from qwos.core.config.settings import settings


def test_application_name():
    """Application name should be configured."""

    assert settings.APP_NAME == "Quantum Workforce OS"


def test_environment():
    """Environment should default to development."""

    assert settings.ENVIRONMENT == "development"


def test_database_url():
    """Database URL should exist."""

    assert settings.DATABASE_URL is not None
    assert settings.DATABASE_URL != ""