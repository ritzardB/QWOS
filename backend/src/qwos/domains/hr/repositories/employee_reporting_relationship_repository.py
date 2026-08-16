"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

Employee Reporting Relationship Repository Contract
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from qwos.domains.hr.models.employee_reporting_relationship import (
    EmployeeReportingRelationship,
)


class EmployeeReportingRelationshipRepository(Protocol):
    """
    Contract for employee reporting relationship persistence.
    """

    def get_by_id(
        self,
        relationship_id: str,
    ) -> EmployeeReportingRelationship | None:
        ...

    def save(
        self,
        relationship: EmployeeReportingRelationship,
    ) -> None:
        ...

    def get_active_primary_manager(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> EmployeeReportingRelationship | None:
        ...

    def exists_active_primary_manager(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> bool:
        ...

    def get_active_reports(
        self,
        *,
        tenant_id: str,
        manager_employee_id: str,
    ) -> list[EmployeeReportingRelationship]:
        ...