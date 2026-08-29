"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Document Intelligence

File:
    document_intelligence_router.py

Description:
    Routes document-intelligence operations to the implementation
    registered for the requested document family.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.ports.document_intelligence import (
    DocumentClassification,
    DocumentExtraction,
    DocumentIntelligence,
)


class DocumentIntelligenceRouter:
    """
    Routes document-intelligence operations by document family.
    """

    def __init__(
        self,
        *,
        implementations: dict[
            str,
            DocumentIntelligence,
        ],
    ) -> None:
        self._implementations = {key.strip().lower(): implementation for key, implementation in implementations.items()}

    def _resolve(
        self,
        document_family: str | None,
    ) -> DocumentIntelligence:
        if not document_family:
            raise ValueError(
                "Document family is required for document intelligence routing.",
            )

        normalized_family = document_family.strip().lower()

        implementation = self._implementations.get(
            normalized_family,
        )

        if implementation is None:
            raise ValueError(
                f"No document intelligence implementation is registered for document family '{normalized_family}'.",
            )

        return implementation

    def classify(
        self,
        *,
        content: bytes,
        filename: str,
        mime_type: str | None = None,
        document_family: str | None = None,
    ) -> DocumentClassification:
        """
        Route document classification.
        """

        implementation = self._resolve(
            document_family,
        )

        return implementation.classify(
            content=content,
            filename=filename,
            mime_type=mime_type,
            document_family=document_family,
        )

    def extract(
        self,
        *,
        content: bytes,
        filename: str,
        mime_type: str | None = None,
        document_family: str | None = None,
        country_code: str | None = None,
    ) -> DocumentExtraction:
        """
        Route document extraction.
        """

        implementation = self._resolve(
            document_family,
        )

        return implementation.extract(
            content=content,
            filename=filename,
            mime_type=mime_type,
            document_family=document_family,
            country_code=country_code,
        )
