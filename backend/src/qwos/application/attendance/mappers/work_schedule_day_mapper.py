"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    work_schedule_day_mapper.py

Description:
    Maps Work Schedule Day API contracts to application commands
    and application responses to API responses.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.requests.attendance.create_work_schedule_day_request import (
    CreateWorkScheduleDayRequest,
)
from qwos.api.contracts.responses.attendance.create_work_schedule_day_response import (
    CreateWorkScheduleDayResponse,
)
from qwos.api.contracts.responses.attendance.list_work_schedule_days_response import (
    ListWorkScheduleDaysResponse,
    WorkScheduleDayListItem,
)
from qwos.application.attendance.commands.create_work_schedule_day_command import (
    CreateWorkScheduleDayCommand,
)
from qwos.application.attendance.responses.create_work_schedule_day_response import (
    CreateWorkScheduleDayResponse as ApplicationCreateWorkScheduleDayResponse,
)
from qwos.application.attendance.responses.list_work_schedule_days_response import (
    ListWorkScheduleDaysResponse as ApplicationListWorkScheduleDaysResponse,
)
from qwos.application.common.context.request_context import RequestContext


class WorkScheduleDayMapper:
    """
    Maps Work Schedule Day API contracts to application commands
    and application responses to API responses.
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
        Convert a create application response into an API response.
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

    @staticmethod
    def to_list_response(
        response: ApplicationListWorkScheduleDaysResponse,
    ) -> ListWorkScheduleDaysResponse:
        """
        Convert a list application response into an API response.
        """

        return ListWorkScheduleDaysResponse(
            items=[
                WorkScheduleDayListItem(
                    id=item.id,
                    work_schedule_id=item.work_schedule_id,
                    day_of_week=item.day_of_week,
                    day_type=item.day_type,
                    start_time=item.start_time,
                    end_time=item.end_time,
                    break_minutes=item.break_minutes,
                    is_overnight=item.is_overnight,
                    created_at=item.created_at,
                )
                for item in response.items
            ],
            total=response.total,
        )