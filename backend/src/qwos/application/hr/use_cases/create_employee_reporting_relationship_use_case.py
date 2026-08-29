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
from qwos.application.hr.commands.create_employee_reporting_relationship_command import (
    CreateEmployeeReportingRelationshipCommand,
)
from qwos.application.hr.responses.create_employee_reporting_relationship_response import (
    CreateEmployeeReportingRelationshipResponse,
)
from qwos.application.hr.validators.create_employee_reporting_relationship_validator import (
    CreateEmployeeReportingRelationshipValidator,
)
from qwos.domains.hr.models.employee_reporting_relationship import (
    EmployeeReportingRelationship,
)
from qwos.domains.hr.repositories.employee_reporting_relationship_repository import (
    EmployeeReportingRelationshipRepository,
)
from qwos.domains.hr.repositories.employee_repository import (
    EmployeeRepository,
)


class CreateEmployeeReportingRelationshipUseCase:
    """
    Create an employee reporting relationship.
    """

    def __init__(
        self,
        *,
        employee_repository: EmployeeRepository,
        relationship_repository: (EmployeeReportingRelationshipRepository),
        id_generator: IdGenerator,
        unit_of_work: UnitOfWork,
        validator: CreateEmployeeReportingRelationshipValidator,
        request_context: RequestContext,
    ) -> None:
        self._employee_repository = employee_repository
        self._relationship_repository = relationship_repository
        self._id_generator = id_generator
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._request_context = request_context

    async def execute(
        self,
        command: CreateEmployeeReportingRelationshipCommand,
    ) -> CreateEmployeeReportingRelationshipResponse:
        validation = self._validator.validate(command)

        if validation.errors:
            raise ValidationException(validation)

        employee = self._employee_repository.get_by_id(
            command.employee_id,
        )

        if employee is None:
            raise ResourceNotFoundException(
                resource="Employee",
                identifier=command.employee_id,
            )

        manager = self._employee_repository.get_by_id(
            command.manager_employee_id,
        )

        if manager is None:
            raise ResourceNotFoundException(
                resource="Employee",
                identifier=command.manager_employee_id,
            )

        if employee.tenant_id != command.tenant_id:
            raise ValueError("Employee does not belong to the requested tenant.")

        if manager.tenant_id != command.tenant_id:
            raise ValueError("Manager does not belong to the requested tenant.")

        if command.is_primary and command.relationship_type == "primary_manager":
            if self._relationship_repository.exists_active_primary_manager(
                tenant_id=command.tenant_id,
                employee_id=command.employee_id,
            ):
                raise DuplicateResourceException(
                    resource="EmployeeReportingRelationship",
                    field="employee_id",
                    value=command.employee_id,
                )

        relationship = EmployeeReportingRelationship.create(
            id=self._id_generator.generate(),
            tenant_id=command.tenant_id,
            employee_id=command.employee_id,
            manager_employee_id=command.manager_employee_id,
            relationship_type=command.relationship_type,
            effective_from=command.effective_from,
            effective_to=command.effective_to,
            is_primary=command.is_primary,
            created_by=self._request_context.user_id,
        )

        with self._unit_of_work:
            self._relationship_repository.save(relationship)
            self._unit_of_work.flush()

        return CreateEmployeeReportingRelationshipResponse(
            id=relationship.id,
            employee_id=relationship.employee_id,
            manager_employee_id=relationship.manager_employee_id,
            relationship_type=relationship.relationship_type,
            effective_from=relationship.effective_from,
            effective_to=relationship.effective_to,
            is_primary=relationship.is_primary,
            created_at=relationship.created_at,
        )
