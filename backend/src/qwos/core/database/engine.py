"""
===============================================================================
Quantum Workforce OS (QWOS)

File:
    engine.py

Description:
    SQLAlchemy database engine configuration.

Author:
    Richard Balabarcon

===============================================================================
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from qwos.core.config.settings import settings


def create_database_engine() -> Engine:
    """
    Create and configure the SQLAlchemy engine.

    Returns:
        Engine: Configured SQLAlchemy engine instance.
    """
    return create_engine(
        settings.DATABASE_URL,
        echo=settings.ENVIRONMENT.lower() == "development",
        future=True,
        pool_pre_ping=True,
    )


engine = create_database_engine()