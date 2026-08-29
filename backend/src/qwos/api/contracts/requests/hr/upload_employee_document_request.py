"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

HR Module

File:
    upload_employee_document_request.py

Description:
    Multipart request fields for uploading an employee document.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Form


class UploadEmployeeDocumentRequest:
    """
    Multipart form fields for employee document upload.
    """

    def __init__(
        self,
        document_name: Annotated[str, Form()],
        document_category: Annotated[str, Form()],
        immigration_id: Annotated[str | None, Form()] = None,
    ) -> None:
        self.document_name = document_name
        self.document_category = document_category
        self.immigration_id = immigration_id
