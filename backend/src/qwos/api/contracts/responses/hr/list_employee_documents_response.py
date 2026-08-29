from __future__ import annotations

from pydantic import BaseModel


class EmployeeDocumentItemResponse(BaseModel):
    id: str
    employee_id: str
    immigration_id: str | None
    document_name: str
    document_category: str
    original_filename: str
    stored_filename: str
    mime_type: str | None
    file_extension: str | None
    file_size_bytes: int
    storage_provider: str
    storage_key: str
    checksum_sha256: str
    document_version: int


class ListEmployeeDocumentsResponse(BaseModel):
    items: list[EmployeeDocumentItemResponse]
