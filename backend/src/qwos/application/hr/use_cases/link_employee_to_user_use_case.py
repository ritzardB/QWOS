"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    link_employee_to_user_use_case.py

Description:
    Links an HR employee record to an existing QWOS user and creates the
    corresponding UserProfile.

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
from qwos.application.hr.commands.link_employee_to_user_command import (
    LinkEmployeeToUserCommand,
)
from qwos.application.hr.responses.link_employee_to_user_response import (
    LinkEmployeeToUserResponse,
)
from qwos.domains.hr.repositories.employee_repository import (
    EmployeeRepository,
)
from qwos.domains.identity.models.user_profile import UserProfile
from qwos.domains.identity.repositories.user_profile_repository import (
    UserProfileRepository,
)
from qwos.domains.identity.repositories.user_repository import (
    UserRepository,
)


class LinkEmployeeToUserUseCase:
    """
    Use case for linking an employee to an existing QWOS user.
    """

    def __init__(
        self,
        *,
        employee_repository: EmployeeRepository,
        user_repository: UserRepository,
        user_profile_repository: UserProfileRepository,
        id_generator: IdGenerator,
        unit_of_work: UnitOfWork,
        request_context: RequestContext,
    ) -> None:
        self._employee_repository = employee_repository
        self._user_repository = user_repository
        self._user_profile_repository = user_profile_repository
        self._id_generator = id_generator
        self._unit_of_work = unit_of_work
        self._request_context = request_context

    async def execute(
        self,
        command: LinkEmployeeToUserCommand,
    ) -> LinkEmployeeToUserResponse:
        """
        Link the employee to the user and create the user profile atomically.
        """

        # ------------------------------------------------------------------
        # Basic structural validation
        # ------------------------------------------------------------------

        if not command.first_name.strip():
            raise ValidationException(
                self._validation_result(
                    "first_name",
                    "First name is required.",
                )
            )

        if not command.last_name.strip():
            raise ValidationException(
                self._validation_result(
                    "last_name",
                    "Last name is required.",
                )
            )

        if not command.tenant_id.strip():
            raise ValidationException(
                self._validation_result(
                    "tenant_id",
                    "Tenant ID is required.",
                )
            )

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
        # Employee link state
        # ------------------------------------------------------------------

        if employee.user_id is not None:
            raise DuplicateResourceException(
                resource="Employee",
                field="user_id",
                value=employee.user_id,
            )

        # ------------------------------------------------------------------
        # Locate user
        # ------------------------------------------------------------------

        user = self._user_repository.get_by_id(
            command.user_id,
        )

        if user is None:
            raise ResourceNotFoundException(
                resource="User",
                identifier=command.user_id,
            )

        if user.tenant_id != command.tenant_id:
            raise ValueError("User does not belong to the requested tenant.")

        # ------------------------------------------------------------------
        # Check profile
        # ------------------------------------------------------------------

        existing_profile = self._user_profile_repository.get_by_user_id(
            command.user_id,
        )

        if existing_profile is not None:
            if (
                existing_profile.first_name != command.first_name.strip()
                or existing_profile.middle_name != (command.middle_name.strip() if command.middle_name else None)
                or existing_profile.last_name != command.last_name.strip()
                or existing_profile.preferred_name
                != (command.preferred_name.strip() if command.preferred_name else None)
            ):
                raise ValueError("Existing UserProfile does not match the supplied identity data.")

            profile = existing_profile

        else:
            profile_id = self._id_generator.generate()

            profile = UserProfile.create(
                id=profile_id,
                tenant_id=command.tenant_id,
                user_id=command.user_id,
                first_name=command.first_name,
                middle_name=command.middle_name,
                last_name=command.last_name,
                preferred_name=command.preferred_name,
            )

        # ------------------------------------------------------------------
        # Link and persist atomically
        # ------------------------------------------------------------------

        with self._unit_of_work:
            employee.user_id = command.user_id

            if existing_profile is None:
                self._user_profile_repository.save(profile)

            self._employee_repository.save(employee)

            self._unit_of_work.flush()

        # ------------------------------------------------------------------
        # Response
        # ------------------------------------------------------------------

        return LinkEmployeeToUserResponse(
            employee_id=employee.id,
            employee_number=employee.employee_number,
            user_id=user.id,
            profile_id=profile.id,
            display_name=profile.display_name,
            preferred_name=profile.preferred_name,
            updated_at=employee.updated_at,
        )

    @staticmethod
    def _validation_result(
        field: str,
        message: str,
    ):
        """
        Build a ValidationResult for a single validation error.
        """

        from qwos.application.common.results.validation_error import (
            ValidationError,
        )
        from qwos.application.common.results.validation_result import (
            ValidationResult,
        )

        return ValidationResult(
            errors=[
                ValidationError(
                    field=field,
                    message=message,
                )
            ]
        )
