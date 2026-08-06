"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Business Rule Exception

Description:
    Raised when a business rule is violated.
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.exceptions.application_exception import (
    ApplicationException,
)


class BusinessRuleException(ApplicationException):
    """
    Raised when a business rule is violated.
    """

    pass