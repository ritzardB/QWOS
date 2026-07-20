"""
===============================================================================
Quantum Workforce OS (QWOS)

Test:
    base.py

===============================================================================
"""

from qwos.core.database.entity_base import BaseEntity


def test_base_entity_is_abstract() -> None:
    """BaseEntity should be abstract."""

    assert BaseEntity.__abstract__ is True
