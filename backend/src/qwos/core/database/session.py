"""
===============================================================================
Quantum Workforce OS (QWOS)

File:
    session.py

Description:
    SQLAlchemy session management.

Author:
    Richard Balabarcon

===============================================================================
"""

from collections.abc import Generator

from sqlalchemy.orm import Session, sessionmaker

from qwos.core.database.engine import engine

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a SQLAlchemy session.
    """
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
