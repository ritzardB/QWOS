"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

SQLAlchemy Leave Type Repository

Author:
    Richard Balabarcon
===============================================================================
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from qwos.core.database.repositories.base_repository import BaseRepository
from qwos.domains.leave.models.leave_type import LeaveType
from qwos.domains.leave.repositories.leave_type_repository import (
    LeaveTypeRepository,
)


class SQLAlchemyLeaveTypeRepository(
    BaseRepository[LeaveType],
    LeaveTypeRepository,
):
    """
    SQLAlchemy implementation of the LeaveTypeRepository.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(
            session=session,
            model=LeaveType,
        )

    def get_by_id(
        self,
        leave_type_id: str,
    ) -> LeaveType | None:
        return super().get_by_id(leave_type_id)

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        leave_type_id: str,
    ) -> LeaveType | None:
        statement = select(LeaveType).where(
            LeaveType.id == leave_type_id,
            LeaveType.tenant_id == tenant_id,
            LeaveType.deleted_at.is_(None),
        )

        return self._session.scalar(statement)

    def save(
        self,
        leave_type: LeaveType,
    ) -> None:
        self._session.add(leave_type)

    def list_by_tenant(
        self,
        *,
        tenant_id: str,
    ) -> list[LeaveType]:
        statement = (
            select(LeaveType)
            .where(
                LeaveType.tenant_id == tenant_id,
                LeaveType.deleted_at.is_(None),
            )
            .order_by(LeaveType.leave_code)
        )

        return list(self._session.scalars(statement).all())

    def get_active_by_code(
        self,
        *,
        tenant_id: str,
        leave_code: str,
    ) -> LeaveType | None:
        normalized_code = leave_code.strip().lower()

        statement = select(LeaveType).where(
            LeaveType.tenant_id == tenant_id,
            LeaveType.leave_code == normalized_code,
            LeaveType.is_active.is_(True),
            LeaveType.deleted_at.is_(None),
        )

        return self._session.scalar(statement)

    def exists_by_code(
        self,
        *,
        tenant_id: str,
        leave_code: str,
    ) -> bool:
        normalized_code = leave_code.strip().lower()

        statement = select(LeaveType.id).where(
            LeaveType.tenant_id == tenant_id,
            LeaveType.leave_code == normalized_code,
            LeaveType.deleted_at.is_(None),
        )

        return self._session.scalar(statement) is not None