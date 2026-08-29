"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Document Intelligence

File:
    national_id_document_intelligence.py

Description:
    Generic National ID document-intelligence implementation.

    Routes country-specific National ID extraction strategies while keeping
    the QWOS document family generic.

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
from qwos.infrastructure.document_intelligence.national_id.national_id_ae_extractor import (
    NationalIdAEExtractor,
)


class NationalIdDocumentIntelligence:
    """
    National ID DocumentIntelligence implementation.
    """

    DOCUMENT_FAMILY = "national id"

    def __init__(
        self,
        *,
        ocr: DocumentOCR,
        ae_extractor: NationalIdAEExtractor | None = None,
    ) -> None:
        self._ocr = ocr
        self._ae_extractor = ae_extractor or NationalIdAEExtractor()

    def _extract_ocr(
        self,
        *,
        content: bytes,
        filename: str,
        mime_type: str | None,
    ):
        return self._ocr.extract_text(
            content=content,
            filename=filename,
            mime_type=mime_type,
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
        Classify a National ID document.
        """

        self._validate_document_family(
            document_family,
        )

        ocr_result = self._extract_ocr(
            content=content,
            filename=filename,
            mime_type=mime_type,
        )

        return DocumentClassification(
            document_family=self.DOCUMENT_FAMILY,
            country_code=self._detect_country(
                ocr_result.text,
            ),
            confidence=ocr_result.confidence,
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
        Extract structured National ID fields.
        """

        self._validate_document_family(
            document_family,
        )

        normalized_country = country_code.strip().upper() if country_code else None

        ocr_result = self._extract_ocr(
            content=content,
            filename=filename,
            mime_type=mime_type,
        )

        detected_country = self._detect_country(
            ocr_result.text,
        )

        effective_country = normalized_country or detected_country

        if effective_country == "AE":
            extraction = self._ae_extractor.extract(
                ocr_result=ocr_result,
            )

            return DocumentExtraction(
                classification=DocumentClassification(
                    document_family=self.DOCUMENT_FAMILY,
                    country_code="AE",
                    confidence=ocr_result.confidence,
                ),
                fields=extraction.fields,
            )

        raise ValueError(
            f"No National ID extraction strategy is registered for country code '{effective_country}'.",
        )

    @staticmethod
    def _validate_document_family(
        document_family: str | None,
    ) -> None:
        if document_family is not None and document_family.strip().lower() != "national id":
            raise ValueError(
                "NationalIdDocumentIntelligence only supports the national id document family.",
            )

    @staticmethod
    def _detect_country(
        text: str,
    ) -> str | None:
        normalized = text.upper()

        if "UNITEDARABEMIRATES" in normalized or "UNITEDARABEMIRATES" in normalized:
            return "AE"

        return None
