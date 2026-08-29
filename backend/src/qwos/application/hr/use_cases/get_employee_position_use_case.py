"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    get_employee_position_use_case.py

Description:
    Use case for retrieving an employee's current organizational position.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.hr.responses.get_employee_position_response import (
    GetEmployeePositionResponse,
)
from qwos.domains.hr.repositories.employee_position_repository import (
    EmployeePositionRepository,
)


class GetEmployeePositionUseCase:
    """
    Retrieve an employee's current organizational position.
    """

    def __init__(
        self,
        *,
        employee_position_repository: EmployeePositionRepository,
    ) -> None:
        self._employee_position_repository = employee_position_repository

    async def execute(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> GetEmployeePositionResponse:
        """
        Retrieve the employee's current position.
        """

        position = self._employee_position_repository.get_current_by_employee_id(
            tenant_id=tenant_id,
            employee_id=employee_id,
        )

        if position is None:
            raise ResourceNotFoundException(
                resource="EmployeePosition",
                identifier=employee_id,
            )

        return GetEmployeePositionResponse(
            id=position.id,
            employee_id=position.employee_id,
            job_title=position.job_title,
            organizational_level=position.organizational_level,
            effective_from=position.effective_from,
            effective_to=position.effective_to,
        )
