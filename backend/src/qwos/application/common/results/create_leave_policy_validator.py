from decimal import Decimal

from qwos.application.common.results.validation_result import ValidationResult
from qwos.application.leave.commands.create_leave_policy_command import (
    CreateLeavePolicyCommand,
)


class CreateLeavePolicyValidator:
    def validate(
        self,
        command: CreateLeavePolicyCommand,
    ) -> ValidationResult:
        errors: list[str] = []

        if not command.leave_type_id.strip():
            errors.append("leave_type_id is required.")

        if not command.policy_code.strip():
            errors.append("policy_code is required.")

        if not command.policy_name.strip():
            errors.append("policy_name is required.")

        if not command.accrual_method.strip():
            errors.append("accrual_method is required.")

        if not command.accrual_frequency.strip():
            errors.append("accrual_frequency is required.")

        if command.entitlement_days < Decimal("0"):
            errors.append(
                "entitlement_days must be greater than or equal to 0."
            )

        if (
            command.carry_forward_days is not None
            and command.carry_forward_days < Decimal("0")
        ):
            errors.append(
                "carry_forward_days must be greater than or equal to 0."
            )

        if command.minimum_service_days < 0:
            errors.append(
                "minimum_service_days must be greater than or equal to 0."
            )

        return ValidationResult(errors=errors)