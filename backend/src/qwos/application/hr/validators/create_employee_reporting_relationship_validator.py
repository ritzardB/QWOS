from __future__ import annotations

from qwos.application.common.results.validation_error import ValidationError
from qwos.application.common.results.validation_result import ValidationResult
from qwos.application.hr.commands.create_employee_reporting_relationship_command import (
    CreateEmployeeReportingRelationshipCommand,
)


class CreateEmployeeReportingRelationshipValidator:
    """
    Validator for CreateEmployeeReportingRelationshipCommand.
    """

    def validate(
        self,
        command: CreateEmployeeReportingRelationshipCommand,
    ) -> ValidationResult:
        errors: list[ValidationError] = []

        if not command.tenant_id.strip():
            errors.append(
                ValidationError(
                    field="tenant_id",
                    message="Tenant ID is required.",
                )
            )

        if not command.employee_id.strip():
            errors.append(
                ValidationError(
                    field="employee_id",
                    message="Employee ID is required.",
                )
            )

        if not command.manager_employee_id.strip():
            errors.append(
                ValidationError(
                    field="manager_employee_id",
                    message="Manager employee ID is required.",
                )
            )

        if command.employee_id == command.manager_employee_id:
            errors.append(
                ValidationError(
                    field="manager_employee_id",
                    message="An employee cannot report to themselves.",
                )
            )

        if not command.relationship_type.strip():
            errors.append(
                ValidationError(
                    field="relationship_type",
                    message="Relationship type is required.",
                )
            )

        if command.effective_to is not None and command.effective_to < command.effective_from:
            errors.append(
                ValidationError(
                    field="effective_to",
                    message=("Effective-to date cannot be earlier than effective-from date."),
                )
            )

        return ValidationResult(errors=errors)
