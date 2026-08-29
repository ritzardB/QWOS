"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

HR Module

File:
    approve_employee_document_extraction_request.py

Description:
    API request contract for approving employee document extraction results.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import BaseModel


class ApprovedEmployeeDocumentFieldRequest(BaseModel):
    """
    A field value explicitly confirmed by the reviewer.
    """

    extraction_result_id: str
    value: str | None


class ApproveEmployeeDocumentExtractionRequest(BaseModel):
    """
    Human-confirmed employee document extraction values.
    """

    fields: list[ApprovedEmployeeDocumentFieldRequest]
