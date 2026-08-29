"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    get_employee_document_content_use_case.py

Description:
    Retrieves the physical content of an employee document after authorization
    and tenant/employee validation.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.forbidden_exception import (
    ForbiddenException,
)
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.common.ports.document_storage import (
    DocumentStorage,
)
from qwos.application.hr.responses.get_employee_document_content_response import (
    GetEmployeeDocumentContentResponse,
)
from qwos.domains.hr.repositories.employee_document_repository import (
    EmployeeDocumentRepository,
)
from qwos.domains.identity.services.authorization_service import (
    AuthorizationService,
)


class GetEmployeeDocumentContentUseCase:
    """
    Retrieve the physical content of an employee document.
    """

    REQUIRED_PERMISSION = "HR_DOCUMENT_VIEW"

    def __init__(
        self,
        *,
        employee_document_repository: EmployeeDocumentRepository,
        authorization_service: AuthorizationService,
        document_storage: DocumentStorage,
        request_context: RequestContext,
    ) -> None:
        self._employee_document_repository = employee_document_repository
        self._authorization_service = authorization_service
        self._document_storage = document_storage
        self._request_context = request_context

    async def execute(
        self,
        *,
        employee_id: str,
        document_id: str,
    ) -> GetEmployeeDocumentContentResponse:
        """
        Retrieve document content for an authorized employee request.
        """

        tenant_id = self._request_context.tenant_id
        user_id = self._request_context.user_id

        allowed = await self._authorization_service.has_permission(
            tenant_id=tenant_id,
            user_id=user_id,
            permission_code=self.REQUIRED_PERMISSION,
        )

        if not allowed:
            raise ForbiddenException(
                message=("User is not authorized to view employee documents."),
            )

        document = self._employee_document_repository.get_by_id(
            document_id,
        )

        if document is None:
            raise ResourceNotFoundException(
                resource="EmployeeDocument",
                identifier=document_id,
            )

        if document.tenant_id != tenant_id:
            raise ResourceNotFoundException(
                resource="EmployeeDocument",
                identifier=document_id,
            )

        if document.employee_id != employee_id:
            raise ResourceNotFoundException(
                resource="EmployeeDocument",
                identifier=document_id,
            )

        if document.deleted_at is not None:
            raise ResourceNotFoundException(
                resource="EmployeeDocument",
                identifier=document_id,
            )

        stored_document = self._document_storage.read(
            storage_key=document.storage_key,
        )

        return GetEmployeeDocumentContentResponse(
            id=document.id,
            employee_id=document.employee_id,
            filename=document.original_filename,
            mime_type=document.mime_type,
            content=stored_document.content,
        )
