"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    list_work_schedule_days_use_case.py

Description:
    Lists the weekly day rules for a work schedule.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.attendance.responses.list_work_schedule_days_response import (
    ListWorkScheduleDaysResponse,
    WorkScheduleDayListItem,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.domains.attendance.repositories.work_schedule_day_repository import (
    WorkScheduleDayRepository,
)
from qwos.domains.attendance.repositories.work_schedule_repository import (
    WorkScheduleRepository,
)


class ListWorkScheduleDaysUseCase:
    """
    Use case for listing the weekly day rules for a work schedule.
    """

    def __init__(
        self,
        *,
        work_schedule_repository: WorkScheduleRepository,
        work_schedule_day_repository: WorkScheduleDayRepository,
        request_context: RequestContext,
    ) -> None:
        self._work_schedule_repository = work_schedule_repository
        self._work_schedule_day_repository = work_schedule_day_repository
        self._request_context = request_context

    async def execute(
        self,
        work_schedule_id: str,
    ) -> ListWorkScheduleDaysResponse:
        """
        List the weekly day rules for a work schedule.
        """

        # ------------------------------------------------------------------
        # Verify work schedule exists within tenant
        # ------------------------------------------------------------------

        work_schedule = (
            self._work_schedule_repository.get_by_id_for_tenant(
                tenant_id=self._request_context.tenant_id,
                schedule_id=work_schedule_id,
            )
        )

        if work_schedule is None:
            raise ResourceNotFoundException(
                resource="WorkSchedule",
                identifier=work_schedule_id,
            )

        # ------------------------------------------------------------------
        # Retrieve schedule days
        # ------------------------------------------------------------------

        schedule_days = (
            self._work_schedule_day_repository.list_by_schedule(
                tenant_id=self._request_context.tenant_id,
                work_schedule_id=work_schedule_id,
            )
        )

        # ------------------------------------------------------------------
        # Map response
        # ------------------------------------------------------------------

        items = [
            WorkScheduleDayListItem(
                id=schedule_day.id,
                work_schedule_id=schedule_day.work_schedule_id,
                day_of_week=schedule_day.day_of_week,
                day_type=schedule_day.day_type,
                start_time=schedule_day.start_time,
                end_time=schedule_day.end_time,
                break_minutes=schedule_day.break_minutes,
                is_overnight=schedule_day.is_overnight,
                created_at=schedule_day.created_at,
            )
            for schedule_day in schedule_days
        ]

        return ListWorkScheduleDaysResponse(
            items=items,
            total=len(items),
        )