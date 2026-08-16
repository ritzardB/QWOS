"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    create_employee_profile_validator.py

Description:
    Validates CreateEmployeeProfileCommand.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import re

from qwos.application.common.results.validation_error import ValidationError
from qwos.application.common.results.validation_result import ValidationResult
from qwos.application.hr.commands.create_employee_profile_command import (
    CreateEmployeeProfileCommand,
)


class CreateEmployeeProfileValidator:
    """
    Validator for CreateEmployeeProfileCommand.
    """

    EMAIL_PATTERN = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    COUNTRY_CODE_PATTERN = re.compile(
        r"^[A-Za-z]{2}$"
    )

    def validate(
        self,
        command: CreateEmployeeProfileCommand,
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
        # Employee
        # ------------------------------------------------------------------

        if not command.employee_id.strip():
            errors.append(
                ValidationError(
                    field="employee_id",
                    message="Employee ID is required.",
                )
            )

        # ------------------------------------------------------------------
        # Personal Email
        # ------------------------------------------------------------------

        if command.personal_email is not None:
            if not command.personal_email.strip():
                errors.append(
                    ValidationError(
                        field="personal_email",
                        message="Personal email cannot be empty.",
                    )
                )

            elif not self.EMAIL_PATTERN.fullmatch(
                command.personal_email
            ):
                errors.append(
                    ValidationError(
                        field="personal_email",
                        message="Personal email format is invalid.",
                    )
                )

        # ------------------------------------------------------------------
        # Country Code
        # ------------------------------------------------------------------

        if command.country_code is not None:
            country_code = command.country_code.strip()

            if not country_code:
                errors.append(
                    ValidationError(
                        field="country_code",
                        message="Country code cannot be empty.",
                    )
                )

            elif not self.COUNTRY_CODE_PATTERN.fullmatch(
                country_code
            ):
                errors.append(
                    ValidationError(
                        field="country_code",
                        message="Country code must contain 2 letters.",
                    )
                )

        # ------------------------------------------------------------------
        # Personal Phone
        # ------------------------------------------------------------------

        if command.personal_phone is not None:
            if not command.personal_phone.strip():
                errors.append(
                    ValidationError(
                        field="personal_phone",
                        message="Personal phone cannot be empty.",
                    )
                )

            elif len(command.personal_phone.strip()) > 30:
                errors.append(
                    ValidationError(
                        field="personal_phone",
                        message="Personal phone cannot exceed 30 characters.",
                    )
                )

        # ------------------------------------------------------------------
        # Emergency Contact Phone
        # ------------------------------------------------------------------

        if command.emergency_contact_phone is not None:
            if not command.emergency_contact_phone.strip():
                errors.append(
                    ValidationError(
                        field="emergency_contact_phone",
                        message="Emergency contact phone cannot be empty.",
                    )
                )

            elif len(command.emergency_contact_phone.strip()) > 30:
                errors.append(
                    ValidationError(
                        field="emergency_contact_phone",
                        message=(
                            "Emergency contact phone cannot exceed 30 "
                            "characters."
                        ),
                    )
                )

        return ValidationResult(errors=errors)