from __future__ import annotations

from qwos.application.hr.responses.list_employee_immigration_response import (
    EmployeeImmigrationItem,
    ListEmployeeImmigrationResponse,
)
from qwos.domains.hr.repositories.employee_immigration_repository import (
    EmployeeImmigrationRepository,
)


class ListEmployeeImmigrationUseCase:
    """
    Retrieve immigration history for an employee.
    """

    def __init__(
        self,
        *,
        employee_immigration_repository: EmployeeImmigrationRepository,
    ) -> None:
        self._employee_immigration_repository = employee_immigration_repository

    async def execute(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        immigration_type: str | None = None,
    ) -> ListEmployeeImmigrationResponse:
        records = self._employee_immigration_repository.list_by_employee_id(
            tenant_id=tenant_id,
            employee_id=employee_id,
            immigration_type=immigration_type,
        )

        return ListEmployeeImmigrationResponse(
            items=[
                EmployeeImmigrationItem(
                    id=record.id,
                    employee_id=record.employee_id,
                    immigration_type=record.immigration_type,
                    status=record.status,
                    document_number=record.document_number,
                    sponsor_name=record.sponsor_name,
                    issuing_authority=record.issuing_authority,
                    issue_date=record.issue_date,
                    expiry_date=record.expiry_date,
                    notes=record.notes,
                )
                for record in records
            ],
        )
