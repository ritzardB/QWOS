"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Employee Work Agreement Repository Contract
===============================================================================
"""

from __future__ import annotations

from datetime import date
from typing import Protocol

from qwos.domains.attendance.models.employee_work_agreement import (
    EmployeeWorkAgreement,
)


class EmployeeWorkAgreementRepository(Protocol):
    """
    Contract for EmployeeWorkAgreement persistence.
    """

    # -------------------------------------------------------------------------
    # Base Operations
    # -------------------------------------------------------------------------

    def get_by_id(
        self,
        agreement_id: str,
    ) -> EmployeeWorkAgreement | None:
        """
        Retrieve a work agreement by identifier.
        """
        ...

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        agreement_id: str,
    ) -> EmployeeWorkAgreement | None:
        """
        Retrieve a non-deleted work agreement within a tenant.
        """
        ...

    def save(
        self,
        agreement: EmployeeWorkAgreement,
    ) -> None:
        """
        Persist an employee work agreement.
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
    ) -> EmployeeWorkAgreement | None:
        """
        Retrieve the work agreement effective for an employee on a date.
        """
        ...

    def list_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> list[EmployeeWorkAgreement]:
        """
        Retrieve all non-deleted work agreements for an employee.
        """
        ...

    def get_active_by_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> EmployeeWorkAgreement | None:
        """
        Retrieve the currently active work agreement for an employee.
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
        Determine whether an agreement already starts on a given date.
        """
        ...
