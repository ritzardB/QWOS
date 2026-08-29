"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    extract_employee_document_response.py

Description:
    Response returned after document data has been extracted.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExtractedEmployeeDocumentField:
    """
    A single extracted document field.
    """

    extraction_result_id: str
    field_code: str
    raw_value: str | None
    normalized_value: str | None
    confidence: float | None
    source: str
    is_hr_updateable: bool
    target_entity: str | None
    target_field: str | None


@dataclass(frozen=True, slots=True)
class ExtractEmployeeDocumentResponse:
    """
    Result returned after document extraction.
    """

    document_id: str
    employee_id: str
    document_family: str
    country_code: str | None
    fields: tuple[ExtractedEmployeeDocumentField, ...]
