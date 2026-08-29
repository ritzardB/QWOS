"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    employee_work_schedule_mapper.py

Description:
    Maps Employee Work Schedule API contracts to application commands
    and responses.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.requests.attendance.create_employee_work_schedule_request import (
    CreateEmployeeWorkScheduleRequest,
)
from qwos.api.contracts.responses.attendance.create_employee_work_schedule_response import (
    CreateEmployeeWorkScheduleResponse,
)
from qwos.application.attendance.commands.create_employee_work_schedule_command import (
    CreateEmployeeWorkScheduleCommand,
)
from qwos.application.attendance.responses.create_employee_work_schedule_response import (
    CreateEmployeeWorkScheduleResponse as ApplicationCreateEmployeeWorkScheduleResponse,
)
from qwos.application.common.context.request_context import RequestContext


class EmployeeWorkScheduleMapper:
    """
    Maps Employee Work Schedule API contracts
    to application commands and responses.
    """

    @staticmethod
    def to_create_command(
        *,
        employee_id: str,
        request: CreateEmployeeWorkScheduleRequest,
        request_context: RequestContext,
    ) -> CreateEmployeeWorkScheduleCommand:
        """
        Convert an API request into a
        CreateEmployeeWorkScheduleCommand.
        """

        return CreateEmployeeWorkScheduleCommand(
            tenant_id=request_context.tenant_id,
            employee_id=employee_id,
            work_schedule_id=request.work_schedule_id,
            effective_from=request.effective_from,
            effective_until=request.effective_until,
            is_active=request.is_active,
        )

    @staticmethod
    def to_create_response(
        response: ApplicationCreateEmployeeWorkScheduleResponse,
    ) -> CreateEmployeeWorkScheduleResponse:
        """
        Convert an application response into an API response.
        """

        return CreateEmployeeWorkScheduleResponse(
            id=response.id,
            employee_id=response.employee_id,
            work_schedule_id=response.work_schedule_id,
            effective_from=response.effective_from,
            effective_until=response.effective_until,
            is_active=response.is_active,
            created_at=response.created_at,
        )
