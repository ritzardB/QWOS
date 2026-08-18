from __future__ import annotations

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.forbidden_exception import (
    ForbiddenException,
)
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.application.hr.commands.create_employee_immigration_command import (
    CreateEmployeeImmigrationCommand,
)
from qwos.application.hr.responses.create_employee_immigration_response import (
    CreateEmployeeImmigrationResponse,
)
from qwos.domains.hr.models.employee_immigration import (
    EmployeeImmigration,
)
from qwos.domains.hr.repositories.employee_immigration_repository import (
    EmployeeImmigrationRepository,
)
from qwos.domains.hr.repositories.employee_repository import (
    EmployeeRepository,
)
from qwos.domains.identity.services.authorization_service import (
    AuthorizationService,
)


class CreateEmployeeImmigrationUseCase:
    """
    Use case for creating an employee immigration record.
    """

    REQUIRED_PERMISSION = "HR_IMMIGRATION_CREATE"

    def __init__(
        self,
        *,
        employee_repository: EmployeeRepository,
        employee_immigration_repository: EmployeeImmigrationRepository,
        authorization_service: AuthorizationService,
        id_generator: IdGenerator,
        unit_of_work: UnitOfWork,
        request_context: RequestContext,
    ) -> None:
        self._employee_repository = employee_repository
        self._employee_immigration_repository = (
            employee_immigration_repository
        )
        self._authorization_service = authorization_service
        self._id_generator = id_generator
        self._unit_of_work = unit_of_work
        self._request_context = request_context

    async def execute(
        self,
        command: CreateEmployeeImmigrationCommand,
    ) -> CreateEmployeeImmigrationResponse:
        """
        Create an employee immigration record.
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
                message=(
                    "User is not authorized to create "
                    "employee immigration records."
                ),
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
        # Create record
        # ------------------------------------------------------------------

        immigration = EmployeeImmigration.create(
            id=self._id_generator.generate(),
            tenant_id=tenant_id,
            employee_id=employee.id,
            immigration_type=command.immigration_type,
            status=command.status,
            document_number=command.document_number,
            sponsor_name=command.sponsor_name,
            issuing_authority=command.issuing_authority,
            issue_date=command.issue_date,
            expiry_date=command.expiry_date,
            notes=command.notes,
            created_by=user_id,
        )

        # ------------------------------------------------------------------
        # Persist
        # ------------------------------------------------------------------

        with self._unit_of_work:
            self._employee_immigration_repository.save(
                immigration,
            )
            self._unit_of_work.flush()

        return CreateEmployeeImmigrationResponse(
            id=immigration.id,
            employee_id=immigration.employee_id,
            immigration_type=immigration.immigration_type,
            status=immigration.status,
            document_number=immigration.document_number,
            sponsor_name=immigration.sponsor_name,
            issuing_authority=immigration.issuing_authority,
            issue_date=immigration.issue_date,
            expiry_date=immigration.expiry_date,
            notes=immigration.notes,
        )