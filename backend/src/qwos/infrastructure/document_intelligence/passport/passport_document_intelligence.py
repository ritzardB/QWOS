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
    - Classify passport MRZ content
    - Extract passport fields from MRZ data
    - Adapt PassportMRZParser results to the application port
    - Remain independent of OCR providers

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.ports.document_intelligence import (
    DocumentClassification,
    DocumentExtraction,
)
from qwos.infrastructure.document_intelligence.passport.passport_mrz_parser import (
    PassportMRZParser,
)


class PassportDocumentIntelligence:
    """
    Passport implementation of DocumentIntelligence.

    The current implementation operates on MRZ text that has already been
    extracted from the document.

    OCR/image recognition is intentionally kept outside this adapter so that
    an OCR provider can be introduced later without changing the application
    layer.
    """

    def __init__(
        self,
        *,
        parser: PassportMRZParser | None = None,
    ) -> None:
        self._parser = parser or PassportMRZParser()

    def classify(
        self,
        *,
        content: bytes,
        filename: str,
        mime_type: str | None = None,
    ) -> DocumentClassification:
        """
        Classify passport content from MRZ text.
        """

        mrz = self._decode_mrz_content(
            content,
            mime_type=mime_type,
        )

        extraction = self._parser.parse(
            mrz,
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
        Extract structured passport fields from MRZ text.
        """

        if (
            document_family is not None
            and document_family.strip().lower()
            != "passport"
        ):
            raise ValueError(
                "PassportDocumentIntelligence only supports "
                "the passport document family.",
            )

        mrz = self._decode_mrz_content(
            content,
            mime_type=mime_type,
        )

        extraction = self._parser.parse(
            mrz,
        )

        extracted_country_code = (
            extraction.classification.country_code
        )

        if (
            country_code is not None
            and extracted_country_code
            != country_code.strip().upper()
        ):
            raise ValueError(
                "Passport MRZ country does not match the requested "
                "country code.",
            )

        return extraction

    @staticmethod
    def _decode_mrz_content(
        content: bytes,
        *,
        mime_type: str | None = None,
    ) -> str:
        """
        Decode MRZ text supplied to the adapter.

        The current implementation expects MRZ text as UTF-8.

        Image and PDF documents are intentionally rejected because OCR /
        MRZ detection has not yet been implemented.
        """

        if not content:
            raise ValueError(
                "Document content cannot be empty.",
            )

        normalized_mime_type = (
            mime_type.strip().lower()
            if mime_type
            else None
        )

        if (
            normalized_mime_type == "application/pdf"
            or (
                normalized_mime_type is not None
                and normalized_mime_type.startswith("image/")
            )
        ):
            raise ValueError(
                "Binary image/PDF OCR is not implemented yet.",
            )

        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(
                "Passport MRZ adapter requires MRZ text content. "
                "Binary image/PDF OCR is not implemented yet.",
            ) from exc

        normalized = text.strip()

        if not normalized:
            raise ValueError(
                "Passport MRZ content cannot be empty.",
            )

        return normalized