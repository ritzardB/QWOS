"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

HR Module

File:
    sqlalchemy_employee_repository.py

Description:
    SQLAlchemy implementation of EmployeeRepository.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from qwos.core.database.repositories.base_repository import BaseRepository
from qwos.domains.hr.models.employee import Employee
from qwos.domains.hr.repositories.employee_repository import (
    EmployeeRepository,
)


class SQLAlchemyEmployeeRepository(
    BaseRepository[Employee],
    EmployeeRepository,
):
    """
    SQLAlchemy implementation of EmployeeRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=Employee,
        )

    # -------------------------------------------------------------------------
    # Employee Queries
    # -------------------------------------------------------------------------

    def list_active(
        self,
        *,
        tenant_id: str,
    ) -> list[Employee]:
        """
        Retrieve active, non-deleted employees for a tenant.
        """

        stmt = (
            select(Employee)
            .where(
                Employee.tenant_id == tenant_id,
                Employee.deleted_at.is_(None),
                Employee.employment_status == "active",
            )
            .order_by(Employee.employee_number)
        )

        return list(self._session.scalars(stmt).all())

    def get_by_employee_number(
        self,
        *,
        tenant_id: str,
        employee_number: str,
    ) -> Employee | None:
        """
        Retrieve an employee by tenant-scoped employee number.
        """

        stmt = select(Employee).where(
            Employee.tenant_id == tenant_id,
            Employee.employee_number == employee_number,
            Employee.deleted_at.is_(None),
        )

        return self._session.scalar(stmt)

    def get_by_user_id(
        self,
        *,
        tenant_id: str,
        user_id: str,
    ) -> Employee | None:
        """
        Retrieve an employee linked to a QWOS user.
        """

        stmt = select(Employee).where(
            Employee.tenant_id == tenant_id,
            Employee.user_id == user_id,
            Employee.deleted_at.is_(None),
        )

        return self._session.scalar(stmt)

    def exists_by_employee_number(
        self,
        *,
        tenant_id: str,
        employee_number: str,
    ) -> bool:
        """
        Determine whether an employee number already exists for a tenant.
        """

        return (
            self.get_by_employee_number(
                tenant_id=tenant_id,
                employee_number=employee_number,
            )
            is not None
        )

    def exists_by_user_id(
        self,
        *,
        tenant_id: str,
        user_id: str,
    ) -> bool:
        """
        Determine whether a user is already linked to an employee.
        """

        return (
            self.get_by_user_id(
                tenant_id=tenant_id,
                user_id=user_id,
            )
            is not None
        )

    def exists_by_work_email(
        self,
        *,
        tenant_id: str,
        work_email: str,
    ) -> bool:
        """
        Determine whether an active employee already uses the work email.
        """

        stmt = select(Employee.id).where(
            Employee.tenant_id == tenant_id,
            Employee.work_email == work_email.strip().lower(),
            Employee.deleted_at.is_(None),
        )

        return self._session.scalar(stmt) is not None