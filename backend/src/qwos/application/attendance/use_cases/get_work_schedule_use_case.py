"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    get_work_schedule_use_case.py

Description:
    Retrieves a work schedule for the current tenant.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.attendance.responses.get_work_schedule_response import (
    GetWorkScheduleResponse,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.domains.attendance.repositories.work_schedule_repository import (
    WorkScheduleRepository,
)


class GetWorkScheduleUseCase:
    """
    Use case for retrieving a work schedule.
    """

    def __init__(
        self,
        *,
        work_schedule_repository: WorkScheduleRepository,
        request_context: RequestContext,
    ) -> None:
        self._work_schedule_repository = work_schedule_repository
        self._request_context = request_context

    async def execute(
        self,
        schedule_id: str,
    ) -> GetWorkScheduleResponse:
        """
        Retrieve a work schedule for the current tenant.
        """

        schedule = self._work_schedule_repository.get_by_id_for_tenant(
            tenant_id=self._request_context.tenant_id,
            schedule_id=schedule_id,
        )

        if schedule is None:
            raise ResourceNotFoundException(
                resource="WorkSchedule",
                identifier=schedule_id,
            )

        return GetWorkScheduleResponse(
            id=schedule.id,
            schedule_code=schedule.schedule_code,
            schedule_name=schedule.schedule_name,
            timezone=schedule.timezone,
            is_active=schedule.is_active,
            created_at=schedule.created_at,
        )
