"""
===============================================================================
Quantum Workforce OS (QWOS)

Test:
    session.py

===============================================================================
"""

from sqlalchemy.orm import Session

from qwos.core.database.session import SessionLocal


def test_session_creation() -> None:
    """Session should be created successfully."""

    db = SessionLocal()

    try:
        assert isinstance(db, Session)
    finally:
        db.close()
