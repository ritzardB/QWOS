"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

Password Reset Status Enumeration
===============================================================================
"""

from enum import StrEnum


class PasswordResetStatus(StrEnum):
    """
    Password reset request lifecycle status.
    """

    PENDING = "PENDING"
    USED = "USED"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
