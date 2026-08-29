"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

HR Module

File:
    sqlalchemy_employee_profile_repository.py

Description:
    SQLAlchemy implementation of EmployeeProfileRepository.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from qwos.core.database.repositories.base_repository import BaseRepository
from qwos.domains.hr.models.employee_profile import EmployeeProfile
from qwos.domains.hr.repositories.employee_profile_repository import (
    EmployeeProfileRepository,
)


class SQLAlchemyEmployeeProfileRepository(
    BaseRepository[EmployeeProfile],
    EmployeeProfileRepository,
):
    """
    SQLAlchemy implementation of EmployeeProfileRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=EmployeeProfile,
        )

    # -------------------------------------------------------------------------
    # Employee Profile Queries
    # -------------------------------------------------------------------------

    def get_by_employee_id(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> EmployeeProfile | None:
        """
        Retrieve an active employee profile by employee identifier.
        """

        stmt = select(EmployeeProfile).where(
            EmployeeProfile.tenant_id == tenant_id,
            EmployeeProfile.employee_id == employee_id,
            EmployeeProfile.deleted_at.is_(None),
        )

        return self._session.scalar(stmt)

    def exists_by_employee_id(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> bool:
        """
        Determine whether an active employee profile exists.
        """

        return (
            self.get_by_employee_id(
                tenant_id=tenant_id,
                employee_id=employee_id,
            )
            is not None
        )
