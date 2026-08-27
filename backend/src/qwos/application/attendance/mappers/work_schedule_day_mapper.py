"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    work_schedule_day_mapper.py

Description:
    Maps Work Schedule Day API contracts to application commands
    and responses.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.responses.attendance.create_work_schedule_day_response import (
    CreateWorkScheduleDayResponse,
)

from qwos.api.contracts.requests.attendance.create_work_schedule_day_request import (
    CreateWorkScheduleDayRequest,
)
from qwos.application.attendance.commands.create_work_schedule_day_command import (
    CreateWorkScheduleDayCommand,
)
from qwos.application.attendance.responses.create_work_schedule_day_response import (
    CreateWorkScheduleDayResponse as ApplicationCreateWorkScheduleDayResponse,
)
from qwos.application.common.context.request_context import RequestContext


class WorkScheduleDayMapper:
    """
    Maps Work Schedule Day API contracts
    to application commands and responses.
    """

    @staticmethod
    def to_create_command(
        *,
        work_schedule_id: str,
        request: CreateWorkScheduleDayRequest,
        request_context: RequestContext,
    ) -> CreateWorkScheduleDayCommand:
        """
        Convert an API request into a CreateWorkScheduleDayCommand.
        """

        return CreateWorkScheduleDayCommand(
            tenant_id=request_context.tenant_id,
            work_schedule_id=work_schedule_id,
            day_of_week=request.day_of_week,
            day_type=request.day_type,
            start_time=request.start_time,
            end_time=request.end_time,
            break_minutes=request.break_minutes,
            is_overnight=request.is_overnight,
        )

    @staticmethod
    def to_create_response(
        response: ApplicationCreateWorkScheduleDayResponse,
    ) -> CreateWorkScheduleDayResponse:
        """
        Convert an application response into an API response.
        """

        return CreateWorkScheduleDayResponse(
            id=response.id,
            work_schedule_id=response.work_schedule_id,
            day_of_week=response.day_of_week,
            day_type=response.day_type,
            start_time=response.start_time,
            end_time=response.end_time,
            break_minutes=response.break_minutes,
            is_overnight=response.is_overnight,
            created_at=response.created_at,
        )