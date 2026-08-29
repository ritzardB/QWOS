"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Attendance Module

File:
    sqlalchemy_employee_work_arrangement_repository.py

Description:
    SQLAlchemy implementation of EmployeeWorkArrangementRepository.

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
from qwos.domains.attendance.models.employee_work_arrangement import (
    EmployeeWorkArrangement,
)
from qwos.domains.attendance.repositories.employee_work_arrangement_repository import (
    EmployeeWorkArrangementRepository,
)


class SQLAlchemyEmployeeWorkArrangementRepository(
    BaseRepository[EmployeeWorkArrangement],
    EmployeeWorkArrangementRepository,
):
    """
    SQLAlchemy implementation of EmployeeWorkArrangementRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=EmployeeWorkArrangement,
        )

    # -------------------------------------------------------------------------
    # Tenant Queries
    # -------------------------------------------------------------------------

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        arrangement_id: str,
    ) -> EmployeeWorkArrangement | None:
        """
        Retrieve a non-deleted work arrangement within a tenant.
        """

        stmt = select(EmployeeWorkArrangement).where(
            EmployeeWorkArrangement.id == arrangement_id,
            EmployeeWorkArrangement.tenant_id == tenant_id,
            EmployeeWorkArrangement.deleted_at.is_(None),
        )

        return self._session.scalar(stmt)

    # -------------------------------------------------------------------------
    # Employee Queries
    # -------------------------------------------------------------------------

    def get_by_employee_and_date(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> EmployeeWorkArrangement | None:
        """
        Retrieve the work arrangement effective for an employee on a date.

        The arrangement must have started on or before the requested date
        and must not have ended before that date.
        """

        stmt = (
            select(EmployeeWorkArrangement)
            .where(
                EmployeeWorkArrangement.tenant_id == tenant_id,
                EmployeeWorkArrangement.employee_id == employee_id,
                EmployeeWorkArrangement.effective_from <= effective_date,
                (
                    EmployeeWorkArrangement.effective_until.is_(None)
                    | (EmployeeWorkArrangement.effective_until >= effective_date)
                ),
                EmployeeWorkArrangement.deleted_at.is_(None),
            )
            .order_by(
                EmployeeWorkArrangement.effective_from.desc(),
            )
            .limit(1)
        )

        return self._session.scalar(stmt)

    def list_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> list[EmployeeWorkArrangement]:
        """
        Retrieve all non-deleted work arrangements for an employee.
        """

        stmt = (
            select(EmployeeWorkArrangement)
            .where(
                EmployeeWorkArrangement.tenant_id == tenant_id,
                EmployeeWorkArrangement.employee_id == employee_id,
                EmployeeWorkArrangement.deleted_at.is_(None),
            )
            .order_by(
                EmployeeWorkArrangement.effective_from.desc(),
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
    ) -> EmployeeWorkArrangement | None:
        """
        Retrieve the currently active work arrangement for an employee.
        """

        stmt = (
            select(EmployeeWorkArrangement)
            .where(
                EmployeeWorkArrangement.tenant_id == tenant_id,
                EmployeeWorkArrangement.employee_id == employee_id,
                EmployeeWorkArrangement.is_active.is_(True),
                EmployeeWorkArrangement.deleted_at.is_(None),
            )
            .order_by(
                EmployeeWorkArrangement.effective_from.desc(),
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
        Determine whether an arrangement already starts on a given date.
        """

        stmt = select(EmployeeWorkArrangement.id).where(
            EmployeeWorkArrangement.tenant_id == tenant_id,
            EmployeeWorkArrangement.employee_id == employee_id,
            EmployeeWorkArrangement.effective_from == effective_from,
            EmployeeWorkArrangement.deleted_at.is_(None),
        )

        return self._session.scalar(stmt) is not None
