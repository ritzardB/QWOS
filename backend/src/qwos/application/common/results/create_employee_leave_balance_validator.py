from __future__ import annotations

from qwos.application.common.results.validation_result import ValidationResult
from qwos.application.leave.commands.create_employee_leave_balance_command import (
    CreateEmployeeLeaveBalanceCommand,
)


class CreateEmployeeLeaveBalanceValidator:
    def validate(
        self,
        command: CreateEmployeeLeaveBalanceCommand,
    ) -> ValidationResult:
        errors: list[str] = []

        if not command.employee_leave_assignment_id.strip():
            errors.append("employee_leave_assignment_id is required.")

        if not command.employee_id.strip():
            errors.append("employee_id is required.")

        if command.period_end < command.period_start:
            errors.append(
                "period_end must be greater than or equal to period_start."
            )

        if command.entitlement_days < 0:
            errors.append(
                "entitlement_days must be greater than or equal to 0."
            )

        if command.carried_forward_days < 0:
            errors.append(
                "carried_forward_days must be greater than or equal to 0."
            )

        if command.accrued_days < 0:
            errors.append(
                "accrued_days must be greater than or equal to 0."
            )

        if command.used_days < 0:
            errors.append(
                "used_days must be greater than or equal to 0."
            )

        return ValidationResult(errors=errors)