from __future__ import annotations

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.duplicate_resource_exception import (
    DuplicateResourceException,
)
from qwos.application.common.exceptions.validation_exception import (
    ValidationException,
)
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.application.common.results.create_employee_leave_assignment_validator import (
    CreateEmployeeLeaveAssignmentValidator,
)
from qwos.application.leave.commands.create_employee_leave_assignment_command import (
    CreateEmployeeLeaveAssignmentCommand,
)
from qwos.application.leave.responses.create_employee_leave_assignment_response import (
    CreateEmployeeLeaveAssignmentResponse,
)
from qwos.domains.leave.models.employee_leave_assignment import (
    EmployeeLeaveAssignment,
)
from qwos.domains.leave.repositories.employee_leave_assignment_repository import (
    EmployeeLeaveAssignmentRepository,
)


class CreateEmployeeLeaveAssignmentUseCase:
    def __init__(
        self,
        *,
        employee_leave_assignment_repository: EmployeeLeaveAssignmentRepository,
        id_generator: IdGenerator,
        unit_of_work: UnitOfWork,
        validator: CreateEmployeeLeaveAssignmentValidator,
        request_context: RequestContext,
    ) -> None:
        self._employee_leave_assignment_repository = (
            employee_leave_assignment_repository
        )
        self._id_generator = id_generator
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._request_context = request_context

    async def execute(
        self,
        command: CreateEmployeeLeaveAssignmentCommand,
    ) -> CreateEmployeeLeaveAssignmentResponse:
        validation = self._validator.validate(command)

        if validation.errors:
            raise ValidationException(validation)

        if self._employee_leave_assignment_repository.exists_by_employee_and_start_date(
            tenant_id=command.tenant_id,
            employee_id=command.employee_id,
            effective_from=command.effective_from,
        ):
            raise DuplicateResourceException(
                resource="EmployeeLeaveAssignment",
                field="effective_from",
                value=str(command.effective_from),
            )

        assignment_id = self._id_generator.generate()

        assignment = EmployeeLeaveAssignment.create(
            id=assignment_id,
            tenant_id=command.tenant_id,
            employee_id=command.employee_id,
            leave_policy_id=command.leave_policy_id,
            effective_from=command.effective_from,
            effective_until=command.effective_until,
            is_active=command.is_active,
            created_by=self._request_context.user_id,
        )

        with self._unit_of_work:
            self._employee_leave_assignment_repository.save(assignment)
            self._unit_of_work.flush()

        return CreateEmployeeLeaveAssignmentResponse(
            id=assignment.id,
            employee_id=assignment.employee_id,
            leave_policy_id=assignment.leave_policy_id,
            effective_from=assignment.effective_from,
            effective_until=assignment.effective_until,
            is_active=assignment.is_active,
            created_at=assignment.created_at,
        )