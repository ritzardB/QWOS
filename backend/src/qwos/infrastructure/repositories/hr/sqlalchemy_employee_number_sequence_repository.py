"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

HR Module

Employee Number Sequence Repository

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from qwos.core.database.repositories.base_repository import BaseRepository
from qwos.domains.hr.models.employee_number_sequence import (
    EmployeeNumberSequence,
)
from qwos.domains.hr.repositories.employee_number_sequence_repository import (
    EmployeeNumberSequenceRepository,
)


class SQLAlchemyEmployeeNumberSequenceRepository(
    BaseRepository[EmployeeNumberSequence],
    EmployeeNumberSequenceRepository,
):
    """
    SQLAlchemy implementation of EmployeeNumberSequenceRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=EmployeeNumberSequence,
        )

    def get_by_tenant_id_for_update(
        self,
        tenant_id: str,
    ) -> EmployeeNumberSequence | None:
        """
        Retrieve the active tenant sequence while acquiring a row lock.

        The caller must already be inside the Unit of Work transaction.
        """

        stmt = (
            select(EmployeeNumberSequence)
            .where(
                EmployeeNumberSequence.tenant_id == tenant_id,
                EmployeeNumberSequence.is_active.is_(True),
                EmployeeNumberSequence.deleted_at.is_(None),
            )
            .with_for_update()
        )

        return self._session.scalar(stmt)
