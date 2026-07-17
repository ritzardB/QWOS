"""
===============================================================================
Quantum Workforce OS (QWOS)

Test:
    base.py

===============================================================================
"""

from qwos.core.database.base import BaseEntity


def test_base_entity_is_abstract():
    """BaseEntity should be abstract."""

    assert BaseEntity.__abstract__ is True