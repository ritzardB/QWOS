"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Account Locked Exception
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.exceptions.business_rule_exception import (
    BusinessRuleException,
)


class AccountLockedException(BusinessRuleException):
    """
    Raised when a user account is locked.
    """

    def __init__(self) -> None:
        super().__init__(
            "The account is locked."
        )