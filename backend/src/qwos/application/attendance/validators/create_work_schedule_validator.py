from __future__ import annotations

from qwos.application.attendance.commands.create_work_schedule_command import (
    CreateWorkScheduleCommand,
)
from qwos.application.common.results.validation_error import ValidationError
from qwos.application.common.results.validation_result import ValidationResult


class CreateWorkScheduleValidator:
    """
    Validator for CreateWorkScheduleCommand.
    """

    def validate(
        self,
        command: CreateWorkScheduleCommand,
    ) -> ValidationResult:
        errors: list[ValidationError] = []

        if not command.tenant_id.strip():
            errors.append(
                ValidationError(
                    field="tenant_id",
                    message="Tenant ID is required.",
                )
            )

        if not command.schedule_code.strip():
            errors.append(
                ValidationError(
                    field="schedule_code",
                    message="Schedule code is required.",
                )
            )

        if not command.schedule_name.strip():
            errors.append(
                ValidationError(
                    field="schedule_name",
                    message="Schedule name is required.",
                )
            )

        if not command.timezone.strip():
            errors.append(
                ValidationError(
                    field="timezone",
                    message="Timezone is required.",
                )
            )

        return ValidationResult(errors=errors)