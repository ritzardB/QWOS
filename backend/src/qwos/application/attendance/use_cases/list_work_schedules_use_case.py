"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    list_work_schedules_use_case.py

Description:
    Lists work schedules for the current tenant.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.attendance.responses.list_work_schedules_response import (
    ListWorkSchedulesResponse,
    WorkScheduleListItem,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.domains.attendance.repositories.work_schedule_repository import (
    WorkScheduleRepository,
)


class ListWorkSchedulesUseCase:
    """
    Use case for listing work schedules.
    """

    def __init__(
        self,
        *,
        work_schedule_repository: WorkScheduleRepository,
        request_context: RequestContext,
    ) -> None:
        self._work_schedule_repository = work_schedule_repository
        self._request_context = request_context

    async def execute(self) -> ListWorkSchedulesResponse:
        """
        List all work schedules for the current tenant.
        """

        schedules = self._work_schedule_repository.list_by_tenant(
            tenant_id=self._request_context.tenant_id,
        )

        items = [
            WorkScheduleListItem(
                id=schedule.id,
                schedule_code=schedule.schedule_code,
                schedule_name=schedule.schedule_name,
                timezone=schedule.timezone,
                is_active=schedule.is_active,
                created_at=schedule.created_at,
            )
            for schedule in schedules
        ]

        return ListWorkSchedulesResponse(
            items=items,
            total=len(items),
        )