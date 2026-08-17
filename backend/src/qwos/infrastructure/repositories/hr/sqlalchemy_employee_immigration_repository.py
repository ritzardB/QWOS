"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

HR Module

File:
    sqlalchemy_employee_immigration_repository.py

Description:
    SQLAlchemy implementation of EmployeeImmigrationRepository.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from qwos.core.database.repositories.base_repository import BaseRepository
from qwos.domains.hr.models.employee_immigration import (
    EmployeeImmigration,
)
from qwos.domains.hr.repositories.employee_immigration_repository import (
    EmployeeImmigrationRepository,
)


class SQLAlchemyEmployeeImmigrationRepository(
    BaseRepository[EmployeeImmigration],
    EmployeeImmigrationRepository,
):
    """
    SQLAlchemy implementation of EmployeeImmigrationRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=EmployeeImmigration,
        )

    # -------------------------------------------------------------------------
    # Employee Immigration Queries
    # -------------------------------------------------------------------------

    def get_current_by_employee_id(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        immigration_type: str,
        as_of_date: date,
    ) -> EmployeeImmigration | None:
        """
        Retrieve the current valid immigration record.
        """

        stmt = (
            select(EmployeeImmigration)
            .where(
                EmployeeImmigration.tenant_id == tenant_id,
                EmployeeImmigration.employee_id == employee_id,
                EmployeeImmigration.immigration_type
                == immigration_type.strip().lower(),
                EmployeeImmigration.deleted_at.is_(None),
                (
                    EmployeeImmigration.expiry_date.is_(None)
                    | (
                        EmployeeImmigration.expiry_date
                        >= as_of_date
                    )
                ),
            )
            .order_by(
                EmployeeImmigration.expiry_date.is_(None).desc(),
                EmployeeImmigration.expiry_date.desc(),
                EmployeeImmigration.issue_date.desc(),
            )
        )

        return self._session.scalar(stmt)

    def list_by_employee_id(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        immigration_type: str | None = None,
    ) -> list[EmployeeImmigration]:
        """
        Retrieve immigration history for an employee.
        """

        conditions = [
            EmployeeImmigration.tenant_id == tenant_id,
            EmployeeImmigration.employee_id == employee_id,
            EmployeeImmigration.deleted_at.is_(None),
        ]

        if immigration_type is not None:
            conditions.append(
                EmployeeImmigration.immigration_type
                == immigration_type.strip().lower()
            )

        stmt = (
            select(EmployeeImmigration)
            .where(*conditions)
            .order_by(
                EmployeeImmigration.issue_date.desc().nullslast(),
                EmployeeImmigration.expiry_date.desc().nullslast(),
            )
        )

        return list(self._session.scalars(stmt).all())

    def list_expiring_between(
        self,
        *,
        tenant_id: str,
        start_date: date,
        end_date: date,
        immigration_type: str | None = None,
    ) -> list[EmployeeImmigration]:
        """
        Retrieve records whose expiry date falls within the requested window.
        """

        conditions = [
            EmployeeImmigration.tenant_id == tenant_id,
            EmployeeImmigration.deleted_at.is_(None),
            EmployeeImmigration.expiry_date >= start_date,
            EmployeeImmigration.expiry_date <= end_date,
        ]

        if immigration_type is not None:
            conditions.append(
                EmployeeImmigration.immigration_type
                == immigration_type.strip().lower()
            )

        stmt = (
            select(EmployeeImmigration)
            .where(*conditions)
            .order_by(
                EmployeeImmigration.expiry_date.asc(),
                EmployeeImmigration.employee_id,
            )
        )

        return list(self._session.scalars(stmt).all())