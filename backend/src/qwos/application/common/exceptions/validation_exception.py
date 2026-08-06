"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Validation Exception
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.exceptions.application_exception import (
    ApplicationException,
)
from qwos.application.common.results.validation_result import ValidationResult


class ValidationException(ApplicationException):
    """
    Raised when command validation fails.
    """

    def __init__(
        self,
        validation_result: ValidationResult,
    ) -> None:
        super().__init__("Validation failed.")

        self.validation_result = validation_result