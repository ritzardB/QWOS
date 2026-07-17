"""
===============================================================================
Quantum Workforce OS (QWOS)

File:
    enum.py

Description:
    Reusable SQLAlchemy Enum type helpers.

===============================================================================
"""

from enum import Enum

from sqlalchemy import Enum as SQLEnum


def enum_column(enum_type: type[Enum]) -> SQLEnum:
    """
    Create a PostgreSQL-compatible SQLAlchemy Enum.

    Args:
        enum_type:
            Python enumeration class.

    Returns:
        Configured SQLAlchemy Enum.
    """
    return SQLEnum(
        enum_type,
        native_enum=True,
        validate_strings=True,
    )
