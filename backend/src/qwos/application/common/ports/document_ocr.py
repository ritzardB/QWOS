"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Port

File:
    document_ocr.py

Description:
    Abstraction for optical character recognition of employee documents.

Responsibilities:
    - Convert document content into OCR text
    - Remain independent of a specific OCR provider
    - Provide a stable contract for document intelligence infrastructure

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class OCRTextResult:
    """
    Result returned by an OCR implementation.
    """

    text: str
    source: str
    confidence: float | None = None


class DocumentOCR(Protocol):
    """
    Port for document OCR implementations.

    Implementations may use:
        - local OCR engines
        - cloud OCR services
        - AI vision models
        - other document recognition providers
    """

    def extract_text(
        self,
        *,
        content: bytes,
        filename: str,
        mime_type: str | None = None,
    ) -> OCRTextResult:
        """
        Extract textual content from a document.
        """
        ...
