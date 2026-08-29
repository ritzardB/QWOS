"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    extract_employee_document_use_case.py

Description:
    Orchestrates document intelligence extraction for an employee document.

Responsibilities:
    - Authorize document extraction
    - Retrieve employee document metadata
    - Resolve the generic document definition
    - Read physical document content
    - Classify the document
    - Extract structured fields
    - Persist extraction results
    - Return extraction candidates for human review

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
from qwos.application.common.ports.document_intelligence import (
    DocumentIntelligence,
)
from qwos.application.common.ports.document_storage import (
    DocumentStorage,
)
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.application.hr.commands.extract_employee_document_command import (
    ExtractEmployeeDocumentCommand,
)
from qwos.application.hr.responses.extract_employee_document_response import (
    ExtractedEmployeeDocumentField,
    ExtractEmployeeDocumentResponse,
)
from qwos.domains.hr.models.document_extraction_result import (
    DocumentExtractionResult,
)
from qwos.domains.hr.repositories.document_definition_field_repository import (
    DocumentDefinitionFieldRepository,
)
from qwos.domains.hr.repositories.document_definition_repository import (
    DocumentDefinitionRepository,
)
from qwos.domains.hr.repositories.document_extraction_result_repository import (
    DocumentExtractionResultRepository,
)
from qwos.domains.hr.repositories.employee_document_repository import (
    EmployeeDocumentRepository,
)
from qwos.domains.identity.services.authorization_service import (
    AuthorizationService,
)
from qwos.infrastructure.document_intelligence.document_field_validator import (
    DocumentFieldValidator,
)


