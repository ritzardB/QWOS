from __future__ import annotations

from datetime import date
from typing import Protocol

from qwos.domains.leave.models.employee_leave_assignment import (
    EmployeeLeaveAssignment,
)


class EmployeeLeaveAssignmentRepository(Protocol):
    def get_by_id(
        self,
        assignment_id: str,
    ) -> EmployeeLeaveAssignment | None: ...

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        assignment_id: str,
    ) -> EmployeeLeaveAssignment | None: ...

    def save(
        self,
        assignment: EmployeeLeaveAssignment,
    ) -> None: ...

    def list_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> list[EmployeeLeaveAssignment]: ...

    def get_by_employee_and_start_date(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_from: date,
    ) -> EmployeeLeaveAssignment | None: ...

    def exists_by_employee_and_start_date(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_from: date,
    ) -> bool: ...