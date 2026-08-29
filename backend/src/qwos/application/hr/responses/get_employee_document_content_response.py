"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    get_employee_document_content_response.py

Description:
    Response returned when retrieving the physical content of an employee
    document.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetEmployeeDocumentContentResponse:
    """
    Response containing employee document content and metadata.
    """

    id: str
    employee_id: str
    filename: str
    mime_type: str | None
    content: bytes
