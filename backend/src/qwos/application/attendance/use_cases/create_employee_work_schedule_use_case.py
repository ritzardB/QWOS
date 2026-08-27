"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    create_employee_work_schedule_use_case.py

Description:
    Creates an effective-dated employee work schedule assignment.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.attendance.commands.create_employee_work_schedule_command import (
    CreateEmployeeWorkScheduleCommand,
)
from qwos.application.attendance.responses.create_employee_work_schedule_response import (
    CreateEmployeeWorkScheduleResponse,
)
from qwos.application.attendance.validators.create_employee_work_schedule_validator import (
    CreateEmployeeWorkScheduleValidator,
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
from qwos.domains.attendance.models.employee_work_schedule import (
    EmployeeWorkSchedule,
)
from qwos.domains.attendance.repositories.employee_work_schedule_repository import (
    EmployeeWorkScheduleRepository,
)
from qwos.domains.attendance.repositories.work_schedule_repository import (
    WorkScheduleRepository,
)
from qwos.domains.hr.repositories.employee_repository import (
    EmployeeRepository,
)


class CreateEmployeeWorkScheduleUseCase:
    """
    Use case for creating an employee work schedule assignment.
    """

    def __init__(
        self,
        *,
        employee_repository: EmployeeRepository,
        work_schedule_repository: WorkScheduleRepository,
        employee_work_schedule_repository: EmployeeWorkScheduleRepository,
        id_generator: IdGenerator,
        unit_of_work: UnitOfWork,
        validator: CreateEmployeeWorkScheduleValidator,
        request_context: RequestContext,
    ) -> None:
        self._employee_repository = employee_repository
        self._work_schedule_repository = work_schedule_repository
        self._employee_work_schedule_repository = (
            employee_work_schedule_repository
        )
        self._id_generator = id_generator
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._request_context = request_context

    async def execute(
        self,
        command: CreateEmployeeWorkScheduleCommand,
    ) -> CreateEmployeeWorkScheduleResponse:
        """
        Create an employee work schedule assignment.
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
            raise ValueError(
                "Employee does not belong to the requested tenant.",
            )

        # ------------------------------------------------------------------
        # Locate work schedule
        # ------------------------------------------------------------------

        work_schedule = self._work_schedule_repository.get_by_id_for_tenant(
            tenant_id=command.tenant_id,
            schedule_id=command.work_schedule_id,
        )

        if work_schedule is None:
            raise ResourceNotFoundException(
                resource="WorkSchedule",
                identifier=command.work_schedule_id,
            )

        # ------------------------------------------------------------------
        # Duplicate start date check
        # ------------------------------------------------------------------

        if (
            self._employee_work_schedule_repository
            .exists_by_employee_and_start_date(
                tenant_id=command.tenant_id,
                employee_id=command.employee_id,
                effective_from=command.effective_from,
            )
        ):
            raise DuplicateResourceException(
                resource="EmployeeWorkSchedule",
                field="effective_from",
                value=str(command.effective_from),
            )

        # ------------------------------------------------------------------
        # Generate identifier
        # ------------------------------------------------------------------

        assignment_id = self._id_generator.generate()

        # ------------------------------------------------------------------
        # Create assignment
        # ------------------------------------------------------------------

        assignment = EmployeeWorkSchedule.create(
            id=assignment_id,
            tenant_id=command.tenant_id,
            employee_id=employee.id,
            work_schedule_id=work_schedule.id,
            effective_from=command.effective_from,
            effective_until=command.effective_until,
            is_active=command.is_active,
            created_by=self._request_context.user_id,
        )

        # ------------------------------------------------------------------
        # Persist atomically
        # ------------------------------------------------------------------

        with self._unit_of_work:
            self._employee_work_schedule_repository.save(
                assignment,
            )
            self._unit_of_work.flush()

        # ------------------------------------------------------------------
        # Response
        # ------------------------------------------------------------------

        return CreateEmployeeWorkScheduleResponse(
            id=assignment.id,
            employee_id=assignment.employee_id,
            work_schedule_id=assignment.work_schedule_id,
            effective_from=assignment.effective_from,
            effective_until=assignment.effective_until,
            is_active=assignment.is_active,
            created_at=assignment.created_at,
        )