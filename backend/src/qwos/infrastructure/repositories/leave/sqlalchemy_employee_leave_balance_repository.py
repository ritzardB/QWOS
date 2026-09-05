from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from qwos.core.database.repositories.base_repository import BaseRepository
from qwos.domains.leave.models.employee_leave_balance import (
    EmployeeLeaveBalance,
)
from qwos.domains.leave.repositories.employee_leave_balance_repository import (
    EmployeeLeaveBalanceRepository,
)


class SQLAlchemyEmployeeLeaveBalanceRepository(
    BaseRepository[EmployeeLeaveBalance],
    EmployeeLeaveBalanceRepository,
):
    def __init__(self, session: Session) -> None:
        super().__init__(
            session=session,
            model=EmployeeLeaveBalance,
        )

    def get_by_id(
        self,
        balance_id: str,
    ) -> EmployeeLeaveBalance | None:
        return super().get_by_id(balance_id)

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        balance_id: str,
    ) -> EmployeeLeaveBalance | None:
        statement = select(EmployeeLeaveBalance).where(
            EmployeeLeaveBalance.id == balance_id,
            EmployeeLeaveBalance.tenant_id == tenant_id,
            EmployeeLeaveBalance.deleted_at.is_(None),
        )
        return self._session.scalar(statement)

    def save(
        self,
        balance: EmployeeLeaveBalance,
    ) -> None:
        self._session.add(balance)

    def list_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> list[EmployeeLeaveBalance]:
        statement = (
            select(EmployeeLeaveBalance)
            .where(
                EmployeeLeaveBalance.tenant_id == tenant_id,
                EmployeeLeaveBalance.employee_id == employee_id,
                EmployeeLeaveBalance.deleted_at.is_(None),
            )
            .order_by(
                EmployeeLeaveBalance.period_start,
                EmployeeLeaveBalance.period_end,
            )
        )
        return list(self._session.scalars(statement).all())

    def get_by_assignment_and_period(
        self,
        *,
        tenant_id: str,
        employee_leave_assignment_id: str,
        period_start: date,
        period_end: date,
    ) -> EmployeeLeaveBalance | None:
        statement = select(EmployeeLeaveBalance).where(
            EmployeeLeaveBalance.tenant_id == tenant_id,
            EmployeeLeaveBalance.employee_leave_assignment_id
            == employee_leave_assignment_id,
            EmployeeLeaveBalance.period_start == period_start,
            EmployeeLeaveBalance.period_end == period_end,
            EmployeeLeaveBalance.deleted_at.is_(None),
        )
        return self._session.scalar(statement)

    def exists_by_assignment_and_period(
        self,
        *,
        tenant_id: str,
        employee_leave_assignment_id: str,
        period_start: date,
        period_end: date,
    ) -> bool:
        statement = select(EmployeeLeaveBalance.id).where(
            EmployeeLeaveBalance.tenant_id == tenant_id,
            EmployeeLeaveBalance.employee_leave_assignment_id
            == employee_leave_assignment_id,
            EmployeeLeaveBalance.period_start == period_start,
            EmployeeLeaveBalance.period_end == period_end,
            EmployeeLeaveBalance.deleted_at.is_(None),
        )
        return self._session.scalar(statement) is not None