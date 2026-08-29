"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    create_employee_profile_use_case.py

Description:
    Creates the core HR profile for an existing employee.

Responsibilities:
    - Validate the command
    - Verify employee existence
    - Enforce tenant isolation
    - Prevent duplicate active profiles
    - Create EmployeeProfile aggregate
    - Persist atomically
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
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.application.hr.commands.create_employee_profile_command import (
    CreateEmployeeProfileCommand,
)
from qwos.application.hr.responses.create_employee_profile_response import (
    CreateEmployeeProfileResponse,
)
from qwos.application.hr.validators.create_employee_profile_validator import (
    CreateEmployeeProfileValidator,
)
from qwos.domains.hr.models.employee_profile import EmployeeProfile
from qwos.domains.hr.repositories.employee_profile_repository import (
    EmployeeProfileRepository,
)
from qwos.domains.hr.repositories.employee_repository import (
    EmployeeRepository,
)


class CreateEmployeeProfileUseCase:
    """
    Use case for creating an employee profile.
    """

    def __init__(
        self,
        *,
        employee_repository: EmployeeRepository,
        employee_profile_repository: EmployeeProfileRepository,
        id_generator: IdGenerator,
        unit_of_work: UnitOfWork,
        validator: CreateEmployeeProfileValidator,
        request_context: RequestContext,
    ) -> None:
        self._employee_repository = employee_repository
        self._employee_profile_repository = employee_profile_repository
        self._id_generator = id_generator
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._request_context = request_context

    async def execute(
        self,
        command: CreateEmployeeProfileCommand,
    ) -> CreateEmployeeProfileResponse:
        """
        Create the core HR profile for an employee.
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
        # Duplicate profile check
        # ------------------------------------------------------------------

        if self._employee_profile_repository.exists_by_employee_id(
            tenant_id=command.tenant_id,
            employee_id=command.employee_id,
        ):
            raise DuplicateResourceException(
                resource="EmployeeProfile",
                field="employee_id",
                value=command.employee_id,
            )

        # ------------------------------------------------------------------
        # Generate identifier
        # ------------------------------------------------------------------

        profile_id = self._id_generator.generate()

        # ------------------------------------------------------------------
        # Create profile
        # ------------------------------------------------------------------

        profile = EmployeeProfile.create(
            id=profile_id,
            tenant_id=command.tenant_id,
            employee_id=employee.id,
            date_of_birth=command.date_of_birth,
            gender=command.gender,
            nationality=command.nationality,
            marital_status=command.marital_status,
            personal_email=command.personal_email,
            personal_phone=command.personal_phone,
            address_line_1=command.address_line_1,
            address_line_2=command.address_line_2,
            city=command.city,
            state_province=command.state_province,
            postal_code=command.postal_code,
            country_code=command.country_code,
            emergency_contact_name=command.emergency_contact_name,
            emergency_contact_relationship=(command.emergency_contact_relationship),
            emergency_contact_phone=command.emergency_contact_phone,
            created_by=self._request_context.user_id,
        )

        # ------------------------------------------------------------------
        # Persist atomically
        # ------------------------------------------------------------------

        with self._unit_of_work:
            self._employee_profile_repository.save(profile)
            self._unit_of_work.flush()

        # ------------------------------------------------------------------
        # Response
        # ------------------------------------------------------------------

        return CreateEmployeeProfileResponse(
            id=profile.id,
            employee_id=profile.employee_id,
            date_of_birth=profile.date_of_birth,
            gender=profile.gender,
            nationality=profile.nationality,
            marital_status=profile.marital_status,
            personal_email=profile.personal_email,
            personal_phone=profile.personal_phone,
            address_line_1=profile.address_line_1,
            address_line_2=profile.address_line_2,
            city=profile.city,
            state_province=profile.state_province,
            postal_code=profile.postal_code,
            country_code=profile.country_code,
            emergency_contact_name=profile.emergency_contact_name,
            emergency_contact_relationship=(profile.emergency_contact_relationship),
            emergency_contact_phone=profile.emergency_contact_phone,
            created_at=profile.created_at,
        )
