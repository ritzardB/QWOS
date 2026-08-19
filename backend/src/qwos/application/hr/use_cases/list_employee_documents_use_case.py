from __future__ import annotations

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.forbidden_exception import (
    ForbiddenException,
)
from qwos.application.hr.responses.list_employee_documents_response import (
    EmployeeDocumentItem,
    ListEmployeeDocumentsResponse,
)
from qwos.domains.hr.repositories.employee_document_repository import (
    EmployeeDocumentRepository,
)
from qwos.domains.identity.services.authorization_service import (
    AuthorizationService,
)


class ListEmployeeDocumentsUseCase:
    """
    Retrieve documents for an employee.
    """

    REQUIRED_PERMISSION = "HR_DOCUMENT_VIEW"

    def __init__(
        self,
        *,
        employee_document_repository: EmployeeDocumentRepository,
        authorization_service: AuthorizationService,
        request_context: RequestContext,
    ) -> None:
        self._employee_document_repository = (
            employee_document_repository
        )
        self._authorization_service = authorization_service
        self._request_context = request_context

    async def execute(
        self,
        *,
        employee_id: str,
        document_category: str | None = None,
    ) -> ListEmployeeDocumentsResponse:
        tenant_id = self._request_context.tenant_id
        user_id = self._request_context.user_id

        allowed = await self._authorization_service.has_permission(
            tenant_id=tenant_id,
            user_id=user_id,
            permission_code=self.REQUIRED_PERMISSION,
        )

        if not allowed:
            raise ForbiddenException(
                message="User is not authorized to view employee documents.",
            )

        records = self._employee_document_repository.list_by_employee_id(
            tenant_id=tenant_id,
            employee_id=employee_id,
            document_category=document_category,
        )

        return ListEmployeeDocumentsResponse(
            items=[
                EmployeeDocumentItem(
                    id=record.id,
                    employee_id=record.employee_id,
                    immigration_id=record.immigration_id,
                    document_name=record.document_name,
                    document_category=record.document_category,
                    original_filename=record.original_filename,
                    stored_filename=record.stored_filename,
                    mime_type=record.mime_type,
                    file_extension=record.file_extension,
                    file_size_bytes=record.file_size_bytes,
                    storage_provider=record.storage_provider,
                    storage_key=record.storage_key,
                    checksum_sha256=record.checksum_sha256,
                    document_version=record.document_version,
                )
                for record in records
            ],
        )