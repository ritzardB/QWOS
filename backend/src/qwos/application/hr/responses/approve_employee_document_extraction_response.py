"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    approve_employee_document_extraction_response.py

Description:
    Response returned after approved document extraction values are applied.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApprovedEmployeeDocumentField:
    """
    A successfully approved extraction field.
    """

    extraction_result_id: str
    field_code: str
    target_entity: str
    target_field: str
    value: str | None


@dataclass(frozen=True, slots=True)
class ApproveEmployeeDocumentExtractionResponse:
    """
    Result of an approved document extraction.
    """

    document_id: str
    employee_id: str
    approved_fields: tuple[
        ApprovedEmployeeDocumentField,
        ...,
    ]
