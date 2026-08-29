"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Forbidden Exception
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.exceptions.application_exception import (
    ApplicationException,
)


class ForbiddenException(ApplicationException):
    """
    Raised when the current user is authenticated but not authorized
    to perform an operation.
    """

    def __init__(
        self,
        *,
        message: str = "You are not authorized to perform this operation.",
    ) -> None:
        super().__init__(message)
