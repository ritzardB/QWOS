"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Attendance Module

File:
    sqlalchemy_employee_attendance_policy_repository.py

Description:
    SQLAlchemy implementation of EmployeeAttendancePolicyRepository.

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
from qwos.domains.attendance.models.employee_attendance_policy import (
    EmployeeAttendancePolicy,
)
from qwos.domains.attendance.repositories.employee_attendance_policy_repository import (
    EmployeeAttendancePolicyRepository,
)


class SQLAlchemyEmployeeAttendancePolicyRepository(
    BaseRepository[EmployeeAttendancePolicy],
    EmployeeAttendancePolicyRepository,
):
    """
    SQLAlchemy implementation of EmployeeAttendancePolicyRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=EmployeeAttendancePolicy,
        )

    # -------------------------------------------------------------------------
    # Base Operations
    # -------------------------------------------------------------------------

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        employee_attendance_policy_id: str,
    ) -> EmployeeAttendancePolicy | None:
        """
        Retrieve a non-deleted employee attendance policy assignment
        within a tenant.
        """

        stmt = select(EmployeeAttendancePolicy).where(
            EmployeeAttendancePolicy.id
            == employee_attendance_policy_id,
            EmployeeAttendancePolicy.tenant_id
            == tenant_id,
            EmployeeAttendancePolicy.deleted_at.is_(None),
        )

        return self._session.scalar(stmt)

    # -------------------------------------------------------------------------
    # Effective Policy
    # -------------------------------------------------------------------------

    def get_effective_policy(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> EmployeeAttendancePolicy | None:
        """
        Retrieve the attendance policy assignment effective for an employee
        on a specific date.
        """

        stmt = (
            select(EmployeeAttendancePolicy)
            .where(
                EmployeeAttendancePolicy.tenant_id
                == tenant_id,
                EmployeeAttendancePolicy.employee_id
                == employee_id,
                EmployeeAttendancePolicy.effective_from
                <= effective_date,
                (
                    EmployeeAttendancePolicy.effective_until.is_(None)
                    | (
                        EmployeeAttendancePolicy.effective_until
                        >= effective_date
                    )
                ),
                EmployeeAttendancePolicy.is_active.is_(True),
                EmployeeAttendancePolicy.deleted_at.is_(None),
            )
            .order_by(
                EmployeeAttendancePolicy.effective_from.desc(),
            )
        )

        return self._session.scalar(stmt)

    # -------------------------------------------------------------------------
    # Employee Queries
    # -------------------------------------------------------------------------

    def list_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> list[EmployeeAttendancePolicy]:
        """
        Retrieve all non-deleted attendance policy assignments for an employee.
        """

        stmt = (
            select(EmployeeAttendancePolicy)
            .where(
                EmployeeAttendancePolicy.tenant_id
                == tenant_id,
                EmployeeAttendancePolicy.employee_id
                == employee_id,
                EmployeeAttendancePolicy.deleted_at.is_(None),
            )
            .order_by(
                EmployeeAttendancePolicy.effective_from.desc(),
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
        effective_from: date,
        effective_until: date,
    ) -> list[EmployeeAttendancePolicy]:
        """
        Retrieve attendance policy assignments overlapping a date range.
        """

        stmt = (
            select(EmployeeAttendancePolicy)
            .where(
                EmployeeAttendancePolicy.tenant_id
                == tenant_id,
                EmployeeAttendancePolicy.employee_id
                == employee_id,
                EmployeeAttendancePolicy.deleted_at.is_(None),
                EmployeeAttendancePolicy.effective_from
                <= effective_until,
                (
                    EmployeeAttendancePolicy.effective_until.is_(None)
                    | (
                        EmployeeAttendancePolicy.effective_until
                        >= effective_from
                    )
                ),
            )
            .order_by(
                EmployeeAttendancePolicy.effective_from.asc(),
            )
        )

        return list(
            self._session.scalars(stmt).all(),
        )

    # -------------------------------------------------------------------------
    # Existence
    # -------------------------------------------------------------------------

    def exists_effective_policy(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> bool:
        """
        Determine whether an active attendance policy assignment exists
        for an employee on a specific date.
        """

        stmt = select(EmployeeAttendancePolicy.id).where(
            EmployeeAttendancePolicy.tenant_id
            == tenant_id,
            EmployeeAttendancePolicy.employee_id
            == employee_id,
            EmployeeAttendancePolicy.effective_from
            <= effective_date,
            (
                EmployeeAttendancePolicy.effective_until.is_(None)
                | (
                    EmployeeAttendancePolicy.effective_until
                    >= effective_date
                )
            ),
            EmployeeAttendancePolicy.is_active.is_(True),
            EmployeeAttendancePolicy.deleted_at.is_(None),
        )

        return self._session.scalar(stmt) is not None