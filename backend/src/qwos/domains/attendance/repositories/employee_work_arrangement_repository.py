"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Employee Work Arrangement Repository Contract
===============================================================================
"""

from __future__ import annotations

from datetime import date
from typing import Protocol

from qwos.domains.attendance.models.employee_work_arrangement import (
    EmployeeWorkArrangement,
)


class EmployeeWorkArrangementRepository(Protocol):
    """
    Contract for EmployeeWorkArrangement persistence.
    """

    # -------------------------------------------------------------------------
    # Base Operations
    # -------------------------------------------------------------------------

    def get_by_id(
        self,
        arrangement_id: str,
    ) -> EmployeeWorkArrangement | None:
        """
        Retrieve a work arrangement by identifier.
        """
        ...

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        arrangement_id: str,
    ) -> EmployeeWorkArrangement | None:
        """
        Retrieve a non-deleted work arrangement within a tenant.
        """
        ...

    def save(
        self,
        arrangement: EmployeeWorkArrangement,
    ) -> None:
        """
        Persist an employee work arrangement.
        """
        ...

    # -------------------------------------------------------------------------
    # Employee Queries
    # -------------------------------------------------------------------------

    def get_by_employee_and_date(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> EmployeeWorkArrangement | None:
        """
        Retrieve the work arrangement effective for an employee on a date.
        """
        ...

    def list_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> list[EmployeeWorkArrangement]:
        """
        Retrieve all non-deleted work arrangements for an employee.
        """
        ...

    def get_active_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> EmployeeWorkArrangement | None:
        """
        Retrieve the currently active work arrangement for an employee.
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
        Determine whether an arrangement already starts on a given date.
        """
        ...
