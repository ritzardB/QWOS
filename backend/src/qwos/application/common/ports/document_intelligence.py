"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Port

File:
    document_intelligence.py

Description:
    Abstraction for document classification and field extraction.

Responsibilities:
    - Classify document content
    - Extract structured fields
    - Return normalized extraction candidates
    - Remain independent of any OCR or AI provider

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class DocumentClassification:
    """
    Result returned after document classification.
    """

    document_family: str
    country_code: str | None
    confidence: float | None


@dataclass(frozen=True)
class ExtractedDocumentField:
    """
    A single field extracted from a document.
    """

    field_code: str
    raw_value: str | None
    normalized_value: str | None
    confidence: float | None
    source: str


@dataclass(frozen=True)
class DocumentExtraction:
    """
    Result returned after document field extraction.
    """

    classification: DocumentClassification
    fields: tuple[ExtractedDocumentField, ...]


class DocumentIntelligence(Protocol):
    """
    Port for document intelligence implementations.

    Implementations may use OCR, MRZ parsing, AI vision models,
    cloud document-intelligence services, or other techniques.
    """

    def classify(
        self,
        *,
        content: bytes,
        filename: str,
        mime_type: str | None = None,
        document_family: str | None = None,
    ) -> DocumentClassification:
        """
        Classify the supplied document.
        """
        ...

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
        Extract structured fields from the supplied document.
        """
        ...