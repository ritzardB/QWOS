from sqlalchemy import select
from sqlalchemy.orm import Session

from qwos.core.database.repositories.base_repository import BaseRepository
from qwos.domains.leave.models.leave_policy import LeavePolicy
from qwos.domains.leave.repositories.leave_policy_repository import (
    LeavePolicyRepository,
)


class SQLAlchemyLeavePolicyRepository(
    BaseRepository[LeavePolicy],
    LeavePolicyRepository,
):
    def __init__(self, session: Session) -> None:
        super().__init__(
            session=session,
            model=LeavePolicy,
        )

    def get_by_id(self, leave_policy_id: str) -> LeavePolicy | None:
        return super().get_by_id(leave_policy_id)

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        leave_policy_id: str,
    ) -> LeavePolicy | None:
        statement = select(LeavePolicy).where(
            LeavePolicy.id == leave_policy_id,
            LeavePolicy.tenant_id == tenant_id,
            LeavePolicy.deleted_at.is_(None),
        )

        return self._session.scalar(statement)

    def save(self, leave_policy: LeavePolicy) -> None:
        self._session.add(leave_policy)

    def list_by_tenant(
        self,
        *,
        tenant_id: str,
    ) -> list[LeavePolicy]:
        statement = (
            select(LeavePolicy)
            .where(
                LeavePolicy.tenant_id == tenant_id,
                LeavePolicy.deleted_at.is_(None),
            )
            .order_by(LeavePolicy.policy_code)
        )

        return list(self._session.scalars(statement).all())

    def get_active_by_code(
        self,
        *,
        tenant_id: str,
        policy_code: str,
    ) -> LeavePolicy | None:
        normalized_code = policy_code.strip().lower()

        statement = select(LeavePolicy).where(
            LeavePolicy.tenant_id == tenant_id,
            LeavePolicy.policy_code == normalized_code,
            LeavePolicy.is_active.is_(True),
            LeavePolicy.deleted_at.is_(None),
        )

        return self._session.scalar(statement)

    def exists_by_code(
        self,
        *,
        tenant_id: str,
        policy_code: str,
    ) -> bool:
        normalized_code = policy_code.strip().lower()

        statement = select(LeavePolicy.id).where(
            LeavePolicy.tenant_id == tenant_id,
            LeavePolicy.policy_code == normalized_code,
            LeavePolicy.deleted_at.is_(None),
        )

        return self._session.scalar(statement) is not None