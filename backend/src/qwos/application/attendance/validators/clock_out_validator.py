"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    clock_out_validator.py

Description:
    Validates the ClockOutCommand before execution.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.attendance.commands.clock_out_command import (
    ClockOutCommand,
)
from qwos.application.common.results.validation_result import (
    ValidationResult,
)


class ClockOutValidator:
    """
    Validates clock-out application commands.
    """

    def validate(
        self,
        command: ClockOutCommand,
    ) -> ValidationResult:
        result = ValidationResult()

        if not command.tenant_id.strip():
            result.add_error(
                field="tenant_id",
                message="tenant_id is required.",
            )

        if not command.employee_id.strip():
            result.add_error(
                field="employee_id",
                message="employee_id is required.",
            )

        if (
            command.clock_out_at is not None
            and command.clock_out_at.tzinfo is None
        ):
            result.add_error(
                field="clock_out_at",
                message="clock_out_at must be timezone-aware.",
            )

        if not command.event_source.strip():
            result.add_error(
                field="event_source",
                message="event_source is required.",
            )

        return result
