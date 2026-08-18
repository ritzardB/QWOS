"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Document Storage Key Generator

File:
    document_storage_key_generator.py

Description:
    Generates standardized QWOS document storage keys.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import re


class QWOSDocumentStorageKeyGenerator:
    """
    Generates standardized QWOS document storage keys.
    """

    def generate(
        self,
        *,
        employee_number: str,
        document_category: str,
        stored_filename: str,
    ) -> str:
        employee_token = self._normalize_token(
            employee_number,
        )

        category_token = self._normalize_token(
            document_category,
        )

        filename = stored_filename.strip()

        if not filename:
            raise ValueError(
                "stored_filename is required."
            )

        return (
            f"employees/{employee_token}/"
            f"documents/{category_token.lower()}/"
            f"{filename}"
        )

    @staticmethod
    def _normalize_token(value: str) -> str:
        normalized = value.strip().upper()

        normalized = re.sub(
            r"[^A-Z0-9]+",
            "-",
            normalized,
        )

        normalized = normalized.strip("-")

        if not normalized:
            raise ValueError(
                "Storage key token cannot be empty."
            )

        return normalized