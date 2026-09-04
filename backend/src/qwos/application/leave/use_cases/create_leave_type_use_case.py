"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Create Leave Type Use Case

Author:
    Richard Balabarcon
===============================================================================
"""

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
from qwos.application.common.results.create_leave_type_validator import (
    CreateLeaveTypeValidator,
)
from qwos.application.leave.commands.create_leave_type_command import (
    CreateLeaveTypeCommand,
)
from qwos.application.leave.responses.create_leave_type_response import (
    CreateLeaveTypeResponse,
)
from qwos.domains.leave.models.leave_type import LeaveType
from qwos.domains.leave.repositories.leave_type_repository import (
    LeaveTypeRepository,
)


class CreateLeaveTypeUseCase:
    """
    Creates a tenant leave type.
    """

    def __init__(
        self,
        *,
        leave_type_repository: LeaveTypeRepository,
        id_generator: IdGenerator,
        unit_of_work: UnitOfWork,
        validator: CreateLeaveTypeValidator,
        request_context: RequestContext,
    ) -> None:
        self._leave_type_repository = leave_type_repository
        self._id_generator = id_generator
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._request_context = request_context

    async def execute(
        self,
        command: CreateLeaveTypeCommand,
    ) -> CreateLeaveTypeResponse:
        validation = self._validator.validate(command)

        if validation.errors:
            raise ValidationException(validation)

        normalized_code = command.leave_code.strip().lower()

        if self._leave_type_repository.exists_by_code(
            tenant_id=command.tenant_id,
            leave_code=normalized_code,
        ):
            raise DuplicateResourceException(
                resource="LeaveType",
                field="leave_code",
                value=normalized_code,
            )

        leave_type_id = self._id_generator.generate()

        leave_type = LeaveType.create(
            id=leave_type_id,
            tenant_id=command.tenant_id,
            leave_code=command.leave_code,
            leave_name=command.leave_name,
            description=command.description,
            is_paid=command.is_paid,
            is_active=command.is_active,
            created_by=self._request_context.user_id,
        )

        with self._unit_of_work:
            self._leave_type_repository.save(leave_type)
            self._unit_of_work.flush()

        return CreateLeaveTypeResponse(
            id=leave_type.id,
            leave_code=leave_type.leave_code,
            leave_name=leave_type.leave_name,
            description=leave_type.description,
            is_paid=leave_type.is_paid,
            is_active=leave_type.is_active,
            created_at=leave_type.created_at,
        )