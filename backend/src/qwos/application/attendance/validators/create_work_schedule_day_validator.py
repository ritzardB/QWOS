"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    create_work_schedule_day_validator.py

Description:
    Validates CreateWorkScheduleDayCommand.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.attendance.commands.create_work_schedule_day_command import (
    CreateWorkScheduleDayCommand,
)
from qwos.application.common.results.validation_error import ValidationError
from qwos.application.common.results.validation_result import ValidationResult


class CreateWorkScheduleDayValidator:
    """
    Validator for CreateWorkScheduleDayCommand.
    """

    ALLOWED_DAY_TYPES = {
        "workday",
        "rest_day",
    }

    def validate(
        self,
        command: CreateWorkScheduleDayCommand,
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
        # Day of Week
        # ------------------------------------------------------------------

        if command.day_of_week < 1 or command.day_of_week > 7:
            errors.append(
                ValidationError(
                    field="day_of_week",
                    message="Day of week must be between 1 and 7.",
                )
            )

        # ------------------------------------------------------------------
        # Day Type
        # ------------------------------------------------------------------

        normalized_day_type = command.day_type.strip().lower()

        if not normalized_day_type:
            errors.append(
                ValidationError(
                    field="day_type",
                    message="Day type is required.",
                )
            )

        elif normalized_day_type not in self.ALLOWED_DAY_TYPES:
            errors.append(
                ValidationError(
                    field="day_type",
                    message=("Day type must be one of: workday, rest_day."),
                )
            )

        # ------------------------------------------------------------------
        # Workday Times
        # ------------------------------------------------------------------

        if normalized_day_type == "workday":
            if command.start_time is None:
                errors.append(
                    ValidationError(
                        field="start_time",
                        message="Start time is required for a workday.",
                    )
                )

            if command.end_time is None:
                errors.append(
                    ValidationError(
                        field="end_time",
                        message="End time is required for a workday.",
                    )
                )

        # ------------------------------------------------------------------
        # Rest Day
        # ------------------------------------------------------------------

        if normalized_day_type == "rest_day":
            if command.start_time is not None:
                errors.append(
                    ValidationError(
                        field="start_time",
                        message="Rest day cannot have a start time.",
                    )
                )

            if command.end_time is not None:
                errors.append(
                    ValidationError(
                        field="end_time",
                        message="Rest day cannot have an end time.",
                    )
                )

            if command.break_minutes != 0:
                errors.append(
                    ValidationError(
                        field="break_minutes",
                        message="Rest day break minutes must be zero.",
                    )
                )

            if command.is_overnight:
                errors.append(
                    ValidationError(
                        field="is_overnight",
                        message="Rest day cannot be overnight.",
                    )
                )

        # ------------------------------------------------------------------
        # Break
        # ------------------------------------------------------------------

        if command.break_minutes < 0:
            errors.append(
                ValidationError(
                    field="break_minutes",
                    message="Break minutes cannot be negative.",
                )
            )

        return ValidationResult(errors=errors)
