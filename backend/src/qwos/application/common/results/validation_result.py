"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Validation Result

File:
    validation_result.py

Description:
    Represents the result of command validation.

Responsibilities:
    - Indicate whether validation succeeded
    - Collect validation errors
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from qwos.application.common.results.validation_error import (
    ValidationError,
)


@dataclass(slots=True)
class ValidationResult:
    """
    Result of validating a command.
    """

    errors: list[ValidationError] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """
        Returns True when no validation errors exist.
        """
        return not self.errors

    def add_error(
        self,
        field: str,
        message: str,
    ) -> None:
        """
        Add a validation error.
        """
        self.errors.append(
            ValidationError(
                field=field,
                message=message,
            )
        )