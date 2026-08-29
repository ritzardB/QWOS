"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    create_employee_validator.py

Description:
    Validates CreateEmployeeCommand before execution.

Responsibilities:
    - Validate required fields
    - Validate field formats
    - Validate basic business-independent rules

Notes:
    This validator performs structural validation only.
    Repository-backed business rules belong in the use case.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import re

from qwos.application.common.results.validation_error import ValidationError
from qwos.application.common.results.validation_result import ValidationResult
from qwos.application.hr.commands.create_employee_command import (
    CreateEmployeeCommand,
)


class CreateEmployeeValidator:
    """
    Validator for CreateEmployeeCommand.
    """

    EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    IDENTIFIER_PATTERN = re.compile(r"^[a-z][a-z0-9_]{1,49}$")

    def validate(
        self,
        command: CreateEmployeeCommand,
    ) -> ValidationResult:
        """
        Validate the command.
        """

        errors: list[ValidationError] = []

        # ------------------------------------------------------------------
        # Tenant
        # ------------------------------------------------------------------

        if not command.tenant_id.strip():
            errors.append(
                ValidationError(
                    field="tenant_id",
                    message="Tenant ID is required.",
                )
            )

        # ------------------------------------------------------------------
        # User ID
        # ------------------------------------------------------------------

        if command.user_id is not None:
            if not command.user_id.strip():
                errors.append(
                    ValidationError(
                        field="user_id",
                        message="User ID cannot be empty.",
                    )
                )

        # ------------------------------------------------------------------
        # Employment Status
        # ------------------------------------------------------------------

        if not command.employment_status.strip():
            errors.append(
                ValidationError(
                    field="employment_status",
                    message="Employment status is required.",
                )
            )

        elif not self.IDENTIFIER_PATTERN.fullmatch(command.employment_status):
            errors.append(
                ValidationError(
                    field="employment_status",
                    message="Employment status format is invalid.",
                )
            )

        # ------------------------------------------------------------------
        # Employment Type
        # ------------------------------------------------------------------

        if not command.employment_type.strip():
            errors.append(
                ValidationError(
                    field="employment_type",
                    message="Employment type is required.",
                )
            )

        elif not self.IDENTIFIER_PATTERN.fullmatch(command.employment_type):
            errors.append(
                ValidationError(
                    field="employment_type",
                    message="Employment type format is invalid.",
                )
            )

        # ------------------------------------------------------------------
        # Work Email
        # ------------------------------------------------------------------

        if command.work_email is not None:
            if not command.work_email.strip():
                errors.append(
                    ValidationError(
                        field="work_email",
                        message="Work email cannot be empty.",
                    )
                )

            elif not self.EMAIL_PATTERN.fullmatch(command.work_email):
                errors.append(
                    ValidationError(
                        field="work_email",
                        message="Work email format is invalid.",
                    )
                )

        # ------------------------------------------------------------------
        # Work Phone
        # ------------------------------------------------------------------

        if command.work_phone is not None:
            if not command.work_phone.strip():
                errors.append(
                    ValidationError(
                        field="work_phone",
                        message="Work phone cannot be empty.",
                    )
                )

            elif len(command.work_phone.strip()) > 30:
                errors.append(
                    ValidationError(
                        field="work_phone",
                        message="Work phone cannot exceed 30 characters.",
                    )
                )

        return ValidationResult(errors=errors)
