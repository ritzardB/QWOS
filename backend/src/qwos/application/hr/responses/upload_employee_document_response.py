"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    upload_employee_document_response.py

Description:
    Response returned after uploading an employee document.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations


class UploadEmployeeDocumentResponse:
    """
    Response returned after an employee document upload.
    """

    def __init__(
        self,
        *,
        id: str,
        employee_id: str,
        immigration_id: str | None,
        document_name: str,
        document_category: str,
        original_filename: str,
        stored_filename: str,
        mime_type: str | None,
        file_extension: str | None,
        file_size_bytes: int,
        storage_provider: str,
        storage_key: str,
        checksum_sha256: str,
        document_version: int,
    ) -> None:
        self.id = id
        self.employee_id = employee_id
        self.immigration_id = immigration_id
        self.document_name = document_name
        self.document_category = document_category
        self.original_filename = original_filename
        self.stored_filename = stored_filename
        self.mime_type = mime_type
        self.file_extension = file_extension
        self.file_size_bytes = file_size_bytes
        self.storage_provider = storage_provider
        self.storage_key = storage_key
        self.checksum_sha256 = checksum_sha256
        self.document_version = document_version