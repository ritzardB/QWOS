"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Work Schedule Repository Contract
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from qwos.domains.attendance.models.work_schedule import (
    WorkSchedule,
)


class WorkScheduleRepository(Protocol):
    """
    Contract for WorkSchedule persistence.
    """

    # -------------------------------------------------------------------------
    # Base Operations
    # -------------------------------------------------------------------------

    def get_by_id(
        self,
        schedule_id: str,
    ) -> WorkSchedule | None:
        """
        Retrieve a work schedule by identifier.
        """
        ...

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        schedule_id: str,
    ) -> WorkSchedule | None:
        """
        Retrieve a non-deleted work schedule within a tenant.
        """
        ...

    def save(
        self,
        schedule: WorkSchedule,
    ) -> None:
        """
        Persist a work schedule.
        """
        ...

    # -------------------------------------------------------------------------
    # Tenant Queries
    # -------------------------------------------------------------------------

    def list_by_tenant(
        self,
        *,
        tenant_id: str,
    ) -> list[WorkSchedule]:
        """
        Retrieve all non-deleted work schedules for a tenant.
        """
        ...

    def get_active_by_code(
        self,
        *,
        tenant_id: str,
        schedule_code: str,
    ) -> WorkSchedule | None:
        """
        Retrieve an active work schedule by tenant and schedule code.
        """
        ...

    def exists_by_code(
        self,
        *,
        tenant_id: str,
        schedule_code: str,
    ) -> bool:
        """
        Determine whether a work schedule code already exists
        within a tenant.
        """
        ...
