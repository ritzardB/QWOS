"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    upload_employee_document_use_case.py

Description:
    Handles the complete employee-document upload workflow.

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
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.document_filename_generator import (
    DocumentFilenameGenerator,
)
from qwos.application.common.ports.document_storage import DocumentStorage
from qwos.application.common.ports.document_storage_key_generator import (
    DocumentStorageKeyGenerator,
)
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.application.hr.commands.upload_employee_document_command import (
    UploadEmployeeDocumentCommand,
)
from qwos.application.hr.responses.upload_employee_document_response import (
    UploadEmployeeDocumentResponse,
)
from qwos.domains.hr.models.employee_document import EmployeeDocument
from qwos.domains.hr.repositories.employee_document_repository import (
    EmployeeDocumentRepository,
)
from qwos.domains.hr.repositories.employee_immigration_repository import (
    EmployeeImmigrationRepository,
)
from qwos.domains.hr.repositories.employee_repository import (
    EmployeeRepository,
)
from qwos.domains.identity.services.authorization_service import (
    AuthorizationService,
)


class UploadEmployeeDocumentUseCase:
    """
    Use case for uploading an employee document.
    """

    REQUIRED_PERMISSION = "HR_DOCUMENT_UPLOAD"

    def __init__(
        self,
        *,
        employee_repository: EmployeeRepository,
        employee_immigration_repository: EmployeeImmigrationRepository,
        employee_document_repository: EmployeeDocumentRepository,
        authorization_service: AuthorizationService,
        filename_generator: DocumentFilenameGenerator,
        storage_key_generator: DocumentStorageKeyGenerator,
        document_storage: DocumentStorage,
        id_generator: IdGenerator,
        unit_of_work: UnitOfWork,
        request_context: RequestContext,
    ) -> None:
        self._employee_repository = employee_repository
        self._employee_immigration_repository = employee_immigration_repository
        self._employee_document_repository = employee_document_repository
        self._authorization_service = authorization_service
        self._filename_generator = filename_generator
        self._storage_key_generator = storage_key_generator
        self._document_storage = document_storage
        self._id_generator = id_generator
        self._unit_of_work = unit_of_work
        self._request_context = request_context

    async def execute(
        self,
        command: UploadEmployeeDocumentCommand,
    ) -> UploadEmployeeDocumentResponse:
        """
        Upload an employee document.
        """

        tenant_id = self._request_context.tenant_id
        user_id = self._request_context.user_id

        # ------------------------------------------------------------------
        # Authorization
        # ------------------------------------------------------------------

        allowed = await self._authorization_service.has_permission(
            tenant_id=tenant_id,
            user_id=user_id,
            permission_code=self.REQUIRED_PERMISSION,
        )

        if not allowed:
            raise ForbiddenException(
                message=("User is not authorized to upload employee documents."),
            )

        # ------------------------------------------------------------------
        # Employee validation
        # ------------------------------------------------------------------

        employee = self._employee_repository.get_by_id_for_tenant(
            tenant_id=tenant_id,
            employee_id=command.employee_id,
        )

        if employee is None:
            raise ResourceNotFoundException(
                resource="Employee",
                identifier=command.employee_id,
            )

        # ------------------------------------------------------------------
        # Immigration validation
        # ------------------------------------------------------------------

        immigration = None

        if command.immigration_id is not None:
            immigration = self._employee_immigration_repository.get_by_id(
                command.immigration_id,
            )

            if immigration is None:
                raise ResourceNotFoundException(
                    resource="EmployeeImmigration",
                    identifier=command.immigration_id,
                )

            if immigration.tenant_id != tenant_id:
                raise ResourceNotFoundException(
                    resource="EmployeeImmigration",
                    identifier=command.immigration_id,
                )

            if immigration.employee_id != command.employee_id:
                raise ResourceNotFoundException(
                    resource="EmployeeImmigration",
                    identifier=command.immigration_id,
                )

        # ------------------------------------------------------------------
        # Determine document version
        # ------------------------------------------------------------------

        document_version = self._employee_document_repository.get_next_version(
            tenant_id=tenant_id,
            employee_id=command.employee_id,
            document_category=command.document_category,
            immigration_id=command.immigration_id,
        )

        # ------------------------------------------------------------------
        # Generate QWOS filename
        # ------------------------------------------------------------------

        issue_date = immigration.issue_date if immigration is not None else None

        expiry_date = immigration.expiry_date if immigration is not None else None

        stored_filename = self._filename_generator.generate(
            employee_number=employee.employee_number,
            document_category=command.document_category,
            issue_date=issue_date,
            expiry_date=expiry_date,
            version=document_version,
            extension=command.file_extension,
        )

        # ------------------------------------------------------------------
        # Generate storage key
        # ------------------------------------------------------------------

        storage_key = self._storage_key_generator.generate(
            employee_number=employee.employee_number,
            document_category=command.document_category,
            stored_filename=stored_filename,
        )

        # ------------------------------------------------------------------
        # Store physical document
        # ------------------------------------------------------------------

        stored_document = None

        try:
            stored_document = self._document_storage.store(
                content=command.content,
                storage_key=storage_key,
                filename=stored_filename,
                mime_type=command.mime_type,
            )

            # --------------------------------------------------------------
            # Create document metadata
            # --------------------------------------------------------------

            document = EmployeeDocument.create(
                id=self._id_generator.generate(),
                tenant_id=tenant_id,
                employee_id=command.employee_id,
                immigration_id=command.immigration_id,
                document_name=command.document_name,
                document_category=command.document_category,
                original_filename=command.original_filename,
                stored_filename=stored_document.stored_filename,
                mime_type=command.mime_type,
                file_extension=command.file_extension,
                file_size_bytes=stored_document.file_size_bytes,
                storage_provider=stored_document.storage_provider,
                storage_key=stored_document.storage_key,
                checksum_sha256=stored_document.checksum_sha256,
                document_version=document_version,
                uploaded_by=user_id,
                created_by=user_id,
            )

            # --------------------------------------------------------------
            # Persist metadata
            # --------------------------------------------------------------

            with self._unit_of_work:
                self._employee_document_repository.save(
                    document,
                )
                self._unit_of_work.flush()

        except Exception:
            # --------------------------------------------------------------
            # Compensating storage cleanup
            # --------------------------------------------------------------

            if stored_document is not None:
                self._document_storage.delete(
                    storage_key=stored_document.storage_key,
                )

            raise

        return UploadEmployeeDocumentResponse(
            id=document.id,
            employee_id=document.employee_id,
            immigration_id=document.immigration_id,
            document_name=document.document_name,
            document_category=document.document_category,
            original_filename=document.original_filename,
            stored_filename=document.stored_filename,
            mime_type=document.mime_type,
            file_extension=document.file_extension,
            file_size_bytes=document.file_size_bytes,
            storage_provider=document.storage_provider,
            storage_key=document.storage_key,
            checksum_sha256=document.checksum_sha256,
            document_version=document.document_version,
        )
