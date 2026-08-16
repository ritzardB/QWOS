"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    employee_mapper.py

Description:
    Maps HR API contracts to application commands and responses.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.requests.hr.create_employee_request import (
    CreateEmployeeRequest,
)
from qwos.api.contracts.responses.hr.create_employee_response import (
    CreateEmployeeResponse,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.hr.commands.create_employee_command import (
    CreateEmployeeCommand,
)
from qwos.application.hr.responses.create_employee_response import (
    CreateEmployeeResponse as ApplicationCreateEmployeeResponse,
)


class EmployeeMapper:
    """
    Maps between HR API contracts and application objects.
    """

    @staticmethod
    def to_create_command(
        *,
        request: CreateEmployeeRequest,
        request_context: RequestContext,
    ) -> CreateEmployeeCommand:
        """
        Convert an API request into a CreateEmployeeCommand.
        """

        return CreateEmployeeCommand(
            tenant_id=request_context.tenant_id,
            user_id=request.user_id,
            hire_date=request.hire_date,
            employment_status=request.employment_status,
            employment_type=request.employment_type,
            work_email=request.work_email,
            work_phone=request.work_phone,
        )

    @staticmethod
    def to_create_response(
        response: ApplicationCreateEmployeeResponse,
    ) -> CreateEmployeeResponse:
        """
        Convert an application response into an API response.
        """

        return CreateEmployeeResponse(
            id=response.id,
            employee_number=response.employee_number,
            user_id=response.user_id,
            hire_date=response.hire_date,
            employment_status=response.employment_status,
            employment_type=response.employment_type,
            work_email=response.work_email,
            work_phone=response.work_phone,
            created_at=response.created_at,
        )