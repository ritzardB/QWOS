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
    Contract for EmployeeAttendancePolicy persistence.
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
        Retrieve a non-deleted assignment within a tenant.
        """
        ...

    def save(
        self,
        employee_attendance_policy: EmployeeAttendancePolicy,
    ) -> None:
        """
        Persist an employee attendance policy assignment.
        """
        ...

    # -------------------------------------------------------------------------
    # Employee Policy Queries
    # -------------------------------------------------------------------------

    def get_effective_for_employee(
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

    def list_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> list[EmployeeAttendancePolicy]:
        """
        Retrieve attendance policy assignments for an employee.
        """
        ...

    def list_active(
        self,
        *,
        tenant_id: str,
    ) -> list[EmployeeAttendancePolicy]:
        """
        Retrieve active employee attendance policy assignments for a tenant.
        """
        ...