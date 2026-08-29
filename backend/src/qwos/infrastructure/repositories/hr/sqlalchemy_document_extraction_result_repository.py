"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

HR Module

File:
    sqlalchemy_document_extraction_result_repository.py

Description:
    SQLAlchemy repository implementation for document extraction results.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from qwos.domains.hr.models.document_extraction_result import (
    DocumentExtractionResult,
)
from qwos.domains.hr.repositories.document_extraction_result_repository import (
    DocumentExtractionResultRepository,
)


class SQLAlchemyDocumentExtractionResultRepository(
    DocumentExtractionResultRepository,
):
    """
    SQLAlchemy implementation of DocumentExtractionResultRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id(
        self,
        result_id: str,
    ) -> DocumentExtractionResult | None:
        """
        Retrieve an extraction result by identifier.
        """

        statement = select(DocumentExtractionResult).where(
            DocumentExtractionResult.id == result_id,
            DocumentExtractionResult.deleted_at.is_(None),
        )

        return self._session.scalar(statement)

    def save(
        self,
        result: DocumentExtractionResult,
    ) -> None:
        """
        Persist an extraction result.
        """

        self._session.add(result)

    def list_by_document_id(
        self,
        *,
        tenant_id: str,
        employee_document_id: str,
    ) -> list[DocumentExtractionResult]:
        """
        Retrieve active extraction results for an employee document.
        """

        statement = (
            select(DocumentExtractionResult)
            .where(
                DocumentExtractionResult.tenant_id == tenant_id,
                DocumentExtractionResult.employee_document_id == employee_document_id,
                DocumentExtractionResult.deleted_at.is_(None),
            )
            .order_by(
                DocumentExtractionResult.extracted_at.desc(),
                DocumentExtractionResult.created_at.desc(),
            )
        )

        return list(
            self._session.scalars(statement).all(),
        )

    def list_by_field_id(
        self,
        *,
        tenant_id: str,
        document_definition_field_id: str,
    ) -> list[DocumentExtractionResult]:
        """
        Retrieve active extraction results for a document-definition field.
        """

        statement = (
            select(DocumentExtractionResult)
            .where(
                DocumentExtractionResult.tenant_id == tenant_id,
                DocumentExtractionResult.document_definition_field_id == document_definition_field_id,
                DocumentExtractionResult.deleted_at.is_(None),
            )
            .order_by(
                DocumentExtractionResult.extracted_at.desc(),
                DocumentExtractionResult.created_at.desc(),
            )
        )

        return list(
            self._session.scalars(statement).all(),
        )
