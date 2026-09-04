from __future__ import annotations

from qwos.application.common.results.validation_result import ValidationResult
from qwos.application.leave.commands.create_leave_type_command import (
    CreateLeaveTypeCommand,
)


class CreateLeaveTypeValidator:
    def validate(self, command: CreateLeaveTypeCommand) -> ValidationResult:
        errors: dict[str, str] = {}

        if not command.tenant_id.strip():
            errors["tenant_id"] = "tenant_id is required."

        if not command.leave_code.strip():
            errors["leave_code"] = "leave_code is required."

        if not command.leave_name.strip():
            errors["leave_name"] = "leave_name is required."

        return ValidationResult(errors=errors)