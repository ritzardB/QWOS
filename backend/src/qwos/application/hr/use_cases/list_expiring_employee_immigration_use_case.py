from __future__ import annotations

from datetime import date, timedelta

from qwos.application.hr.responses.list_expiring_employee_immigration_response import (
    ExpiringEmployeeImmigrationItem,
    ListExpiringEmployeeImmigrationResponse,
)
from qwos.domains.hr.repositories.employee_immigration_repository import (
    EmployeeImmigrationRepository,
)


class ListExpiringEmployeeImmigrationUseCase:
    """
    Retrieve immigration records expiring within a defined window.
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
        as_of_date: date,
        days: int,
        immigration_type: str | None = None,
    ) -> ListExpiringEmployeeImmigrationResponse:
        if days < 1:
            raise ValueError("days must be greater than zero")

        end_date = as_of_date + timedelta(days=days)

        records = self._employee_immigration_repository.list_expiring_between(
            tenant_id=tenant_id,
            start_date=as_of_date,
            end_date=end_date,
            immigration_type=immigration_type,
        )

        return ListExpiringEmployeeImmigrationResponse(
            items=[
                ExpiringEmployeeImmigrationItem(
                    id=record.id,
                    employee_id=record.employee_id,
                    immigration_type=record.immigration_type,
                    status=record.status,
                    document_number=record.document_number,
                    issue_date=record.issue_date,
                    expiry_date=record.expiry_date,
                    days_until_expiry=(record.expiry_date - as_of_date).days,
                )
                for record in records
                if record.expiry_date is not None
            ],
        )
