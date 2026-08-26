"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Attendance Module

File:
    sqlalchemy_employee_work_agreement_repository.py

Description:
    SQLAlchemy implementation of EmployeeWorkAgreementRepository.

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
from qwos.domains.attendance.models.employee_work_agreement import (
    EmployeeWorkAgreement,
)
from qwos.domains.attendance.repositories.employee_work_agreement_repository import (
    EmployeeWorkAgreementRepository,
)


class SQLAlchemyEmployeeWorkAgreementRepository(
    BaseRepository[EmployeeWorkAgreement],
    EmployeeWorkAgreementRepository,
):
    """
    SQLAlchemy implementation of EmployeeWorkAgreementRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=EmployeeWorkAgreement,
        )

    # -------------------------------------------------------------------------
    # Tenant Queries
    # -------------------------------------------------------------------------

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        agreement_id: str,
    ) -> EmployeeWorkAgreement | None:
        """
        Retrieve a non-deleted work agreement within a tenant.
        """

        stmt = select(EmployeeWorkAgreement).where(
            EmployeeWorkAgreement.id == agreement_id,
            EmployeeWorkAgreement.tenant_id == tenant_id,
            EmployeeWorkAgreement.deleted_at.is_(None),
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
    ) -> EmployeeWorkAgreement | None:
        """
        Retrieve the work agreement effective for an employee on a date.

        The agreement must have started on or before the requested date
        and must not have ended before that date.
        """

        stmt = (
            select(EmployeeWorkAgreement)
            .where(
                EmployeeWorkAgreement.tenant_id == tenant_id,
                EmployeeWorkAgreement.employee_id == employee_id,
                EmployeeWorkAgreement.effective_from <= effective_date,
                (
                    EmployeeWorkAgreement.effective_until.is_(None)
                    | (
                        EmployeeWorkAgreement.effective_until
                        >= effective_date
                    )
                ),
                EmployeeWorkAgreement.deleted_at.is_(None),
            )
            .order_by(
                EmployeeWorkAgreement.effective_from.desc(),
            )
            .limit(1)
        )

        return self._session.scalar(stmt)

    def list_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> list[EmployeeWorkAgreement]:
        """
        Retrieve all non-deleted work agreements for an employee.
        """

        stmt = (
            select(EmployeeWorkAgreement)
            .where(
                EmployeeWorkAgreement.tenant_id == tenant_id,
                EmployeeWorkAgreement.employee_id == employee_id,
                EmployeeWorkAgreement.deleted_at.is_(None),
            )
            .order_by(
                EmployeeWorkAgreement.effective_from.desc(),
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
    ) -> EmployeeWorkAgreement | None:
        """
        Retrieve the currently active work agreement for an employee.
        """

        stmt = (
            select(EmployeeWorkAgreement)
            .where(
                EmployeeWorkAgreement.tenant_id == tenant_id,
                EmployeeWorkAgreement.employee_id == employee_id,
                EmployeeWorkAgreement.is_active.is_(True),
                EmployeeWorkAgreement.deleted_at.is_(None),
            )
            .order_by(
                EmployeeWorkAgreement.effective_from.desc(),
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
        Determine whether an agreement already starts on a given date.
        """

        stmt = select(EmployeeWorkAgreement.id).where(
            EmployeeWorkAgreement.tenant_id == tenant_id,
            EmployeeWorkAgreement.employee_id == employee_id,
            EmployeeWorkAgreement.effective_from == effective_from,
            EmployeeWorkAgreement.deleted_at.is_(None),
        )

        return self._session.scalar(stmt) is not None