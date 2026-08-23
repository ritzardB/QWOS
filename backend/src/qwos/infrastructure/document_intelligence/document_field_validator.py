"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Document Intelligence

File:
    document_field_validator.py

Description:
    Validates extracted document values against configured
    DocumentDefinitionField validation patterns.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import re


class DocumentFieldValidator:
    """
    Validate extracted document values against configured patterns.
    """

    @staticmethod
    def matches(
        *,
        value: str | None,
        validation_pattern: str | None,
    ) -> bool:
        """
        Return True when the value matches the configured pattern.

        Fields without a validation pattern are considered valid.
        """

        if value is None:
            return False

        normalized_value = value.strip()

        if not normalized_value:
            return False

        if not validation_pattern:
            return True

        if not isinstance(
            validation_pattern,
            str,
        ):
            raise ValueError(
                "Document field validation pattern must be a string.",
            )

        try:
            return (
                re.fullmatch(
                    validation_pattern,
                    normalized_value,
                )
                is not None
            )
        except re.error as exc:
            raise ValueError(
                "Invalid document field validation pattern: "
                f"{validation_pattern}",
            ) from exc