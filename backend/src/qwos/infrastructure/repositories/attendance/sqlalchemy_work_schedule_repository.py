"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Attendance Module

File:
    sqlalchemy_work_schedule_repository.py

Description:
    SQLAlchemy implementation of WorkScheduleRepository.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from qwos.core.database.repositories.base_repository import (
    BaseRepository,
)
from qwos.domains.attendance.models.work_schedule import (
    WorkSchedule,
)
from qwos.domains.attendance.repositories.work_schedule_repository import (
    WorkScheduleRepository,
)


class SQLAlchemyWorkScheduleRepository(
    BaseRepository[WorkSchedule],
    WorkScheduleRepository,
):
    """
    SQLAlchemy implementation of WorkScheduleRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=WorkSchedule,
        )

    # -------------------------------------------------------------------------
    # Tenant Queries
    # -------------------------------------------------------------------------

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        schedule_id: str,
    ) -> WorkSchedule | None:
        """
        Retrieve a non-deleted work schedule within a tenant.
        """

        stmt = select(WorkSchedule).where(
            WorkSchedule.id == schedule_id,
            WorkSchedule.tenant_id == tenant_id,
            WorkSchedule.deleted_at.is_(None),
        )

        return self._session.scalar(stmt)

    def list_by_tenant(
        self,
        *,
        tenant_id: str,
    ) -> list[WorkSchedule]:
        """
        Retrieve all non-deleted work schedules for a tenant.
        """

        stmt = (
            select(WorkSchedule)
            .where(
                WorkSchedule.tenant_id == tenant_id,
                WorkSchedule.deleted_at.is_(None),
            )
            .order_by(
                WorkSchedule.schedule_code.asc(),
            )
        )

        return list(
            self._session.scalars(stmt).all(),
        )

    def get_active_by_code(
        self,
        *,
        tenant_id: str,
        schedule_code: str,
    ) -> WorkSchedule | None:
        """
        Retrieve an active work schedule by tenant and schedule code.
        """

        normalized_code = schedule_code.strip().lower()

        stmt = (
            select(WorkSchedule)
            .where(
                WorkSchedule.tenant_id == tenant_id,
                WorkSchedule.schedule_code == normalized_code,
                WorkSchedule.is_active.is_(True),
                WorkSchedule.deleted_at.is_(None),
            )
            .limit(1)
        )

        return self._session.scalar(stmt)

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

        normalized_code = schedule_code.strip().lower()

        stmt = select(WorkSchedule.id).where(
            WorkSchedule.tenant_id == tenant_id,
            WorkSchedule.schedule_code == normalized_code,
            WorkSchedule.deleted_at.is_(None),
        )

        return self._session.scalar(stmt) is not None