"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

File:
    employee_document_repository.py

Description:
    Repository contract for EmployeeDocument persistence.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from qwos.domains.hr.models.employee_document import EmployeeDocument


class EmployeeDocumentRepository(Protocol):
    """
    Contract for EmployeeDocument persistence.
    """

    # -------------------------------------------------------------------------
    # Base Operations
    # -------------------------------------------------------------------------

    def get_by_id(
        self,
        document_id: str,
    ) -> EmployeeDocument | None:
        """
        Retrieve an employee document by identifier.
        """
        ...

    def save(
        self,
        document: EmployeeDocument,
    ) -> None:
        """
        Persist an employee document.
        """
        ...

    # -------------------------------------------------------------------------
    # Employee Queries
    # -------------------------------------------------------------------------

    def list_by_employee_id(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        document_category: str | None = None,
    ) -> list[EmployeeDocument]:
        """
        Retrieve documents belonging to an employee.
        """
        ...

    def list_by_immigration_id(
        self,
        *,
        tenant_id: str,
        immigration_id: str,
    ) -> list[EmployeeDocument]:
        """
        Retrieve documents associated with an immigration record.
        """
        ...

    def exists_by_storage_key(
        self,
        storage_key: str,
    ) -> bool:
        """
        Determine whether a storage key already exists.
        """
        ...

    def get_next_version(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        document_category: str,
        immigration_id: str | None = None,
    ) -> int:
        """
        Return the next business document version.

        Versioning is scoped to the employee, document category, and optional
        immigration record.
        """
        ...
