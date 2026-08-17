"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    employee_position_mapper.py

Description:
    Maps employee position application responses to API responses.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.responses.hr.get_employee_position_response import (
    GetEmployeePositionResponse,
)
from qwos.application.hr.responses.get_employee_position_response import (
    GetEmployeePositionResponse as ApplicationGetEmployeePositionResponse,
)


class EmployeePositionMapper:
    """
    Maps Employee Position application objects to API contracts.
    """

    @staticmethod
    def to_get_response(
        response: ApplicationGetEmployeePositionResponse,
    ) -> GetEmployeePositionResponse:
        """
        Convert an application response into an API response.
        """

        return GetEmployeePositionResponse(
            id=response.id,
            employee_id=response.employee_id,
            job_title=response.job_title,
            organizational_level=response.organizational_level,
            effective_from=response.effective_from,
            effective_to=response.effective_to,
        )