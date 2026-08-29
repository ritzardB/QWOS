"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    employee_document_mapper.py

Description:
    Maps employee document application objects to API contracts.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.requests.hr.approve_employee_document_extraction_request import (
    ApproveEmployeeDocumentExtractionRequest,
)
from qwos.api.contracts.requests.hr.upload_employee_document_request import (
    UploadEmployeeDocumentRequest,
)
from qwos.api.contracts.responses.hr.approve_employee_document_extraction_response import (
    ApprovedEmployeeDocumentFieldResponse,
    ApproveEmployeeDocumentExtractionResponse,
)
from qwos.api.contracts.responses.hr.extract_employee_document_response import (
    ExtractedEmployeeDocumentFieldResponse,
    ExtractEmployeeDocumentResponse,
)
from qwos.api.contracts.responses.hr.list_employee_documents_response import (
    EmployeeDocumentItemResponse,
    ListEmployeeDocumentsResponse,
)
from qwos.api.contracts.responses.hr.upload_employee_document_response import (
    UploadEmployeeDocumentResponse,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.hr.commands.approve_employee_document_extraction_command import (
    ApprovedEmployeeDocumentField,
    ApproveEmployeeDocumentExtractionCommand,
)
from qwos.application.hr.commands.upload_employee_document_command import (
    UploadEmployeeDocumentCommand,
)
from qwos.application.hr.responses.approve_employee_document_extraction_response import (
    ApproveEmployeeDocumentExtractionResponse as ApplicationApproveEmployeeDocumentExtractionResponse,
)
from qwos.application.hr.responses.extract_employee_document_response import (
    ExtractEmployeeDocumentResponse as ApplicationExtractEmployeeDocumentResponse,
)
from qwos.application.hr.responses.list_employee_documents_response import (
    ListEmployeeDocumentsResponse as ApplicationListEmployeeDocumentsResponse,
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
        Convert an application upload response into an API response.
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

    @staticmethod
    def to_list_response(
        response: ApplicationListEmployeeDocumentsResponse,
    ) -> ListEmployeeDocumentsResponse:
        """
        Convert an application document-list response into an API response.
        """

        return ListEmployeeDocumentsResponse(
            items=[
                EmployeeDocumentItemResponse(
                    id=item.id,
                    employee_id=item.employee_id,
                    immigration_id=item.immigration_id,
                    document_name=item.document_name,
                    document_category=item.document_category,
                    original_filename=item.original_filename,
                    stored_filename=item.stored_filename,
                    mime_type=item.mime_type,
                    file_extension=item.file_extension,
                    file_size_bytes=item.file_size_bytes,
                    storage_provider=item.storage_provider,
                    storage_key=item.storage_key,
                    checksum_sha256=item.checksum_sha256,
                    document_version=item.document_version,
                )
                for item in response.items
            ],
        )

    @staticmethod
    def to_extract_response(
        response: ApplicationExtractEmployeeDocumentResponse,
    ) -> ExtractEmployeeDocumentResponse:
        """
        Map application extraction response to API response.
        """

        return ExtractEmployeeDocumentResponse(
            document_id=response.document_id,
            employee_id=response.employee_id,
            document_family=response.document_family,
            country_code=response.country_code,
            fields=[
                ExtractedEmployeeDocumentFieldResponse(
                    extraction_result_id=field.extraction_result_id,
                    field_code=field.field_code,
                    raw_value=field.raw_value,
                    normalized_value=field.normalized_value,
                    confidence=field.confidence,
                    source=field.source,
                    is_hr_updateable=field.is_hr_updateable,
                    target_entity=field.target_entity,
                    target_field=field.target_field,
                )
                for field in response.fields
            ],
        )

    @staticmethod
    def to_approve_command(
        *,
        employee_id: str,
        document_id: str,
        request: ApproveEmployeeDocumentExtractionRequest,
        request_context: RequestContext,
    ) -> ApproveEmployeeDocumentExtractionCommand:
        """
        Convert an API approval request into an application command.
        """

        return ApproveEmployeeDocumentExtractionCommand(
            tenant_id=request_context.tenant_id,
            employee_id=employee_id,
            document_id=document_id,
            fields=tuple(
                ApprovedEmployeeDocumentField(
                    extraction_result_id=field.extraction_result_id,
                    value=field.value,
                )
                for field in request.fields
            ),
        )

    @staticmethod
    def to_approve_response(
        response: ApplicationApproveEmployeeDocumentExtractionResponse,
    ) -> ApproveEmployeeDocumentExtractionResponse:
        """
        Convert the application approval response into an API response.
        """

        return ApproveEmployeeDocumentExtractionResponse(
            document_id=response.document_id,
            employee_id=response.employee_id,
            approved_fields=[
                ApprovedEmployeeDocumentFieldResponse(
                    extraction_result_id=field.extraction_result_id,
                    field_code=field.field_code,
                    target_entity=field.target_entity,
                    target_field=field.target_field,
                    value=field.value,
                )
                for field in response.approved_fields
            ],
        )
