from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from qwos.core.database.repositories.base_repository import BaseRepository
from qwos.domains.leave.models.employee_leave_assignment import (
    EmployeeLeaveAssignment,
)
from qwos.domains.leave.repositories.employee_leave_assignment_repository import (
    EmployeeLeaveAssignmentRepository,
)


class SQLAlchemyEmployeeLeaveAssignmentRepository(
    BaseRepository[EmployeeLeaveAssignment],
    EmployeeLeaveAssignmentRepository,
):
    def __init__(self, session: Session) -> None:
        super().__init__(
            session=session,
            model=EmployeeLeaveAssignment,
        )

    def get_by_id(
        self,
        assignment_id: str,
    ) -> EmployeeLeaveAssignment | None:
        return super().get_by_id(assignment_id)

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        assignment_id: str,
    ) -> EmployeeLeaveAssignment | None:
        statement = select(EmployeeLeaveAssignment).where(
            EmployeeLeaveAssignment.id == assignment_id,
            EmployeeLeaveAssignment.tenant_id == tenant_id,
            EmployeeLeaveAssignment.deleted_at.is_(None),
        )
        return self._session.scalar(statement)

    def save(
        self,
        assignment: EmployeeLeaveAssignment,
    ) -> None:
        self._session.add(assignment)

    def list_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> list[EmployeeLeaveAssignment]:
        statement = (
            select(EmployeeLeaveAssignment)
            .where(
                EmployeeLeaveAssignment.tenant_id == tenant_id,
                EmployeeLeaveAssignment.employee_id == employee_id,
                EmployeeLeaveAssignment.deleted_at.is_(None),
            )
            .order_by(
                EmployeeLeaveAssignment.effective_from,
            )
        )
        return list(self._session.scalars(statement).all())

    def get_by_employee_and_start_date(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_from: date,
    ) -> EmployeeLeaveAssignment | None:
        statement = select(EmployeeLeaveAssignment).where(
            EmployeeLeaveAssignment.tenant_id == tenant_id,
            EmployeeLeaveAssignment.employee_id == employee_id,
            EmployeeLeaveAssignment.effective_from == effective_from,
            EmployeeLeaveAssignment.deleted_at.is_(None),
        )
        return self._session.scalar(statement)

    def exists_by_employee_and_start_date(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_from: date,
    ) -> bool:
        statement = select(EmployeeLeaveAssignment.id).where(
            EmployeeLeaveAssignment.tenant_id == tenant_id,
            EmployeeLeaveAssignment.employee_id == employee_id,
            EmployeeLeaveAssignment.effective_from == effective_from,
            EmployeeLeaveAssignment.deleted_at.is_(None),
        )
        return self._session.scalar(statement) is not None