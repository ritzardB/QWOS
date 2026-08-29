"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Document Intelligence

File:
    national_id_ae_extractor.py

Description:
    United Arab Emirates National ID extraction strategy.

    Extracts configured National ID fields from PaddleOCR text.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import re
from datetime import date

from qwos.application.common.ports.document_intelligence import (
    DocumentClassification,
    DocumentExtraction,
    ExtractedDocumentField,
)
from qwos.application.common.ports.document_ocr import OCRTextResult


class NationalIdAEExtractor:
    """
    Extract fields from UAE National ID OCR output.
    """

    COUNTRY_CODE = "AE"
    DOCUMENT_FAMILY = "national id"

    _ID_NUMBER_PATTERN = re.compile(
        r"ID\s*Number\s*/?\s*[:/]?\s*"
        r"(?P<value>\d{3}-\d{4}-\d{7}-\d)",
        re.IGNORECASE,
    )

    _NAME_PATTERN = re.compile(
        r"Name\s*:\s*(?P<value>[^\n]+)",
        re.IGNORECASE,
    )

    _DATE_OF_BIRTH_PATTERN = re.compile(
        r"Date\s+of\s+Birth\s*:\s*"
        r"(?P<value>\d{2}/\d{2}/\d{4})",
        re.IGNORECASE,
    )

    _NATIONALITY_PATTERN = re.compile(
        r"Nationality\s*:\s*(?P<value>[^\n]+)",
        re.IGNORECASE,
    )

    _ISSUE_DATE_PATTERN = re.compile(
        r"Issuing\s+Date\s*/\s*"
        r"(?P<value>\d{2}/\d{2}/\d{4})",
        re.IGNORECASE,
    )

    _EXPIRY_DATE_PATTERN = re.compile(
        r"Expiry\s+Date\s*/\s*"
        r"(?P<value>\d{2}/\d{2}(?:/\d{4})?)",
        re.IGNORECASE,
    )

    _MRZ_PATTERN = re.compile(
        r"(?m)^(?P<value>"
        r"\d{6}"
        r"[MFXO]"
        r"\d{6}"
        r"\d"
        r"[A-Z]{3}"
        r")",
    )

    def extract(
        self,
        *,
        ocr_result: OCRTextResult,
    ) -> DocumentExtraction:
        """
        Extract configured National ID fields from OCR text.
        """

        text = ocr_result.text

        fields = (
            self._extract_document_number(text),
            self._extract_full_name(text),
            self._extract_date_of_birth(text),
            self._extract_nationality(text),
            self._extract_issue_date(text),
            self._extract_expiry_date(
                text,
            ),
        )

        return DocumentExtraction(
            classification=DocumentClassification(
                document_family=self.DOCUMENT_FAMILY,
                country_code=self.COUNTRY_CODE,
                confidence=ocr_result.confidence,
            ),
            fields=tuple(field for field in fields if field is not None),
        )

    def _extract_document_number(
        self,
        text: str,
    ) -> ExtractedDocumentField | None:
        match = self._ID_NUMBER_PATTERN.search(text)

        if not match:
            return None

        value = match.group("value").strip()

        return ExtractedDocumentField(
            field_code="document_number",
            raw_value=value,
            normalized_value=value,
            confidence=None,
            source="paddleocr",
        )

    def _extract_full_name(
        self,
        text: str,
    ) -> ExtractedDocumentField | None:
        match = self._NAME_PATTERN.search(text)

        if not match:
            return None

        value = self._normalize_name(
            match.group("value"),
        )

        return ExtractedDocumentField(
            field_code="full_name",
            raw_value=match.group("value").strip(),
            normalized_value=value,
            confidence=None,
            source="paddleocr",
        )

    def _extract_date_of_birth(
        self,
        text: str,
    ) -> ExtractedDocumentField | None:
        match = self._DATE_OF_BIRTH_PATTERN.search(text)

        if not match:
            return None

        value = self._normalize_date(
            match.group("value"),
        )

        return ExtractedDocumentField(
            field_code="date_of_birth",
            raw_value=match.group("value").strip(),
            normalized_value=value,
            confidence=None,
            source="paddleocr",
        )

    def _extract_nationality(
        self,
        text: str,
    ) -> ExtractedDocumentField | None:
        match = self._NATIONALITY_PATTERN.search(text)

        if not match:
            return None

        raw_value = match.group("value").strip()

        return ExtractedDocumentField(
            field_code="nationality",
            raw_value=raw_value,
            normalized_value=raw_value,
            confidence=None,
            source="paddleocr",
        )

    def _extract_issue_date(
        self,
        text: str,
    ) -> ExtractedDocumentField | None:
        match = self._ISSUE_DATE_PATTERN.search(text)

        if not match:
            return None

        value = self._normalize_date(
            match.group("value"),
        )

        return ExtractedDocumentField(
            field_code="issue_date",
            raw_value=match.group("value").strip(),
            normalized_value=value,
            confidence=None,
            source="paddleocr",
        )

    def _extract_expiry_date(
        self,
        text: str,
    ) -> ExtractedDocumentField | None:
        match = self._EXPIRY_DATE_PATTERN.search(text)

        if match:
            raw_value = match.group("value").strip()

            if len(raw_value) == 10:
                normalized = self._normalize_date(
                    raw_value,
                )

                return ExtractedDocumentField(
                    field_code="expiry_date",
                    raw_value=raw_value,
                    normalized_value=normalized,
                    confidence=None,
                    source="paddleocr",
                )

        mrz_match = self._MRZ_PATTERN.search(text)

        if not mrz_match:
            return None

        mrz = mrz_match.group("value")

        expiry_raw = mrz[7:13]

        normalized = self._normalize_mrz_date(
            expiry_raw,
        )

        if normalized is None:
            return None

        return ExtractedDocumentField(
            field_code="expiry_date",
            raw_value=expiry_raw,
            normalized_value=normalized,
            confidence=None,
            source="paddleocr",
        )

    @staticmethod
    def _normalize_date(
        value: str,
    ) -> str:
        parsed = date.fromisoformat(
            "-".join(
                (
                    value[6:10],
                    value[3:5],
                    value[0:2],
                ),
            ),
        )

        return parsed.isoformat()

    @staticmethod
    def _normalize_mrz_date(
        value: str,
    ) -> str | None:
        if not re.fullmatch(
            r"\d{6}",
            value,
        ):
            return None

        year = 2000 + int(value[0:2])
        month = int(value[2:4])
        day = int(value[4:6])

        try:
            return date(
                year,
                month,
                day,
            ).isoformat()
        except ValueError:
            return None

    @staticmethod
    def _normalize_name(
        value: str,
    ) -> str:
        return " ".join(
            value.strip().split(),
        )
