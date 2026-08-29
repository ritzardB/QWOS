"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    create_employee_work_arrangement_use_case.py

Description:
    Creates an effective-dated employee work arrangement.

Responsibilities:
    - Validate the command
    - Verify employee existence
    - Enforce tenant isolation
    - Prevent duplicate start dates
    - Create EmployeeWorkArrangement
    - Persist atomically
    - Return application response

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.attendance.commands.create_employee_work_arrangement_command import (
    CreateEmployeeWorkArrangementCommand,
)
from qwos.application.attendance.responses.create_employee_work_arrangement_response import (
    CreateEmployeeWorkArrangementResponse,
)
from qwos.application.attendance.validators.create_employee_work_arrangement_validator import (
    CreateEmployeeWorkArrangementValidator,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.duplicate_resource_exception import (
    DuplicateResourceException,
)
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.common.exceptions.validation_exception import (
    ValidationException,
)
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.domains.attendance.models.employee_work_arrangement import (
    EmployeeWorkArrangement,
)
from qwos.domains.attendance.repositories.employee_work_arrangement_repository import (
    EmployeeWorkArrangementRepository,
)
from qwos.domains.hr.repositories.employee_repository import (
    EmployeeRepository,
)


class CreateEmployeeWorkArrangementUseCase:
    """
    Use case for creating an employee work arrangement.
    """

    def __init__(
        self,
        *,
        employee_repository: EmployeeRepository,
        employee_work_arrangement_repository: (EmployeeWorkArrangementRepository),
        id_generator: IdGenerator,
        unit_of_work: UnitOfWork,
        validator: CreateEmployeeWorkArrangementValidator,
        request_context: RequestContext,
    ) -> None:
        self._employee_repository = employee_repository
        self._employee_work_arrangement_repository = employee_work_arrangement_repository
        self._id_generator = id_generator
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._request_context = request_context

    async def execute(
        self,
        command: CreateEmployeeWorkArrangementCommand,
    ) -> CreateEmployeeWorkArrangementResponse:
        """
        Create an employee work arrangement.
        """

        # ------------------------------------------------------------------
        # Validate command
        # ------------------------------------------------------------------

        validation = self._validator.validate(command)

        if validation.errors:
            raise ValidationException(validation)

        # ------------------------------------------------------------------
        # Locate employee
        # ------------------------------------------------------------------

        employee = self._employee_repository.get_by_id(
            command.employee_id,
        )

        if employee is None:
            raise ResourceNotFoundException(
                resource="Employee",
                identifier=command.employee_id,
            )

        # ------------------------------------------------------------------
        # Tenant isolation
        # ------------------------------------------------------------------

        if employee.tenant_id != command.tenant_id:
            raise ValueError("Employee does not belong to the requested tenant.")

        # ------------------------------------------------------------------
        # Duplicate start date check
        # ------------------------------------------------------------------

        if self._employee_work_arrangement_repository.exists_by_employee_and_start_date(
            tenant_id=command.tenant_id,
            employee_id=command.employee_id,
            effective_from=command.effective_from,
        ):
            raise DuplicateResourceException(
                resource="EmployeeWorkArrangement",
                field="effective_from",
                value=str(command.effective_from),
            )

        # ------------------------------------------------------------------
        # Generate identifier
        # ------------------------------------------------------------------

        arrangement_id = self._id_generator.generate()

        # ------------------------------------------------------------------
        # Create arrangement
        # ------------------------------------------------------------------

        arrangement = EmployeeWorkArrangement.create(
            id=arrangement_id,
            tenant_id=command.tenant_id,
            employee_id=employee.id,
            work_arrangement=command.work_arrangement,
            effective_from=command.effective_from,
            effective_until=command.effective_until,
            is_active=command.is_active,
            created_by=self._request_context.user_id,
        )

        # ------------------------------------------------------------------
        # Persist atomically
        # ------------------------------------------------------------------

        with self._unit_of_work:
            self._employee_work_arrangement_repository.save(
                arrangement,
            )
            self._unit_of_work.flush()

        # ------------------------------------------------------------------
        # Response
        # ------------------------------------------------------------------

        return CreateEmployeeWorkArrangementResponse(
            id=arrangement.id,
            employee_id=arrangement.employee_id,
            work_arrangement=arrangement.work_arrangement,
            effective_from=arrangement.effective_from,
            effective_until=arrangement.effective_until,
            is_active=arrangement.is_active,
            created_at=arrangement.created_at,
        )
