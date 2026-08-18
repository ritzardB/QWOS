from __future__ import annotations

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.forbidden_exception import (
    ForbiddenException,
)
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.hr.commands.update_employee_profile_command import (
    UpdateEmployeeProfileCommand,
)
from qwos.application.hr.responses.update_employee_profile_response import (
    UpdateEmployeeProfileResponse,
)
from qwos.domains.hr.repositories.employee_profile_repository import (
    EmployeeProfileRepository,
)
from qwos.domains.hr.repositories.employee_repository import (
    EmployeeRepository,
)
from qwos.domains.identity.services.authorization_service import (
    AuthorizationService,
)


class UpdateEmployeeProfileUseCase:
    """
    Use case for updating an employee profile.
    """

    REQUIRED_PERMISSION = "HR_PROFILE_UPDATE"

    def __init__(
        self,
        *,
        employee_repository: EmployeeRepository,
        employee_profile_repository: EmployeeProfileRepository,
        authorization_service: AuthorizationService,
        unit_of_work: UnitOfWork,
        request_context: RequestContext,
    ) -> None:
        self._employee_repository = employee_repository
        self._employee_profile_repository = (
            employee_profile_repository
        )
        self._authorization_service = authorization_service
        self._unit_of_work = unit_of_work
        self._request_context = request_context

    async def execute(
        self,
        command: UpdateEmployeeProfileCommand,
    ) -> UpdateEmployeeProfileResponse:
        """
        Update the core HR profile for an employee.
        """

        tenant_id = self._request_context.tenant_id
        user_id = self._request_context.user_id

        # ------------------------------------------------------------------
        # Authorization
        # ------------------------------------------------------------------

        allowed = await self._authorization_service.has_permission(
            tenant_id=tenant_id,
            user_id=user_id,
            permission_code=self.REQUIRED_PERMISSION,
        )

        if not allowed:
            raise ForbiddenException(
                message="User is not authorized to update employee profiles."
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

        if employee.tenant_id != tenant_id:
            raise ResourceNotFoundException(
                resource="Employee",
                identifier=command.employee_id,
            )

        # ------------------------------------------------------------------
        # Locate profile
        # ------------------------------------------------------------------

        profile = (
            self._employee_profile_repository.get_by_employee_id(
                tenant_id=tenant_id,
                employee_id=command.employee_id,
            )
        )

        if profile is None:
            raise ResourceNotFoundException(
                resource="EmployeeProfile",
                identifier=command.employee_id,
            )

        # ------------------------------------------------------------------
        # Update aggregate
        # ------------------------------------------------------------------

        profile.update(
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
            emergency_contact_name=(
                command.emergency_contact_name
            ),
            emergency_contact_relationship=(
                command.emergency_contact_relationship
            ),
            emergency_contact_phone=(
                command.emergency_contact_phone
            ),
            updated_by=user_id,
        )

        # ------------------------------------------------------------------
        # Persist
        # ------------------------------------------------------------------

        with self._unit_of_work:
            self._employee_profile_repository.save(profile)
            self._unit_of_work.flush()

        # ------------------------------------------------------------------
        # Response
        # ------------------------------------------------------------------

        return UpdateEmployeeProfileResponse(
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
            emergency_contact_name=(
                profile.emergency_contact_name
            ),
            emergency_contact_relationship=(
                profile.emergency_contact_relationship
            ),
            emergency_contact_phone=(
                profile.emergency_contact_phone
            ),
            created_at=profile.created_at,
        )