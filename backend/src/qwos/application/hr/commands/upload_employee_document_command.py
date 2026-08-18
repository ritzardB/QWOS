"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    upload_employee_document_command.py

Description:
    Command representing an employee document upload.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UploadEmployeeDocumentCommand:
    """
    Command for uploading an employee document.
    """

    tenant_id: str
    employee_id: str
    document_name: str
    document_category: str
    original_filename: str
    mime_type: str | None
    file_extension: str
    content: bytes
    immigration_id: str | None = None