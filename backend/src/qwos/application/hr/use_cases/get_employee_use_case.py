"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    get_employee_use_case.py

Description:
    Use case for retrieving a single employee.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.hr.responses.get_employee_response import (
    GetEmployeeResponse,
)
from qwos.domains.hr.repositories.employee_repository import (
    EmployeeRepository,
)


class GetEmployeeUseCase:
    """
    Retrieve an employee within the current tenant.
    """

    def __init__(
        self,
        *,
        employee_repository: EmployeeRepository,
    ) -> None:
        self._employee_repository = employee_repository

    async def execute(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> GetEmployeeResponse:
        """
        Retrieve the requested employee.
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

        return GetEmployeeResponse(
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
