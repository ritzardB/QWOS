"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    approve_employee_document_extraction_use_case.py

Description:
    Applies human-approved document extraction values to supported HR records.

Responsibilities:
    - Authorize the approval operation
    - Validate employee/document ownership
    - Validate extraction-result ownership
    - Validate configured HR mappings
    - Update supported HR entities
    - Persist approved changes atomically

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date

from qwos.application.common.exceptions.forbidden_exception import (
    ForbiddenException,
)
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.hr.commands.approve_employee_document_extraction_command import (
    ApproveEmployeeDocumentExtractionCommand,
)
from qwos.application.hr.responses.approve_employee_document_extraction_response import (
    ApprovedEmployeeDocumentField,
    ApproveEmployeeDocumentExtractionResponse,
)
from qwos.domains.hr.repositories.document_definition_field_repository import (
    DocumentDefinitionFieldRepository,
)
from qwos.domains.hr.repositories.document_extraction_result_repository import (
    DocumentExtractionResultRepository,
)
from qwos.domains.hr.repositories.employee_document_repository import (
    EmployeeDocumentRepository,
)
from qwos.domains.hr.repositories.employee_immigration_repository import (
    EmployeeImmigrationRepository,
)
from qwos.domains.hr.repositories.employee_profile_repository import (
    EmployeeProfileRepository,
)
from qwos.domains.identity.services.authorization_service import (
    AuthorizationService,
)


