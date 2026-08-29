"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    create_employee_work_schedule_validator.py

Description:
    Validates CreateEmployeeWorkScheduleCommand.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.attendance.commands.create_employee_work_schedule_command import (
    CreateEmployeeWorkScheduleCommand,
)
from qwos.application.common.results.validation_error import ValidationError
from qwos.application.common.results.validation_result import ValidationResult


class CreateEmployeeWorkScheduleValidator:
    """
    Validator for CreateEmployeeWorkScheduleCommand.
    """

    def validate(
        self,
        command: CreateEmployeeWorkScheduleCommand,
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
        # Work Schedule
        # ------------------------------------------------------------------

        if not command.work_schedule_id.strip():
            errors.append(
                ValidationError(
                    field="work_schedule_id",
                    message="Work schedule ID is required.",
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
                    message=("Effective until cannot be earlier than effective from."),
                )
            )

        return ValidationResult(errors=errors)
