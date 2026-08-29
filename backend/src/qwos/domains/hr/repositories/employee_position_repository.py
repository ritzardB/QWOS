"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

Employee Position Repository Contract
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from qwos.domains.hr.models.employee_position import EmployeePosition


class EmployeePositionRepository(Protocol):
    """
    Contract for EmployeePosition persistence.
    """

    def get_by_id(
        self,
        position_id: str,
    ) -> EmployeePosition | None:
        """
        Retrieve a position by identifier.
        """
        ...

    def save(
        self,
        position: EmployeePosition,
    ) -> None:
        """
        Persist an employee position.
        """
        ...

    def get_current_by_employee_id(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> EmployeePosition | None:
        """
        Retrieve the current active position for an employee.
        """
        ...

    def exists_current_by_employee_id(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> bool:
        """
        Determine whether an employee has a current position.
        """
        ...
