"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

Employee Profile Repository Contract
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from qwos.domains.hr.models.employee_profile import EmployeeProfile


class EmployeeProfileRepository(Protocol):
    """
    Contract for EmployeeProfile persistence.
    """

    # -------------------------------------------------------------------------
    # Base Operations
    # -------------------------------------------------------------------------

    def get_by_id(
        self,
        profile_id: str,
    ) -> EmployeeProfile | None:
        """
        Retrieve an employee profile by identifier.
        """
        ...

    def save(
        self,
        profile: EmployeeProfile,
    ) -> None:
        """
        Persist an employee profile.
        """
        ...

    # -------------------------------------------------------------------------
    # Employee Profile Queries
    # -------------------------------------------------------------------------

    def get_by_employee_id(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> EmployeeProfile | None:
        """
        Retrieve the profile associated with an employee.
        """
        ...

    def exists_by_employee_id(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> bool:
        """
        Determine whether an employee profile already exists.
        """
        ...