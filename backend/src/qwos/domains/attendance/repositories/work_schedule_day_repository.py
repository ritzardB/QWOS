"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Work Schedule Day Repository Contract
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from qwos.domains.attendance.models.work_schedule_day import (
    WorkScheduleDay,
)


class WorkScheduleDayRepository(Protocol):
    """
    Contract for WorkScheduleDay persistence.
    """

    # -------------------------------------------------------------------------
    # Base Operations
    # -------------------------------------------------------------------------

    def get_by_id(
        self,
        schedule_day_id: str,
    ) -> WorkScheduleDay | None:
        """
        Retrieve a work schedule day by identifier.
        """
        ...

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        schedule_day_id: str,
    ) -> WorkScheduleDay | None:
        """
        Retrieve a non-deleted work schedule day within a tenant.
        """
        ...

    def save(
        self,
        schedule_day: WorkScheduleDay,
    ) -> None:
        """
        Persist a work schedule day.
        """
        ...

    # -------------------------------------------------------------------------
    # Schedule Queries
    # -------------------------------------------------------------------------

    def get_by_schedule_and_day(
        self,
        *,
        tenant_id: str,
        work_schedule_id: str,
        day_of_week: int,
    ) -> WorkScheduleDay | None:
        """
        Retrieve the configured day for a schedule.
        """
        ...

    def list_by_schedule(
        self,
        *,
        tenant_id: str,
        work_schedule_id: str,
    ) -> list[WorkScheduleDay]:
        """
        Retrieve all non-deleted day rules for a schedule.
        """
        ...

    def exists_by_schedule_and_day(
        self,
        *,
        tenant_id: str,
        work_schedule_id: str,
        day_of_week: int,
    ) -> bool:
        """
        Determine whether a schedule already has a rule
        for the specified day.
        """
        ...
