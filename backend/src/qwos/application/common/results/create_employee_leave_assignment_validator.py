from __future__ import annotations

from qwos.application.common.results.validation_result import ValidationResult
from qwos.application.leave.commands.create_employee_leave_assignment_command import (
    CreateEmployeeLeaveAssignmentCommand,
)


class CreateEmployeeLeaveAssignmentValidator:
    def validate(
        self,
        command: CreateEmployeeLeaveAssignmentCommand,
    ) -> ValidationResult:
        errors: list[str] = []

        if not command.employee_id.strip():
            errors.append("employee_id is required.")

        if not command.leave_policy_id.strip():
            errors.append("leave_policy_id is required.")

        if (
            command.effective_until is not None
            and command.effective_until < command.effective_from
        ):
            errors.append(
                "effective_until must be greater than or equal to effective_from."
            )

        return ValidationResult(errors=errors)