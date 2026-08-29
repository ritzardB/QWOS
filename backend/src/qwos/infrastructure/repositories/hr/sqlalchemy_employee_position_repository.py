"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

HR Module

File:
    sqlalchemy_employee_position_repository.py

Description:
    SQLAlchemy implementation of EmployeePositionRepository.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from qwos.core.database.repositories.base_repository import BaseRepository
from qwos.domains.hr.models.employee_position import EmployeePosition
from qwos.domains.hr.repositories.employee_position_repository import (
    EmployeePositionRepository,
)


class SQLAlchemyEmployeePositionRepository(
    BaseRepository[EmployeePosition],
    EmployeePositionRepository,
):
    """
    SQLAlchemy implementation of EmployeePositionRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=EmployeePosition,
        )

    def get_current_by_employee_id(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> EmployeePosition | None:
        """
        Retrieve the current active position for an employee.
        """

        stmt = (
            select(EmployeePosition)
            .where(
                EmployeePosition.tenant_id == tenant_id,
                EmployeePosition.employee_id == employee_id,
                EmployeePosition.deleted_at.is_(None),
                EmployeePosition.effective_to.is_(None),
            )
            .order_by(
                EmployeePosition.effective_from.desc(),
            )
        )

        return self._session.scalar(stmt)

    def exists_current_by_employee_id(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> bool:
        """
        Determine whether an employee has a current position.
        """

        return (
            self.get_current_by_employee_id(
                tenant_id=tenant_id,
                employee_id=employee_id,
            )
            is not None
        )
