"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Attendance Module

File:
    sqlalchemy_attendance_event_repository.py

Description:
    SQLAlchemy implementation of AttendanceEventRepository.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from qwos.core.database.repositories.base_repository import (
    BaseRepository,
)
from qwos.domains.attendance.models.attendance_event import (
    AttendanceEvent,
)
from qwos.domains.attendance.repositories.attendance_event_repository import (
    AttendanceEventRepository,
)


class SQLAlchemyAttendanceEventRepository(
    BaseRepository[AttendanceEvent],
    AttendanceEventRepository,
):
    """
    SQLAlchemy implementation of AttendanceEventRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=AttendanceEvent,
        )

    # -------------------------------------------------------------------------
    # Attendance Event Queries
    # -------------------------------------------------------------------------

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        attendance_event_id: str,
    ) -> AttendanceEvent | None:
        """
        Retrieve a non-deleted attendance event within a tenant.
        """

        stmt = select(AttendanceEvent).where(
            AttendanceEvent.id == attendance_event_id,
            AttendanceEvent.tenant_id == tenant_id,
            AttendanceEvent.deleted_at.is_(None),
        )

        return self._session.scalar(stmt)

    def list_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> list[AttendanceEvent]:
        stmt = (
            select(AttendanceEvent)
            .where(
                AttendanceEvent.tenant_id == tenant_id,
                AttendanceEvent.employee_id == employee_id,
                AttendanceEvent.deleted_at.is_(None),
            )
            .order_by(
                AttendanceEvent.event_at.desc(),
                AttendanceEvent.id.desc(),
            )
        )

        return list(
            self._session.scalars(stmt).all(),
        )

    def list_by_employee_and_date(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        attendance_date: date,
    ) -> list[AttendanceEvent]:
        """
        Retrieve attendance events for an employee on a specific date.
        """

        next_date = attendance_date + timedelta(days=1)

        stmt = (
            select(AttendanceEvent)
            .where(
                AttendanceEvent.tenant_id == tenant_id,
                AttendanceEvent.employee_id == employee_id,
                AttendanceEvent.deleted_at.is_(None),
                AttendanceEvent.event_at >= attendance_date,
                AttendanceEvent.event_at < next_date,
            )
            .order_by(
                AttendanceEvent.event_at.asc(),
                AttendanceEvent.id.asc(),
            )
        )

        return list(
            self._session.scalars(stmt).all(),
        )

    def list_by_record(
        self,
        *,
        tenant_id: str,
        attendance_record_id: str,
    ) -> list[AttendanceEvent]:
        """
        Retrieve all non-deleted events belonging to an attendance record.
        """

        stmt = (
            select(AttendanceEvent)
            .where(
                AttendanceEvent.tenant_id == tenant_id,
                AttendanceEvent.attendance_record_id == attendance_record_id,
                AttendanceEvent.deleted_at.is_(None),
            )
            .order_by(
                AttendanceEvent.event_at.asc(),
            )
        )

        return list(
            self._session.scalars(stmt).all(),
        )

    def list_by_record_ordered(
        self,
        *,
        tenant_id: str,
        attendance_record_id: str,
    ) -> list[AttendanceEvent]:
        """
        Retrieve attendance events for a record in chronological order.
        """

        stmt = (
            select(AttendanceEvent)
            .where(
                AttendanceEvent.tenant_id == tenant_id,
                AttendanceEvent.attendance_record_id == attendance_record_id,
                AttendanceEvent.deleted_at.is_(None),
            )
            .order_by(
                AttendanceEvent.event_at.asc(),
                AttendanceEvent.id.asc(),
            )
        )

        return list(
            self._session.scalars(stmt).all(),
        )

    def get_latest_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> AttendanceEvent | None:
        """
        Retrieve the most recent attendance event for an employee.
        """

        stmt = (
            select(AttendanceEvent)
            .where(
                AttendanceEvent.tenant_id == tenant_id,
                AttendanceEvent.employee_id == employee_id,
                AttendanceEvent.deleted_at.is_(None),
            )
            .order_by(
                AttendanceEvent.event_at.desc(),
                AttendanceEvent.id.desc(),
            )
            .limit(1)
        )

        return self._session.scalar(stmt)

    def get_latest_by_record(
        self,
        *,
        tenant_id: str,
        attendance_record_id: str,
    ) -> AttendanceEvent | None:
        """
        Retrieve the most recent attendance event for an attendance record.
        """

        stmt = (
            select(AttendanceEvent)
            .where(
                AttendanceEvent.tenant_id == tenant_id,
                AttendanceEvent.attendance_record_id == attendance_record_id,
                AttendanceEvent.deleted_at.is_(None),
            )
            .order_by(
                AttendanceEvent.event_at.desc(),
                AttendanceEvent.id.desc(),
            )
            .limit(1)
        )

        return self._session.scalar(stmt)
