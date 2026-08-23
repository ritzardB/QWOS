"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    approve_employee_document_extraction_command.py

Description:
    Command for approving employee document extraction results.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ApprovedEmployeeDocumentField:
    """
    A field explicitly confirmed by the human reviewer.
    """

    extraction_result_id: str
    value: str | None


@dataclass(frozen=True)
class ApproveEmployeeDocumentExtractionCommand:
    """
    Command for approving extraction evidence for an employee document.
    """

    tenant_id: str
    employee_id: str
    document_id: str
    fields: tuple[
        ApprovedEmployeeDocumentField,
        ...,
    ]