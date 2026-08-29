"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

HR Module

File:
    extract_employee_document_response.py

Description:
    API response contract for employee document extraction.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import BaseModel


class ExtractedEmployeeDocumentFieldResponse(BaseModel):
    """
    Extracted document field returned for human review.
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


class ExtractEmployeeDocumentResponse(BaseModel):
    """
    Document extraction response returned to the frontend.
    """

    document_id: str
    employee_id: str
    document_family: str
    country_code: str | None
    fields: list[ExtractedEmployeeDocumentFieldResponse]
