from __future__ import annotations

from datetime import date
from typing import Protocol

from qwos.domains.leave.models.employee_leave_balance import (
    EmployeeLeaveBalance,
)


class EmployeeLeaveBalanceRepository(Protocol):
    def get_by_id(
        self,
        balance_id: str,
    ) -> EmployeeLeaveBalance | None:
        ...

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        balance_id: str,
    ) -> EmployeeLeaveBalance | None:
        ...

    def save(
        self,
        balance: EmployeeLeaveBalance,
    ) -> None:
        ...

    def list_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> list[EmployeeLeaveBalance]:
        ...

    def get_by_assignment_and_period(
        self,
        *,
        tenant_id: str,
        employee_leave_assignment_id: str,
        period_start: date,
        period_end: date,
    ) -> EmployeeLeaveBalance | None:
        ...

    def exists_by_assignment_and_period(
        self,
        *,
        tenant_id: str,
        employee_leave_assignment_id: str,
        period_start: date,
        period_end: date,
    ) -> bool:
        ...