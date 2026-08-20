"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

File:
    document_extraction_result_repository.py

Description:
    Repository contract for document extraction results.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from qwos.domains.hr.models.document_extraction_result import (
    DocumentExtractionResult,
)


class DocumentExtractionResultRepository(Protocol):
    """
    Contract for DocumentExtractionResult persistence.
    """

    def get_by_id(
        self,
        result_id: str,
    ) -> DocumentExtractionResult | None:
        """
        Retrieve an extraction result by identifier.
        """
        ...

    def save(
        self,
        result: DocumentExtractionResult,
    ) -> None:
        """
        Persist an extraction result.
        """
        ...

    def list_by_document_id(
        self,
        *,
        tenant_id: str,
        employee_document_id: str,
    ) -> list[DocumentExtractionResult]:
        """
        Retrieve extraction results for an employee document.
        """
        ...

    def list_by_field_id(
        self,
        *,
        tenant_id: str,
        document_definition_field_id: str,
    ) -> list[DocumentExtractionResult]:
        """
        Retrieve extraction results for a document-definition field.
        """
        ...