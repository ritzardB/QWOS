"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    create_employee_use_case.py

Description:
    Creates a new HR employee record.

Responsibilities:
    - Validate the command
    - Validate optional QWOS user linkage
    - Enforce employee business rules
    - Generate tenant-specific employee number
    - Create employee aggregate
    - Persist employee atomically
    - Return application response

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

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
from qwos.application.common.ports.employee_number_generator import (
    EmployeeNumberGenerator,
)
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.application.hr.commands.create_employee_command import (
    CreateEmployeeCommand,
)
from qwos.application.hr.responses.create_employee_response import (
    CreateEmployeeResponse,
)
from qwos.application.hr.validators.create_employee_validator import (
    CreateEmployeeValidator,
)
from qwos.domains.hr.models.employee import Employee
from qwos.domains.hr.repositories.employee_repository import (
    EmployeeRepository,
)
from qwos.domains.identity.repositories.user_repository import (
    UserRepository,
)


class CreateEmployeeUseCase:
    """
    Use case for creating a new employee.
    """

    def __init__(
        self,
        *,
        employee_repository: EmployeeRepository,
        user_repository: UserRepository,
        employee_number_generator: EmployeeNumberGenerator,
        id_generator: IdGenerator,
        unit_of_work: UnitOfWork,
        validator: CreateEmployeeValidator,
        request_context: RequestContext,
    ) -> None:
        self._employee_repository = employee_repository
        self._user_repository = user_repository
        self._employee_number_generator = employee_number_generator
        self._id_generator = id_generator
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._request_context = request_context

    async def execute(
        self,
        command: CreateEmployeeCommand,
    ) -> CreateEmployeeResponse:
        """
        Execute the Create Employee use case.
        """

        # ------------------------------------------------------------------
        # Validate command
        # ------------------------------------------------------------------

        validation = self._validator.validate(command)

        if validation.errors:
            raise ValidationException(validation)

        # ------------------------------------------------------------------
        # Optional user validation
        # ------------------------------------------------------------------

        if command.user_id is not None:
            user = self._user_repository.get_by_id(
                command.user_id,
            )

            if user is None:
                raise ResourceNotFoundException(
                    resource="User",
                    identifier=command.user_id,
                )

            if user.tenant_id != command.tenant_id:
                raise ValueError(
                    "User does not belong to the requested tenant."
                )

            if self._employee_repository.exists_by_user_id(
                tenant_id=command.tenant_id,
                user_id=command.user_id,
            ):
                raise DuplicateResourceException(
                    resource="Employee",
                    field="user_id",
                    value=command.user_id,
                )

        # ------------------------------------------------------------------
        # Work email uniqueness
        # ------------------------------------------------------------------

        if command.work_email is not None:
            normalized_work_email = command.work_email.strip().lower()

            if self._employee_repository.exists_by_work_email(
                tenant_id=command.tenant_id,
                work_email=normalized_work_email,
            ):
                raise DuplicateResourceException(
                    resource="Employee",
                    field="work_email",
                    value=normalized_work_email,
                )

        # ------------------------------------------------------------------
        # Persist atomically
        # ------------------------------------------------------------------

        with self._unit_of_work:
            employee_number = self._employee_number_generator.generate(
                tenant_id=command.tenant_id,
            )

            employee_id = self._id_generator.generate()

            employee = Employee.create(
                id=employee_id,
                tenant_id=command.tenant_id,
                employee_number=employee_number,
                user_id=command.user_id,
                hire_date=command.hire_date,
                employment_status=command.employment_status,
                employment_type=command.employment_type,
                work_email=command.work_email,
                work_phone=command.work_phone,
                created_by=self._request_context.user_id,
            )

            self._employee_repository.save(employee)
            self._unit_of_work.flush()

        # ------------------------------------------------------------------
        # Response
        # ------------------------------------------------------------------

        return CreateEmployeeResponse(
            id=employee.id,
            employee_number=employee.employee_number,
            user_id=employee.user_id,
            hire_date=employee.hire_date,
            employment_status=employee.employment_status,
            employment_type=employee.employment_type,
            work_email=employee.work_email,
            work_phone=employee.work_phone,
            created_at=employee.created_at,
        )

        # ------------------------------------------------------------------
        # Work email uniqueness
        # ------------------------------------------------------------------

        if command.work_email is not None:
            normalized_work_email = command.work_email.strip().lower()

            if self._employee_repository.exists_by_work_email(
                tenant_id=command.tenant_id,
                work_email=normalized_work_email,
            ):
                raise DuplicateResourceException(
                    resource="Employee",
                    field="work_email",
                    value=normalized_work_email,
                )