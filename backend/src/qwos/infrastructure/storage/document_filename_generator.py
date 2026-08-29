"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Document Filename Generator

File:
    document_filename_generator.py

Description:
    Generates standardized QWOS employee-document filenames.

Naming Standard:

    {EMPLOYEE_NUMBER}_{DOCUMENT_CATEGORY}_{ISSUE_DATE}_{EXPIRY_DATE}_{VERSION}.{EXT}

Examples:

    QW-00002_RESIDENCE-VISA_2026-08-16_2027-08-15_V01.pdf
    QW-00002_WORK-PERMIT_2026-08-16_2027-08-15_V01.pdf
    QW-00002_PASSPORT_2024-03-10_2034-03-09_V01.pdf
    QW-00002_EMPLOYMENT-CONTRACT_2026-02-01_V01.pdf

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import re
from datetime import date


class QWOSDocumentFilenameGenerator:
    """
    Generates standardized QWOS document filenames.
    """

    def generate(
        self,
        *,
        employee_number: str,
        document_category: str,
        issue_date: date | None,
        expiry_date: date | None,
        version: int,
        extension: str,
    ) -> str:
        """
        Generate a standardized QWOS document filename.
        """

        if version <= 0:
            raise ValueError("version must be greater than zero.")

        normalized_employee_number = self._normalize_token(
            employee_number,
        )

        normalized_category = self._normalize_token(
            document_category,
        )

        normalized_extension = extension.strip().lower().lstrip(".")

        if not normalized_extension:
            raise ValueError("extension is required.")

        parts = [
            normalized_employee_number,
            normalized_category,
        ]

        if issue_date is not None:
            parts.append(
                issue_date.isoformat(),
            )

        if expiry_date is not None:
            parts.append(
                expiry_date.isoformat(),
            )

        parts.append(
            f"V{version:02d}",
        )

        return f"{'_'.join(parts)}.{normalized_extension}"

    @staticmethod
    def _normalize_token(value: str) -> str:
        """
        Normalize a value for use in a QWOS filename.
        """

        normalized = value.strip().upper()

        normalized = re.sub(
            r"[^A-Z0-9]+",
            "-",
            normalized,
        )

        normalized = normalized.strip("-")

        if not normalized:
            raise ValueError("Filename token cannot be empty.")

        return normalized
