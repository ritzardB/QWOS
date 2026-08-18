"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

HR Module

File:
    sqlalchemy_employee_document_repository.py

Description:
    SQLAlchemy implementation of EmployeeDocumentRepository.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.domains.hr.repositories.employee_document_repository import (
    EmployeeDocumentRepository,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from qwos.core.database.repositories.base_repository import BaseRepository
from qwos.domains.hr.models.employee_document import EmployeeDocument


class SQLAlchemyEmployeeDocumentRepository(
    BaseRepository[EmployeeDocument],
    EmployeeDocumentRepository,
):
    """
    SQLAlchemy implementation of EmployeeDocumentRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=EmployeeDocument,
        )

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
        Retrieve active documents belonging to an employee.
        """

        conditions = [
            EmployeeDocument.tenant_id == tenant_id,
            EmployeeDocument.employee_id == employee_id,
            EmployeeDocument.deleted_at.is_(None),
        ]

        if document_category is not None:
            conditions.append(
                EmployeeDocument.document_category
                == document_category.strip().lower()
            )

        stmt = (
            select(EmployeeDocument)
            .where(*conditions)
            .order_by(
                EmployeeDocument.document_category.asc(),
                EmployeeDocument.document_version.desc(),
                EmployeeDocument.uploaded_at.desc(),
            )
        )

        return list(
            self._session.scalars(stmt).all()
        )

    def list_by_immigration_id(
        self,
        *,
        tenant_id: str,
        immigration_id: str,
    ) -> list[EmployeeDocument]:
        """
        Retrieve active documents attached to an immigration record.
        """

        stmt = (
            select(EmployeeDocument)
            .where(
                EmployeeDocument.tenant_id == tenant_id,
                EmployeeDocument.immigration_id == immigration_id,
                EmployeeDocument.deleted_at.is_(None),
            )
            .order_by(
                EmployeeDocument.document_category.asc(),
                EmployeeDocument.document_version.desc(),
                EmployeeDocument.uploaded_at.desc(),
            )
        )

        return list(
            self._session.scalars(stmt).all()
        )

    def exists_by_storage_key(
        self,
        storage_key: str,
    ) -> bool:
        """
        Determine whether a storage key already exists.
        """

        stmt = (
            select(EmployeeDocument.id)
            .where(
                EmployeeDocument.storage_key == storage_key,
                EmployeeDocument.deleted_at.is_(None),
            )
            .limit(1)
        )

        return self._session.scalar(stmt) is not None