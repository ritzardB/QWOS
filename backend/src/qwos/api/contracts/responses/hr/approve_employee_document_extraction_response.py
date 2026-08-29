"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

HR Module

File:
    approve_employee_document_extraction_response.py

Description:
    API response contract for approved employee document extraction.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import BaseModel


class ApprovedEmployeeDocumentFieldResponse(BaseModel):
    """
    A successfully approved document field.
    """

    extraction_result_id: str
    field_code: str
    target_entity: str
    target_field: str
    value: str | None


class ApproveEmployeeDocumentExtractionResponse(BaseModel):
    """
    Result returned after human-confirmed extraction values are applied.
    """

    document_id: str
    employee_id: str
    approved_fields: list[ApprovedEmployeeDocumentFieldResponse]
