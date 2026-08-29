"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Employee Attendance Policy Repository Contract
===============================================================================
"""

from __future__ import annotations

from datetime import date
from typing import Protocol

from qwos.domains.attendance.models.employee_attendance_policy import (
    EmployeeAttendancePolicy,
)


class EmployeeAttendancePolicyRepository(Protocol):
    """
    Contract for EmployeeAttendancePolicy persistence and queries.
    """

    # -------------------------------------------------------------------------
    # Base Operations
    # -------------------------------------------------------------------------

    def get_by_id(
        self,
        employee_attendance_policy_id: str,
    ) -> EmployeeAttendancePolicy | None:
        """
        Retrieve an employee attendance policy assignment by identifier.
        """
        ...

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        employee_attendance_policy_id: str,
    ) -> EmployeeAttendancePolicy | None:
        """
        Retrieve a non-deleted employee attendance policy assignment
        within a tenant.
        """
        ...

    def save(
        self,
        assignment: EmployeeAttendancePolicy,
    ) -> None:
        """
        Persist an employee attendance policy assignment.
        """
        ...

    # -------------------------------------------------------------------------
    # Effective Policy
    # -------------------------------------------------------------------------

    def get_effective_policy(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> EmployeeAttendancePolicy | None:
        """
        Retrieve the attendance policy assignment effective for an employee
        on a specific date.
        """
        ...

    # -------------------------------------------------------------------------
    # Employee Queries
    # -------------------------------------------------------------------------

    def list_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> list[EmployeeAttendancePolicy]:
        """
        Retrieve all non-deleted attendance policy assignments for an employee.
        """
        ...

    def list_by_employee_and_period(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_from: date,
        effective_until: date,
    ) -> list[EmployeeAttendancePolicy]:
        """
        Retrieve attendance policy assignments overlapping a date range.
        """
        ...

    # -------------------------------------------------------------------------
    # Existence
    # -------------------------------------------------------------------------

    def exists_effective_policy(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> bool:
        """
        Determine whether an attendance policy assignment exists for an
        employee on a specific date.
        """
        ...
