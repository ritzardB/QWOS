"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Employee Work Schedule Repository Contract
===============================================================================
"""

from __future__ import annotations

from datetime import date
from typing import Protocol

from qwos.domains.attendance.models.employee_work_schedule import (
    EmployeeWorkSchedule,
)


class EmployeeWorkScheduleRepository(Protocol):
    """
    Contract for EmployeeWorkSchedule persistence.
    """

    # -------------------------------------------------------------------------
    # Base Operations
    # -------------------------------------------------------------------------

    def get_by_id(
        self,
        assignment_id: str,
    ) -> EmployeeWorkSchedule | None:
        """
        Retrieve an employee work schedule assignment by identifier.
        """
        ...

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        assignment_id: str,
    ) -> EmployeeWorkSchedule | None:
        """
        Retrieve a non-deleted assignment within a tenant.
        """
        ...

    def save(
        self,
        assignment: EmployeeWorkSchedule,
    ) -> None:
        """
        Persist an employee work schedule assignment.
        """
        ...

    # -------------------------------------------------------------------------
    # Employee Queries
    # -------------------------------------------------------------------------

    def get_effective_for_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> EmployeeWorkSchedule | None:
        """
        Retrieve the work schedule assignment effective for an employee
        on a specific date.
        """
        ...

    def list_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> list[EmployeeWorkSchedule]:
        """
        Retrieve all non-deleted work schedule assignments for an employee.
        """
        ...

    def get_active_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> EmployeeWorkSchedule | None:
        """
        Retrieve the currently active work schedule assignment.
        """
        ...

    def exists_by_employee_and_start_date(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_from: date,
    ) -> bool:
        """
        Determine whether an assignment already starts on a given date.
        """
        ...