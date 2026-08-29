"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Invalid Credentials Exception
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.exceptions.business_rule_exception import (
    BusinessRuleException,
)


class InvalidCredentialsException(BusinessRuleException):
    """
    Raised when authentication credentials are invalid.
    """

    def __init__(self) -> None:
        super().__init__("Invalid username or password.")
