"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Document Intelligence

File:
    passport_document_intelligence.py

Description:
    Passport implementation of the QWOS DocumentIntelligence port.

Responsibilities:
    - Run OCR against passport documents
    - Detect the passport MRZ
    - Parse and validate passport MRZ fields
    - Return normalized extraction results

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.ports.document_intelligence import (
    DocumentClassification,
    DocumentExtraction,
)
from qwos.application.common.ports.document_ocr import (
    DocumentOCR,
)
from qwos.infrastructure.document_intelligence.passport.passport_mrz_detector import (
    PassportMRZDetector,
)
from qwos.infrastructure.document_intelligence.passport.passport_mrz_parser import (
    PassportMRZParser,
)


class PassportDocumentIntelligence:
    """
    Passport DocumentIntelligence implementation.

    Pipeline:

        Document
            ↓
        OCR
            ↓
        MRZ Detection
            ↓
        MRZ Parsing
            ↓
        DocumentExtraction
    """

    def __init__(
        self,
        *,
        ocr: DocumentOCR,
        detector: PassportMRZDetector | None = None,
        parser: PassportMRZParser | None = None,
    ) -> None:
        self._ocr = ocr
        self._detector = detector or PassportMRZDetector()
        self._parser = parser or PassportMRZParser()

    def _extract_mrz(
        self,
        *,
        content: bytes,
        filename: str,
        mime_type: str | None,
    ) -> DocumentExtraction:
        """
        Execute the complete passport OCR → MRZ pipeline.
        """

        ocr_result = self._ocr.extract_text(
            content=content,
            filename=filename,
            mime_type=mime_type,
        )

        mrz = self._detector.detect(
            ocr_result.text,
        )

        return self._parser.parse(
            mrz,
        )

    def classify(
        self,
        *,
        content: bytes,
        filename: str,
        mime_type: str | None = None,
        document_family: str | None = None,
    ) -> DocumentClassification:
        """
        Classify a passport document.
        """

        extraction = self._extract_mrz(
            content=content,
            filename=filename,
            mime_type=mime_type,
        )

        return extraction.classification

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
        Extract structured passport fields.
        """

        if document_family is not None and document_family.strip().lower() != "passport":
            raise ValueError(
                "PassportDocumentIntelligence only supports the passport document family.",
            )

        extraction = self._extract_mrz(
            content=content,
            filename=filename,
            mime_type=mime_type,
        )

        if country_code is not None and extraction.classification.country_code != country_code.strip().upper():
            raise ValueError(
                "Passport MRZ country does not match the requested country code.",
            )

        return extraction
