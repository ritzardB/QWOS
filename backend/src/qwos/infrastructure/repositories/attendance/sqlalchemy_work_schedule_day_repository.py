"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Attendance Module

File:
    sqlalchemy_work_schedule_day_repository.py

Description:
    SQLAlchemy implementation of WorkScheduleDayRepository.

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
from qwos.domains.attendance.models.work_schedule_day import (
    WorkScheduleDay,
)
from qwos.domains.attendance.repositories.work_schedule_day_repository import (
    WorkScheduleDayRepository,
)


class SQLAlchemyWorkScheduleDayRepository(
    BaseRepository[WorkScheduleDay],
    WorkScheduleDayRepository,
):
    """
    SQLAlchemy implementation of WorkScheduleDayRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=WorkScheduleDay,
        )

    # -------------------------------------------------------------------------
    # Tenant Queries
    # -------------------------------------------------------------------------

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        schedule_day_id: str,
    ) -> WorkScheduleDay | None:
        """
        Retrieve a non-deleted schedule day within a tenant.
        """

        stmt = select(WorkScheduleDay).where(
            WorkScheduleDay.id == schedule_day_id,
            WorkScheduleDay.tenant_id == tenant_id,
            WorkScheduleDay.deleted_at.is_(None),
        )

        return self._session.scalar(stmt)

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

        stmt = select(WorkScheduleDay).where(
            WorkScheduleDay.tenant_id == tenant_id,
            WorkScheduleDay.work_schedule_id == work_schedule_id,
            WorkScheduleDay.day_of_week == day_of_week,
            WorkScheduleDay.deleted_at.is_(None),
        )

        return self._session.scalar(stmt)

    def list_by_schedule(
        self,
        *,
        tenant_id: str,
        work_schedule_id: str,
    ) -> list[WorkScheduleDay]:
        """
        Retrieve all non-deleted day rules for a schedule.

        Results are ordered Monday through Sunday.
        """

        stmt = (
            select(WorkScheduleDay)
            .where(
                WorkScheduleDay.tenant_id == tenant_id,
                WorkScheduleDay.work_schedule_id == work_schedule_id,
                WorkScheduleDay.deleted_at.is_(None),
            )
            .order_by(
                WorkScheduleDay.day_of_week.asc(),
            )
        )

        return list(
            self._session.scalars(stmt).all(),
        )

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

        stmt = select(WorkScheduleDay.id).where(
            WorkScheduleDay.tenant_id == tenant_id,
            WorkScheduleDay.work_schedule_id == work_schedule_id,
            WorkScheduleDay.day_of_week == day_of_week,
            WorkScheduleDay.deleted_at.is_(None),
        )

        return self._session.scalar(stmt) is not None
