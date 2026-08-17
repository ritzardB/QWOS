from __future__ import annotations

from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.hr.responses.get_employee_manager_response import (
    GetEmployeeManagerResponse,
)
from qwos.domains.hr.repositories.employee_reporting_relationship_repository import (
    EmployeeReportingRelationshipRepository,
)
from qwos.domains.hr.repositories.employee_repository import (
    EmployeeRepository,
)


class GetEmployeeManagerUseCase:
    """
    Retrieve an employee's active primary manager.
    """

    def __init__(
        self,
        *,
        employee_repository: EmployeeRepository,
        relationship_repository: (
            EmployeeReportingRelationshipRepository
        ),
    ) -> None:
        self._employee_repository = employee_repository
        self._relationship_repository = relationship_repository

    async def execute(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> GetEmployeeManagerResponse:
        """
        Retrieve the employee's current primary manager.
        """

        employee = self._employee_repository.get_by_id_for_tenant(
            tenant_id=tenant_id,
            employee_id=employee_id,
        )

        if employee is None:
            raise ResourceNotFoundException(
                resource="Employee",
                identifier=employee_id,
            )

        relationship = (
            self._relationship_repository.get_active_primary_manager(
                tenant_id=tenant_id,
                employee_id=employee_id,
            )
        )

        if relationship is None:
            return GetEmployeeManagerResponse(
                employee_id=employee.id,
                manager_employee_id=None,
                manager_employee_number=None,
                relationship_type=None,
                effective_from=None,
            )

        manager = self._employee_repository.get_by_id_for_tenant(
            tenant_id=tenant_id,
            employee_id=relationship.manager_employee_id,
        )

        if manager is None:
            raise ResourceNotFoundException(
                resource="Manager",
                identifier=relationship.manager_employee_id,
            )

        return GetEmployeeManagerResponse(
            employee_id=employee.id,
            manager_employee_id=manager.id,
            manager_employee_number=manager.employee_number,
            relationship_type=relationship.relationship_type,
            effective_from=relationship.effective_from,
        )