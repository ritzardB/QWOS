"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Attendance Module

File:
    sqlalchemy_attendance_record_repository.py

Description:
    SQLAlchemy implementation of AttendanceRecordRepository.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from qwos.core.database.repositories.base_repository import (
    BaseRepository,
)
from qwos.domains.attendance.models.attendance_record import (
    AttendanceRecord,
)
from qwos.domains.attendance.repositories.attendance_record_repository import (
    AttendanceRecordRepository,
)


class SQLAlchemyAttendanceRecordRepository(
    BaseRepository[AttendanceRecord],
    AttendanceRecordRepository,
):
    """
    SQLAlchemy implementation of AttendanceRecordRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=AttendanceRecord,
        )

    # -------------------------------------------------------------------------
    # Attendance Queries
    # -------------------------------------------------------------------------

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        attendance_record_id: str,
    ) -> AttendanceRecord | None:
        """
        Retrieve a non-deleted attendance record within a tenant.
        """

        stmt = select(AttendanceRecord).where(
            AttendanceRecord.id == attendance_record_id,
            AttendanceRecord.tenant_id == tenant_id,
            AttendanceRecord.deleted_at.is_(None),
        )

        return self._session.scalar(stmt)

    def get_by_employee_and_date(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        attendance_date: date,
    ) -> AttendanceRecord | None:
        """
        Retrieve an employee attendance record for a specific date.
        """

        stmt = select(AttendanceRecord).where(
            AttendanceRecord.tenant_id == tenant_id,
            AttendanceRecord.employee_id == employee_id,
            AttendanceRecord.attendance_date == attendance_date,
            AttendanceRecord.deleted_at.is_(None),
        )

        return self._session.scalar(stmt)

    def list_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> list[AttendanceRecord]:
        """
        Retrieve non-deleted attendance records for an employee.
        """

        stmt = (
            select(AttendanceRecord)
            .where(
                AttendanceRecord.tenant_id == tenant_id,
                AttendanceRecord.employee_id == employee_id,
                AttendanceRecord.deleted_at.is_(None),
            )
            .order_by(
                AttendanceRecord.attendance_date.desc(),
            )
        )

        return list(
            self._session.scalars(stmt).all(),
        )

    def list_by_employee_and_period(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        pay_period_id: str,
    ) -> list[AttendanceRecord]:
        """
        Retrieve attendance records for an employee within a pay period.
        """

        stmt = (
            select(AttendanceRecord)
            .where(
                AttendanceRecord.tenant_id == tenant_id,
                AttendanceRecord.employee_id == employee_id,
                AttendanceRecord.pay_period_id == pay_period_id,
                AttendanceRecord.deleted_at.is_(None),
            )
            .order_by(
                AttendanceRecord.attendance_date.asc(),
            )
        )

        return list(
            self._session.scalars(stmt).all(),
        )

    def list_by_date(
        self,
        *,
        tenant_id: str,
        attendance_date: date,
    ) -> list[AttendanceRecord]:
        """
        Retrieve non-deleted attendance records for a tenant on a date.
        """

        stmt = (
            select(AttendanceRecord)
            .where(
                AttendanceRecord.tenant_id == tenant_id,
                AttendanceRecord.attendance_date == attendance_date,
                AttendanceRecord.deleted_at.is_(None),
            )
            .order_by(
                AttendanceRecord.employee_id.asc(),
            )
        )

        return list(
            self._session.scalars(stmt).all(),
        )
