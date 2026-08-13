"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

Account Status Enumeration

===============================================================================
"""

from enum import StrEnum


class AccountStatus(StrEnum):
    """
    User account status.
    """

    PENDING = "PENDING"

    ACTIVE = "ACTIVE"

    LOCKED = "LOCKED"

    DISABLED = "DISABLED"

    SUSPENDED = "SUSPENDED"

    ARCHIVED = "ARCHIVED"
