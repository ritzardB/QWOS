"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    create_employee_work_arrangement_validator.py

Description:
    Validates CreateEmployeeWorkArrangementCommand.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.attendance.commands.create_employee_work_arrangement_command import (
    CreateEmployeeWorkArrangementCommand,
)
from qwos.application.common.results.validation_error import ValidationError
from qwos.application.common.results.validation_result import ValidationResult


class CreateEmployeeWorkArrangementValidator:
    """
    Validator for CreateEmployeeWorkArrangementCommand.
    """

    ALLOWED_WORK_ARRANGEMENTS = {
        "office",
        "hybrid",
        "remote",
    }

    def validate(
        self,
        command: CreateEmployeeWorkArrangementCommand,
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
        # Work Arrangement
        # ------------------------------------------------------------------

        normalized_arrangement = (
            command.work_arrangement.strip().lower()
        )

        if not normalized_arrangement:
            errors.append(
                ValidationError(
                    field="work_arrangement",
                    message="Work arrangement is required.",
                )
            )

        elif normalized_arrangement not in (
            self.ALLOWED_WORK_ARRANGEMENTS
        ):
            errors.append(
                ValidationError(
                    field="work_arrangement",
                    message=(
                        "Work arrangement must be one of: "
                        "office, hybrid, remote."
                    ),
                )
            )

        # ------------------------------------------------------------------
        # Effective From
        # ------------------------------------------------------------------

        if command.effective_from is None:
            errors.append(
                ValidationError(
                    field="effective_from",
                    message="Effective from date is required.",
                )
            )

        # ------------------------------------------------------------------
        # Effective Until
        # ------------------------------------------------------------------

        if (
            command.effective_from is not None
            and command.effective_until is not None
            and command.effective_until < command.effective_from
        ):
            errors.append(
                ValidationError(
                    field="effective_until",
                    message=(
                        "Effective until cannot be earlier than "
                        "effective from."
                    ),
                )
            )

        return ValidationResult(errors=errors)
