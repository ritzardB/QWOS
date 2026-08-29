"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Attendance Module

File:
    sqlalchemy_employee_work_schedule_repository.py

Description:
    SQLAlchemy implementation of EmployeeWorkScheduleRepository.

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
from qwos.domains.attendance.models.employee_work_schedule import (
    EmployeeWorkSchedule,
)
from qwos.domains.attendance.repositories.employee_work_schedule_repository import (
    EmployeeWorkScheduleRepository,
)


class SQLAlchemyEmployeeWorkScheduleRepository(
    BaseRepository[EmployeeWorkSchedule],
    EmployeeWorkScheduleRepository,
):
    """
    SQLAlchemy implementation of EmployeeWorkScheduleRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=EmployeeWorkSchedule,
        )

    # -------------------------------------------------------------------------
    # Tenant Queries
    # -------------------------------------------------------------------------

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        assignment_id: str,
    ) -> EmployeeWorkSchedule | None:
        """
        Retrieve a non-deleted assignment within a tenant.
        """

        stmt = select(EmployeeWorkSchedule).where(
            EmployeeWorkSchedule.id == assignment_id,
            EmployeeWorkSchedule.tenant_id == tenant_id,
            EmployeeWorkSchedule.deleted_at.is_(None),
        )

        return self._session.scalar(stmt)

    # -------------------------------------------------------------------------
    # Employee Queries
    # -------------------------------------------------------------------------

    def get_effective_for_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> EmployeeWorkSchedule | None:
        """
        Retrieve the work schedule assignment effective for an employee
        on a specific date.

        The assignment must have started on or before the requested date
        and must not have ended before that date.
        """

        stmt = (
            select(EmployeeWorkSchedule)
            .where(
                EmployeeWorkSchedule.tenant_id == tenant_id,
                EmployeeWorkSchedule.employee_id == employee_id,
                EmployeeWorkSchedule.effective_from <= effective_date,
                (
                    EmployeeWorkSchedule.effective_until.is_(None)
                    | (EmployeeWorkSchedule.effective_until >= effective_date)
                ),
                EmployeeWorkSchedule.deleted_at.is_(None),
            )
            .order_by(
                EmployeeWorkSchedule.effective_from.desc(),
            )
            .limit(1)
        )

        return self._session.scalar(stmt)

    def list_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> list[EmployeeWorkSchedule]:
        """
        Retrieve all non-deleted assignments for an employee.
        """

        stmt = (
            select(EmployeeWorkSchedule)
            .where(
                EmployeeWorkSchedule.tenant_id == tenant_id,
                EmployeeWorkSchedule.employee_id == employee_id,
                EmployeeWorkSchedule.deleted_at.is_(None),
            )
            .order_by(
                EmployeeWorkSchedule.effective_from.desc(),
            )
        )

        return list(
            self._session.scalars(stmt).all(),
        )

    def get_active_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> EmployeeWorkSchedule | None:
        """
        Retrieve the currently active work schedule assignment.
        """

        stmt = (
            select(EmployeeWorkSchedule)
            .where(
                EmployeeWorkSchedule.tenant_id == tenant_id,
                EmployeeWorkSchedule.employee_id == employee_id,
                EmployeeWorkSchedule.is_active.is_(True),
                EmployeeWorkSchedule.deleted_at.is_(None),
            )
            .order_by(
                EmployeeWorkSchedule.effective_from.desc(),
            )
            .limit(1)
        )

        return self._session.scalar(stmt)

    def exists_by_employee_and_start_date(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_from: date,
    ) -> bool:
        """
        Determine whether an assignment already starts on a given date.
        """

        stmt = select(EmployeeWorkSchedule.id).where(
            EmployeeWorkSchedule.tenant_id == tenant_id,
            EmployeeWorkSchedule.employee_id == employee_id,
            EmployeeWorkSchedule.effective_from == effective_from,
            EmployeeWorkSchedule.deleted_at.is_(None),
        )

        return self._session.scalar(stmt) is not None