class ExtractEmployeeDocumentUseCase:
    """
    Extract structured data from an employee document.

    Extraction results are persisted as evidence for later human review.

    This use case does not update EmployeeProfile, EmployeeImmigration,
    or other HR records.
    """

    REQUIRED_PERMISSION = "HR_DOCUMENT_VIEW"

    def __init__(
        self,
        *,
        employee_document_repository: EmployeeDocumentRepository,
        document_definition_repository: DocumentDefinitionRepository,
        document_definition_field_repository: (DocumentDefinitionFieldRepository),
        document_extraction_result_repository: DocumentExtractionResultRepository,
        authorization_service: AuthorizationService,
        document_storage: DocumentStorage,
        document_intelligence: DocumentIntelligence,
        id_generator: IdGenerator,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._employee_document_repository = employee_document_repository
        self._document_definition_repository = document_definition_repository
        self._document_definition_field_repository = document_definition_field_repository
        self._document_extraction_result_repository = document_extraction_result_repository
        self._authorization_service = authorization_service
        self._document_storage = document_storage
        self._document_intelligence = document_intelligence
        self._id_generator = id_generator
        self._unit_of_work = unit_of_work

    async def execute(
        self,
        command: ExtractEmployeeDocumentCommand,
    ) -> ExtractEmployeeDocumentResponse:
        """
        Extract structured fields from an employee document.
        """

        request_context: RequestContext = command.request_context

        tenant_id = request_context.tenant_id
        user_id = request_context.user_id

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
                message=("User is not authorized to extract employee documents."),
            )

        # ------------------------------------------------------------------
        # Locate source document
        # ------------------------------------------------------------------

        document = self._employee_document_repository.get_by_id(
            command.document_id,
        )

        if document is None:
            raise ResourceNotFoundException(
                resource="EmployeeDocument",
                identifier=command.document_id,
            )

        # ------------------------------------------------------------------
        # Tenant isolation
        # ------------------------------------------------------------------

        if document.tenant_id != tenant_id:
            raise ResourceNotFoundException(
                resource="EmployeeDocument",
                identifier=command.document_id,
            )

        if document.employee_id != command.employee_id:
            raise ResourceNotFoundException(
                resource="EmployeeDocument",
                identifier=command.document_id,
            )

        if document.deleted_at is not None:
            raise ResourceNotFoundException(
                resource="EmployeeDocument",
                identifier=command.document_id,
            )

        # ------------------------------------------------------------------
        # Read physical document
        # ------------------------------------------------------------------

        stored_document = self._document_storage.read(
            storage_key=document.storage_key,
        )

        # ------------------------------------------------------------------
        # Initial classification
        # ------------------------------------------------------------------

        classification = self._document_intelligence.classify(
            content=stored_document.content,
            filename=document.original_filename,
            mime_type=document.mime_type,
            document_family=document.document_category,
        )

        # ------------------------------------------------------------------
        # Resolve country-specific document definition
        # ------------------------------------------------------------------

        document_definition = self._document_definition_repository.get_by_family(
            tenant_id=tenant_id,
            country_code=classification.country_code,
            document_family=classification.document_family,
        )

        if document_definition is None:
            raise ResourceNotFoundException(
                resource="DocumentDefinition",
                identifier=(f"{classification.document_family}:{classification.country_code or 'generic'}"),
            )
        # ------------------------------------------------------------------
        # Load configured extraction fields
        # ------------------------------------------------------------------

        definition_fields = self._document_definition_field_repository.list_by_definition_id(
            document_definition_id=document_definition.id,
        )

        if not definition_fields:
            raise ResourceNotFoundException(
                resource="DocumentDefinitionField",
                identifier=document_definition.id,
            )

        configured_fields = {field.field_code: field for field in definition_fields if field.is_extractable}

        # ------------------------------------------------------------------
        # Extract structured data
        # ------------------------------------------------------------------

        extraction = self._document_intelligence.extract(
            content=stored_document.content,
            filename=document.original_filename,
            mime_type=document.mime_type,
            document_family=(document_definition.document_family),
            country_code=(classification.country_code),
        )

        # ------------------------------------------------------------------
        # Match extraction candidates to configured fields
        # ------------------------------------------------------------------

        extraction_candidates = []

        for extracted_field in extraction.fields:
            configured_field = configured_fields.get(
                extracted_field.field_code,
            )

            if configured_field is None:
                continue

            # ------------------------------------------------------------------
            # Validate extracted candidate against the configured field pattern
            # ------------------------------------------------------------------

            if not DocumentFieldValidator.matches(
                value=extracted_field.raw_value,
                validation_pattern=(configured_field.validation_pattern),
            ):
                continue

            result = DocumentExtractionResult.create(
                id=self._id_generator.generate(),
                tenant_id=tenant_id,
                employee_document_id=document.id,
                document_definition_field_id=(configured_field.id),
                raw_value=(extracted_field.raw_value),
                normalized_value=(extracted_field.normalized_value),
                confidence=(extracted_field.confidence),
                source=extracted_field.source,
                created_by=user_id,
            )

            extraction_candidates.append(
                result,
            )

        # ------------------------------------------------------------------
        # Persist extraction evidence
        # ------------------------------------------------------------------

        with self._unit_of_work:
            for result in extraction_candidates:
                self._document_extraction_result_repository.save(
                    result,
                )

            self._unit_of_work.flush()

        # ------------------------------------------------------------------
        # Response
        # ------------------------------------------------------------------

        definition_fields_by_id = {field.id: field for field in definition_fields}

        return ExtractEmployeeDocumentResponse(
            document_id=document.id,
            employee_id=document.employee_id,
            document_family=document_definition.document_family,
            country_code=classification.country_code,
            fields=tuple(
                ExtractedEmployeeDocumentField(
                    extraction_result_id=result.id,
                    field_code=(definition_fields_by_id[result.document_definition_field_id].field_code),
                    raw_value=result.raw_value,
                    normalized_value=result.normalized_value,
                    confidence=result.confidence,
                    source=result.source,
                    is_hr_updateable=(definition_fields_by_id[result.document_definition_field_id].is_hr_updateable),
                    target_entity=(definition_fields_by_id[result.document_definition_field_id].target_entity),
                    target_field=(definition_fields_by_id[result.document_definition_field_id].target_field),
                )
                for result in extraction_candidates
            ),
        )
