"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Resource Not Found Exception
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.exceptions.application_exception import (
    ApplicationException,
)


class ResourceNotFoundException(ApplicationException):
    """
    Raised when a requested resource cannot be found.
    """

    def __init__(
        self,
        *,
        resource: str,
        identifier: str,
    ) -> None:
        super().__init__(f"{resource} '{identifier}' was not found.")

        self.resource = resource
        self.identifier = identifier
