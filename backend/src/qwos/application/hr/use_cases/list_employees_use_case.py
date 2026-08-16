from __future__ import annotations

from qwos.application.common.context.request_context import RequestContext
from qwos.application.hr.responses.list_employees_response import (
    EmployeeSummaryResponse,
    ListEmployeesResponse,
)
from qwos.domains.hr.repositories.employee_repository import (
    EmployeeRepository,
)


class ListEmployeesUseCase:
    """
    Retrieve active employees for the current tenant.
    """

    def __init__(
        self,
        *,
        employee_repository: EmployeeRepository,
        request_context: RequestContext,
    ) -> None:
        self._employee_repository = employee_repository
        self._request_context = request_context

    async def execute(self) -> ListEmployeesResponse:
        employees = self._employee_repository.list_active(
            tenant_id=self._request_context.tenant_id,
        )

        return ListEmployeesResponse(
            employees=[
                EmployeeSummaryResponse(
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
                for employee in employees
            ]
        )