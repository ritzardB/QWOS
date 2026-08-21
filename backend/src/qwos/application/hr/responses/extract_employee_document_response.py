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


@dataclass(frozen=True, slots=True)
class ExtractEmployeeDocumentResponse:
    """
    Extraction candidates produced from an employee document.

    These values are extraction evidence and are not yet approved HR data.
    """

    document_id: str
    employee_id: str
    document_family: str
    country_code: str | None
    fields: tuple[ExtractedEmployeeDocumentField, ...]