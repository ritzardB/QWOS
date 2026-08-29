"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

Employee Immigration Repository Contract
===============================================================================
"""

from __future__ import annotations

from datetime import date
from typing import Protocol

from qwos.domains.hr.models.employee_immigration import (
    EmployeeImmigration,
)


class EmployeeImmigrationRepository(Protocol):
    """
    Contract for EmployeeImmigration persistence.
    """

    def get_by_id(
        self,
        immigration_id: str,
    ) -> EmployeeImmigration | None:
        """
        Retrieve an immigration record by identifier.
        """
        ...

    def save(
        self,
        immigration: EmployeeImmigration,
    ) -> None:
        """
        Persist an immigration record.
        """
        ...

    def get_current_by_employee_id(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        immigration_type: str,
        as_of_date: date,
    ) -> EmployeeImmigration | None:
        """
        Retrieve the current non-expired record for an employee/type.
        """
        ...

    def list_by_employee_id(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        immigration_type: str | None = None,
    ) -> list[EmployeeImmigration]:
        """
        Retrieve immigration history for an employee.
        """
        ...

    def list_expiring_between(
        self,
        *,
        tenant_id: str,
        start_date: date,
        end_date: date,
        immigration_type: str | None = None,
    ) -> list[EmployeeImmigration]:
        """
        Retrieve immigration records expiring within a date window.
        """
        ...
