"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    work_schedule_mapper.py

Description:
    Maps Work Schedule application responses to API responses.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.responses.attendance.get_work_schedule_response import (
    GetWorkScheduleResponse,
)
from qwos.api.contracts.responses.attendance.list_work_schedules_response import (
    ListWorkSchedulesResponse,
    WorkScheduleListItem,
)
from qwos.application.attendance.responses.get_work_schedule_response import (
    GetWorkScheduleResponse as ApplicationGetWorkScheduleResponse,
)
from qwos.application.attendance.responses.list_work_schedules_response import (
    ListWorkSchedulesResponse as ApplicationListWorkSchedulesResponse,
)


class WorkScheduleMapper:
    """
    Maps Work Schedule application objects to API contracts.
    """

    @staticmethod
    def to_list_response(
        response: ApplicationListWorkSchedulesResponse,
    ) -> ListWorkSchedulesResponse:
        """
        Convert a list application response into an API response.
        """

        return ListWorkSchedulesResponse(
            items=[
                WorkScheduleListItem(
                    id=item.id,
                    schedule_code=item.schedule_code,
                    schedule_name=item.schedule_name,
                    timezone=item.timezone,
                    is_active=item.is_active,
                    created_at=item.created_at,
                )
                for item in response.items
            ],
            total=response.total,
        )

    @staticmethod
    def to_get_response(
        response: ApplicationGetWorkScheduleResponse,
    ) -> GetWorkScheduleResponse:
        """
        Convert a get application response into an API response.
        """

        return GetWorkScheduleResponse(
            id=response.id,
            schedule_code=response.schedule_code,
            schedule_name=response.schedule_name,
            timezone=response.timezone,
            is_active=response.is_active,
            created_at=response.created_at,
        )