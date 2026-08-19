"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    employee_document_mapper.py

Description:
    Maps employee document API contracts to application objects.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.requests.hr.upload_employee_document_request import (
    UploadEmployeeDocumentRequest,
)
from qwos.api.contracts.responses.hr.upload_employee_document_response import (
    UploadEmployeeDocumentResponse,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.hr.commands.upload_employee_document_command import (
    UploadEmployeeDocumentCommand,
)
from qwos.application.hr.responses.upload_employee_document_response import (
    UploadEmployeeDocumentResponse as ApplicationUploadEmployeeDocumentResponse,
)


class EmployeeDocumentMapper:
    """
    Maps Employee Document application objects to API contracts.
    """

    @staticmethod
    def to_upload_command(
        *,
        employee_id: str,
        request: UploadEmployeeDocumentRequest,
        content: bytes,
        original_filename: str,
        mime_type: str | None,
        file_extension: str,
        request_context: RequestContext,
    ) -> UploadEmployeeDocumentCommand:
        """
        Convert multipart upload data into an application command.
        """

        return UploadEmployeeDocumentCommand(
            tenant_id=request_context.tenant_id,
            employee_id=employee_id,
            document_name=request.document_name,
            document_category=request.document_category,
            original_filename=original_filename,
            mime_type=mime_type,
            file_extension=file_extension,
            content=content,
            immigration_id=request.immigration_id,
        )

    @staticmethod
    def to_upload_response(
        response: ApplicationUploadEmployeeDocumentResponse,
    ) -> UploadEmployeeDocumentResponse:
        """
        Convert an application response into an API response.
        """

        return UploadEmployeeDocumentResponse(
            id=response.id,
            employee_id=response.employee_id,
            immigration_id=response.immigration_id,
            document_name=response.document_name,
            document_category=response.document_category,
            original_filename=response.original_filename,
            stored_filename=response.stored_filename,
            mime_type=response.mime_type,
            file_extension=response.file_extension,
            file_size_bytes=response.file_size_bytes,
            storage_provider=response.storage_provider,
            storage_key=response.storage_key,
            checksum_sha256=response.checksum_sha256,
            document_version=response.document_version,
        )