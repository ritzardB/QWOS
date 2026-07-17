"""
===============================================================================
Quantum Workforce OS (QWOS)

Test:
    engine.py

===============================================================================
"""

from sqlalchemy.engine import Engine

from qwos.core.database.engine import engine


def test_engine_created():
    """Engine should be created."""

    assert isinstance(engine, Engine)