class ApproveEmployeeDocumentExtractionUseCase:
    """
    Apply human-approved extraction candidates to supported HR records.
    """

    REQUIRED_PERMISSION = "HR_DOCUMENT_UPDATE"

    SUPPORTED_PROFILE_FIELDS = frozenset(
        {
            "date_of_birth",
            "nationality",
            "gender",
        },
    )

    SUPPORTED_IMMIGRATION_FIELDS = frozenset(
        {
            "document_number",
            "issuing_authority",
            "issue_date",
            "expiry_date",
        },
    )

    def __init__(
        self,
        *,
        employee_document_repository: EmployeeDocumentRepository,
        document_definition_field_repository: (
            DocumentDefinitionFieldRepository
        ),
        document_extraction_result_repository: (
            DocumentExtractionResultRepository
        ),
        employee_profile_repository: EmployeeProfileRepository,
        employee_immigration_repository: EmployeeImmigrationRepository,
        authorization_service: AuthorizationService,
        unit_of_work: UnitOfWork,
        request_context,
    ) -> None:
        self._employee_document_repository = (
            employee_document_repository
        )
        self._document_definition_field_repository = (
            document_definition_field_repository
        )
        self._document_extraction_result_repository = (
            document_extraction_result_repository
        )
        self._employee_profile_repository = (
            employee_profile_repository
        )
        self._employee_immigration_repository = (
            employee_immigration_repository
        )
        self._authorization_service = (
            authorization_service
        )
        self._unit_of_work = unit_of_work
        self._request_context = request_context

    async def execute(
        self,
        command: ApproveEmployeeDocumentExtractionCommand,
    ) -> ApproveEmployeeDocumentExtractionResponse:
        """
        Approve extraction candidates and update supported HR records.
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
                message=(
                    "User is not authorized to approve "
                    "employee document extraction."
                ),
            )

        # ------------------------------------------------------------------
        # Load document
        # ------------------------------------------------------------------

        document = (
            self._employee_document_repository.get_by_id(
                command.document_id,
            )
        )

        if document is None:
            raise ResourceNotFoundException(
                resource="EmployeeDocument",
                identifier=command.document_id,
            )

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
        # Preload document extraction evidence
        # ------------------------------------------------------------------

        extraction_results = (
            self._document_extraction_result_repository.list_by_document_id(
                tenant_id=tenant_id,
                employee_document_id=document.id,
            )
        )

        extraction_by_id = {
            result.id: result
            for result in extraction_results
        }

        # ------------------------------------------------------------------
        # Load profile / immigration targets lazily
        # ------------------------------------------------------------------

        profile = None
        immigration = None

        approved_fields: list[
            ApprovedEmployeeDocumentField
        ] = []

        profile_updates: dict[str, object | None] = {}
        immigration_updates: dict[
            str,
            object | None,
        ] = {}

        # ------------------------------------------------------------------
        # Validate each approved field
        # ------------------------------------------------------------------

        for approved in command.fields:
            result = extraction_by_id.get(
                approved.extraction_result_id,
            )

            if result is None:
                raise ResourceNotFoundException(
                    resource="DocumentExtractionResult",
                    identifier=approved.extraction_result_id,
                )

            if result.employee_document_id != document.id:
                raise ResourceNotFoundException(
                    resource="DocumentExtractionResult",
                    identifier=approved.extraction_result_id,
                )

            field = (
                self._document_definition_field_repository.get_by_id(
                    result.document_definition_field_id,
                )
            )

            if field is None:
                raise ResourceNotFoundException(
                    resource="DocumentDefinitionField",
                    identifier=result.document_definition_field_id,
                )

            if not field.is_active:
                raise ValueError(
                    f"Document field '{field.field_code}' is inactive.",
                )

            if not field.is_hr_updateable:
                raise ValueError(
                    f"Document field '{field.field_code}' "
                    "is not configured for HR updates.",
                )

            if (
                not field.target_entity
                or not field.target_field
            ):
                raise ValueError(
                    f"Document field '{field.field_code}' "
                    "has no valid HR target mapping.",
                )

            target_entity = field.target_entity.strip().lower()
            target_field = field.target_field.strip().lower()

            # --------------------------------------------------------------
            # Employee Profile
            # --------------------------------------------------------------

            if target_entity == "employee_profile":
                if target_field not in self.SUPPORTED_PROFILE_FIELDS:
                    raise ValueError(
                        f"Unsupported employee profile target "
                        f"'{target_field}'.",
                    )

                if profile is None:
                    profile = (
                        self._employee_profile_repository
                        .get_by_employee_id(
                            tenant_id=tenant_id,
                            employee_id=command.employee_id,
                        )
                    )

                    if profile is None:
                        raise ResourceNotFoundException(
                            resource="EmployeeProfile",
                            identifier=command.employee_id,
                        )

                profile_updates[
                    target_field
                ] = self._normalize_profile_value(
                    target_field=target_field,
                    value=approved.value,
                )

            # --------------------------------------------------------------
            # Employee Immigration
            # --------------------------------------------------------------

            elif target_entity == "employee_immigration":
                if target_field not in self.SUPPORTED_IMMIGRATION_FIELDS:
                    raise ValueError(
                        f"Unsupported employee immigration target "
                        f"'{target_field}'.",
                    )

                if document.immigration_id is None:
                    raise ValueError(
                        "Document is not linked to an immigration record.",
                    )

                if immigration is None:
                    immigration = (
                        self._employee_immigration_repository
                        .get_by_id(
                            document.immigration_id,
                        )
                    )

                    if immigration is None:
                        raise ResourceNotFoundException(
                            resource="EmployeeImmigration",
                            identifier=document.immigration_id,
                        )

                    if immigration.tenant_id != tenant_id:
                        raise ResourceNotFoundException(
                            resource="EmployeeImmigration",
                            identifier=document.immigration_id,
                        )

                    if immigration.employee_id != command.employee_id:
                        raise ResourceNotFoundException(
                            resource="EmployeeImmigration",
                            identifier=document.immigration_id,
                        )

                immigration_updates[
                    target_field
                ] = self._normalize_immigration_value(
                    target_field=target_field,
                    value=approved.value,
                )

            else:
                raise ValueError(
                    f"Unsupported HR target entity "
                    f"'{target_entity}'.",
                )

            approved_fields.append(
                ApprovedEmployeeDocumentField(
                    extraction_result_id=result.id,
                    field_code=field.field_code,
                    target_entity=target_entity,
                    target_field=target_field,
                    value=approved.value,
                ),
            )

        # ------------------------------------------------------------------
        # Apply profile updates
        # ------------------------------------------------------------------

        with self._unit_of_work:
            if profile is not None and profile_updates:
                profile.update(
                    **profile_updates,
                    updated_by=user_id,
                )

                self._employee_profile_repository.save(
                    profile,
                )

            if immigration is not None and immigration_updates:
                immigration.update(
                    document_number=(
                        immigration_updates.get(
                            "document_number",
                        )
                        if "document_number"
                        in immigration_updates
                        else immigration.document_number
                    ),
                    issuing_authority=(
                        immigration_updates.get(
                            "issuing_authority",
                        )
                        if "issuing_authority"
                        in immigration_updates
                        else immigration.issuing_authority
                    ),
                    issue_date=(
                        immigration_updates.get(
                            "issue_date",
                        )
                        if "issue_date"
                        in immigration_updates
                        else immigration.issue_date
                    ),
                    expiry_date=(
                        immigration_updates.get(
                            "expiry_date",
                        )
                        if "expiry_date"
                        in immigration_updates
                        else immigration.expiry_date
                    ),
                    updated_by=user_id,
                )

                self._employee_immigration_repository.save(
                    immigration,
                )

            self._unit_of_work.flush()

        return ApproveEmployeeDocumentExtractionResponse(
            document_id=document.id,
            employee_id=document.employee_id,
            approved_fields=tuple(
                approved_fields,
            ),
        )

    @staticmethod
    def _normalize_profile_value(
        *,
        target_field: str,
        value: str | None,
    ) -> object | None:
        """
        Convert approved profile values to domain-compatible values.
        """

        if value is None:
            return None

        normalized = value.strip()

        if target_field == "date_of_birth":
            return date.fromisoformat(normalized)

        if target_field in {
            "nationality",
            "gender",
        }:
            return normalized

        return normalized

    @staticmethod
    def _normalize_immigration_value(
        *,
        target_field: str,
        value: str | None,
    ) -> object | None:
        """
        Convert approved immigration values to domain-compatible values.
        """

        if value is None:
            return None

        normalized = value.strip()

        if target_field in {
            "issue_date",
            "expiry_date",
        }:
            return date.fromisoformat(normalized)

        return normalized