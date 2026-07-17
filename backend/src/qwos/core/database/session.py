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

from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from qwos.core.database.engine import engine


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.

    Yields:
        Session: SQLAlchemy database session.
    """
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()