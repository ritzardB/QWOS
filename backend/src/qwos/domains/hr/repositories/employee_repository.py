"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

Employee Repository Contract
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from qwos.domains.hr.models.employee import Employee


class EmployeeRepository(Protocol):
    """
    Contract for Employee persistence.
    """

    # -------------------------------------------------------------------------
    # Base Operations
    # -------------------------------------------------------------------------

    def get_by_id(
        self,
        employee_id: str,
    ) -> Employee | None:
        """
        Retrieve an employee by identifier.
        """
        ...

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> Employee | None:
        """
        Retrieve a non-deleted employee within a tenant.
        """
        ...

    def save(
        self,
        employee: Employee,
    ) -> None:
        """
        Persist an employee.
        """
        ...

    # -------------------------------------------------------------------------
    # Employee Queries
    # -------------------------------------------------------------------------

    def get_by_employee_number(
        self,
        *,
        tenant_id: str,
        employee_number: str,
    ) -> Employee | None:
        """
        Retrieve an employee by tenant-scoped employee number.
        """
        ...

    def get_by_user_id(
        self,
        *,
        tenant_id: str,
        user_id: str,
    ) -> Employee | None:
        """
        Retrieve an employee linked to a QWOS user.
        """
        ...

    def list_active(
        self,
        *,
        tenant_id: str,
    ) -> list[Employee]:
        """
        Retrieve active employees for a tenant.
        """
        ...

    def exists_by_employee_number(
        self,
        *,
        tenant_id: str,
        employee_number: str,
    ) -> bool:
        """
        Determine whether an employee number already exists for a tenant.
        """
        ...

    def exists_by_user_id(
        self,
        *,
        tenant_id: str,
        user_id: str,
    ) -> bool:
        """
        Determine whether a user is already linked to an employee.
        """
        ...

    def exists_by_work_email(
        self,
        *,
        tenant_id: str,
        work_email: str,
    ) -> bool:
        """
        Determine whether an active employee already uses the work email.
        """
        ...
