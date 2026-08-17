from __future__ import annotations

from datetime import date

from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.hr.responses.get_employee_immigration_response import (
    GetEmployeeImmigrationResponse,
)
from qwos.domains.hr.repositories.employee_immigration_repository import (
    EmployeeImmigrationRepository,
)


class GetEmployeeImmigrationUseCase:
    """
    Retrieve the current immigration record for an employee.
    """

    def __init__(
        self,
        *,
        employee_immigration_repository: EmployeeImmigrationRepository,
    ) -> None:
        self._employee_immigration_repository = (
            employee_immigration_repository
        )

    async def execute(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        immigration_type: str,
        as_of_date: date,
    ) -> GetEmployeeImmigrationResponse:
        immigration = (
            self._employee_immigration_repository.get_current_by_employee_id(
                tenant_id=tenant_id,
                employee_id=employee_id,
                immigration_type=immigration_type,
                as_of_date=as_of_date,
            )
        )

        if immigration is None:
            raise ResourceNotFoundException(
                resource="EmployeeImmigration",
                identifier=employee_id,
            )

        return GetEmployeeImmigrationResponse(
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