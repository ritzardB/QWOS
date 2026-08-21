"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

HR Module

File:
    test_extract_employee_document_use_case.py

Description:
    Unit tests for ExtractEmployeeDocumentUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from qwos.application.common.context.request_context import (
    RequestContext,
)
from qwos.application.common.exceptions.forbidden_exception import (
    ForbiddenException,
)
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.common.ports.document_intelligence import (
    DocumentClassification,
    DocumentExtraction,
    ExtractedDocumentField,
)
from qwos.application.hr.commands.extract_employee_document_command import (
    ExtractEmployeeDocumentCommand,
)
from qwos.application.hr.use_cases.extract_employee_document_use_case import (
    ExtractEmployeeDocumentUseCase,
)

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
USER_ID = "01KZYTCWRF8S12V28R9NX6JXS5"
EMPLOYEE_ID = "01M03ZJQ8XMGC7424THFKH4HVD"
DOCUMENT_ID = "01M0DOCUMENT000000000000001"
DEFINITION_ID = "01M0DEFINITION000000000001"
FIELD_ID = "01M0FIELD000000000000000001"
RESULT_ID = "01M0RESULT000000000000000001"


def make_request_context() -> RequestContext:
    return RequestContext(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        correlation_id="test-correlation-id",
        request_id="test-request-id",
        locale="en-US",
        timezone="UTC",
        ip_address=None,
        user_agent=None,
    )


def make_command() -> ExtractEmployeeDocumentCommand:
    return ExtractEmployeeDocumentCommand(
        employee_id=EMPLOYEE_ID,
        document_id=DOCUMENT_ID,
        request_context=make_request_context(),
    )


def make_document() -> MagicMock:
    document = MagicMock()

    document.id = DOCUMENT_ID
    document.tenant_id = TENANT_ID
    document.employee_id = EMPLOYEE_ID
    document.deleted_at = None
    document.document_category = "passport"
    document.original_filename = "passport.pdf"
    document.mime_type = "application/pdf"
    document.storage_key = (
        "employees/QW-00001/documents/passport/"
        "QW-00001_PASSPORT_V01.pdf"
    )

    return document


def make_definition() -> MagicMock:
    definition = MagicMock()

    definition.id = DEFINITION_ID
    definition.document_family = "passport"

    return definition


def make_field(
    *,
    field_id: str = FIELD_ID,
    field_code: str = "document_number",
    is_extractable: bool = True,
) -> MagicMock:
    field = MagicMock()

    field.id = field_id
    field.field_code = field_code
    field.is_extractable = is_extractable

    return field


def make_use_case() -> tuple[
    ExtractEmployeeDocumentUseCase,
    dict[str, MagicMock | AsyncMock],
]:
    employee_document_repository = MagicMock()
    document_definition_repository = MagicMock()
    document_definition_field_repository = MagicMock()
    document_extraction_result_repository = MagicMock()
    authorization_service = MagicMock()
    document_storage = MagicMock()
    document_intelligence = MagicMock()
    id_generator = MagicMock()
    unit_of_work = MagicMock()

    authorization_service.has_permission = AsyncMock(
        return_value=True,
    )

    id_generator.generate.return_value = RESULT_ID

    document_definition = make_definition()

    document_definition_repository.get_by_family.return_value = (
        document_definition
    )

    document_definition_field_repository.list_by_definition_id.return_value = [
        make_field(),
    ]

    document_storage.read.return_value = MagicMock(
        content=b"passport content",
        filename="passport.pdf",
        mime_type="application/pdf",
    )

    document_intelligence.classify.return_value = (
        DocumentClassification(
            document_family="passport",
            country_code="UTO",
            confidence=1.0,
        )
    )

    document_intelligence.extract.return_value = (
        DocumentExtraction(
            classification=DocumentClassification(
                document_family="passport",
                country_code="UTO",
                confidence=1.0,
            ),
            fields=(
                ExtractedDocumentField(
                    field_code="document_number",
                    raw_value="L898902C",
                    normalized_value="L898902C",
                    confidence=1.0,
                    source="mrz",
                ),
            ),
        )
    )

    use_case = ExtractEmployeeDocumentUseCase(
        employee_document_repository=(
            employee_document_repository
        ),
        document_definition_repository=(
            document_definition_repository
        ),
        document_definition_field_repository=(
            document_definition_field_repository
        ),
        document_extraction_result_repository=(
            document_extraction_result_repository
        ),
        authorization_service=authorization_service,
        document_storage=document_storage,
        document_intelligence=document_intelligence,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
    )

    return use_case, {
        "employee_document_repository": (
            employee_document_repository
        ),
        "document_definition_repository": (
            document_definition_repository
        ),
        "document_definition_field_repository": (
            document_definition_field_repository
        ),
        "document_extraction_result_repository": (
            document_extraction_result_repository
        ),
        "authorization_service": authorization_service,
        "document_storage": document_storage,
        "document_intelligence": document_intelligence,
        "id_generator": id_generator,
        "unit_of_work": unit_of_work,
        "document_definition": document_definition,
    }


def test_execute_rejects_unauthorized_user() -> None:
    use_case, dependencies = make_use_case()

    authorization_service = dependencies[
        "authorization_service"
    ]

    assert isinstance(
        authorization_service,
        MagicMock,
    )

    authorization_service.has_permission = AsyncMock(
        return_value=False,
    )

    with pytest.raises(
        ForbiddenException,
        match="not authorized",
    ):
        import asyncio

        asyncio.run(
            use_case.execute(
                make_command(),
            ),
        )


def test_execute_rejects_missing_document() -> None:
    use_case, dependencies = make_use_case()

    repository = dependencies[
        "employee_document_repository"
    ]

    repository.get_by_id.return_value = None

    with pytest.raises(
        ResourceNotFoundException,
    ):
        import asyncio

        asyncio.run(
            use_case.execute(
                make_command(),
            ),
        )


def test_execute_rejects_document_from_other_tenant() -> None:
    use_case, dependencies = make_use_case()

    repository = dependencies[
        "employee_document_repository"
    ]

    document = make_document()
    document.tenant_id = "01OTHER00000000000000000001"

    repository.get_by_id.return_value = document

    with pytest.raises(
        ResourceNotFoundException,
    ):
        import asyncio

        asyncio.run(
            use_case.execute(
                make_command(),
            ),
        )


def test_execute_rejects_document_for_other_employee() -> None:
    use_case, dependencies = make_use_case()

    repository = dependencies[
        "employee_document_repository"
    ]

    document = make_document()
    document.employee_id = "01OTHEREMPLOYEE00000000000001"

    repository.get_by_id.return_value = document

    with pytest.raises(
        ResourceNotFoundException,
    ):
        import asyncio

        asyncio.run(
            use_case.execute(
                make_command(),
            ),
        )


def test_execute_rejects_deleted_document() -> None:
    use_case, dependencies = make_use_case()

    repository = dependencies[
        "employee_document_repository"
    ]

    document = make_document()
    document.deleted_at = MagicMock()

    repository.get_by_id.return_value = document

    with pytest.raises(
        ResourceNotFoundException,
    ):
        import asyncio

        asyncio.run(
            use_case.execute(
                make_command(),
            ),
        )


def test_execute_rejects_missing_document_definition() -> None:
    use_case, dependencies = make_use_case()

    employee_document_repository = dependencies[
        "employee_document_repository"
    ]
    definition_repository = dependencies[
        "document_definition_repository"
    ]

    employee_document_repository.get_by_id.return_value = (
        make_document()
    )

    definition_repository.get_by_family.return_value = None

    with pytest.raises(
        ResourceNotFoundException,
    ):
        import asyncio

        asyncio.run(
            use_case.execute(
                make_command(),
            ),
        )


def test_execute_rejects_missing_definition_fields() -> None:
    use_case, dependencies = make_use_case()

    employee_document_repository = dependencies[
        "employee_document_repository"
    ]
    field_repository = dependencies[
        "document_definition_field_repository"
    ]

    employee_document_repository.get_by_id.return_value = (
        make_document()
    )

    field_repository.list_by_definition_id.return_value = []

    with pytest.raises(
        ResourceNotFoundException,
    ):
        import asyncio

        asyncio.run(
            use_case.execute(
                make_command(),
            ),
        )


def test_execute_extracts_and_persists_result() -> None:
    use_case, dependencies = make_use_case()

    employee_document_repository = dependencies[
        "employee_document_repository"
    ]
    definition_repository = dependencies[
        "document_definition_repository"
    ]
    field_repository = dependencies[
        "document_definition_field_repository"
    ]
    extraction_repository = dependencies[
        "document_extraction_result_repository"
    ]
    document_storage = dependencies[
        "document_storage"
    ]
    document_intelligence = dependencies[
        "document_intelligence"
    ]
    id_generator = dependencies[
        "id_generator"
    ]

    employee_document_repository.get_by_id.return_value = (
        make_document()
    )

    definition = make_definition()

    definition_repository.get_by_family.side_effect = [
        definition,
        definition,
    ]

    field_repository.list_by_definition_id.return_value = [
        make_field(),
    ]

    result = __import__(
        "asyncio",
    ).run(
        use_case.execute(
            make_command(),
        ),
    )

    assert result.document_id == DOCUMENT_ID
    assert result.employee_id == EMPLOYEE_ID
    assert result.document_family == "passport"
    assert result.country_code == "UTO"
    assert len(result.fields) == 1

    field = result.fields[0]

    assert field.extraction_result_id == RESULT_ID
    assert field.field_code == "document_number"
    assert field.raw_value == "L898902C"
    assert field.normalized_value == "L898902C"
    assert field.confidence == 1.0
    assert field.source == "mrz"

    document_storage.read.assert_called_once_with(
        storage_key=(
            "employees/QW-00001/documents/passport/"
            "QW-00001_PASSPORT_V01.pdf"
        ),
    )

    document_intelligence.classify.assert_called_once_with(
        content=b"passport content",
        filename="passport.pdf",
        mime_type="application/pdf",
    )

    document_intelligence.extract.assert_called_once_with(
        content=b"passport content",
        filename="passport.pdf",
        mime_type="application/pdf",
        document_family="passport",
        country_code="UTO",
    )

    id_generator.generate.assert_called_once()

    extraction_repository.save.assert_called_once()

    saved_result = (
        extraction_repository.save.call_args.args[0]
    )

    assert saved_result.tenant_id == TENANT_ID
    assert (
        saved_result.employee_document_id
        == DOCUMENT_ID
    )
    assert (
        saved_result.document_definition_field_id
        == FIELD_ID
    )
    assert saved_result.raw_value == "L898902C"
    assert saved_result.normalized_value == "L898902C"
    assert saved_result.confidence == 1.0
    assert saved_result.source == "mrz"


def test_execute_ignores_unconfigured_extracted_fields() -> None:
    use_case, dependencies = make_use_case()

    employee_document_repository = dependencies[
        "employee_document_repository"
    ]
    field_repository = dependencies[
        "document_definition_field_repository"
    ]
    extraction_repository = dependencies[
        "document_extraction_result_repository"
    ]

    employee_document_repository.get_by_id.return_value = (
        make_document()
    )

    field_repository.list_by_definition_id.return_value = [
        make_field(
            field_code="document_number",
        ),
    ]

    document_intelligence = dependencies[
        "document_intelligence"
    ]

    document_intelligence.extract.return_value = (
        DocumentExtraction(
            classification=DocumentClassification(
                document_family="passport",
                country_code="UTO",
                confidence=1.0,
            ),
            fields=(
                ExtractedDocumentField(
                    field_code="document_number",
                    raw_value="L898902C",
                    normalized_value="L898902C",
                    confidence=1.0,
                    source="mrz",
                ),
                ExtractedDocumentField(
                    field_code="unknown_field",
                    raw_value="IGNORED",
                    normalized_value="IGNORED",
                    confidence=0.50,
                    source="ocr",
                ),
            ),
        )
    )

    result = __import__(
        "asyncio",
    ).run(
        use_case.execute(
            make_command(),
        ),
    )

    assert len(result.fields) == 1
    assert result.fields[0].field_code == (
        "document_number"
    )

    extraction_repository.save.assert_called_once()


def test_execute_ignores_non_extractable_fields() -> None:
    use_case, dependencies = make_use_case()

    employee_document_repository = dependencies[
        "employee_document_repository"
    ]
    field_repository = dependencies[
        "document_definition_field_repository"
    ]
    extraction_repository = dependencies[
        "document_extraction_result_repository"
    ]

    employee_document_repository.get_by_id.return_value = (
        make_document()
    )

    field_repository.list_by_definition_id.return_value = [
        make_field(
            field_code="document_number",
            is_extractable=False,
        ),
    ]

    result = __import__(
        "asyncio",
    ).run(
        use_case.execute(
            make_command(),
        ),
    )

    assert result.fields == ()
    extraction_repository.save.assert_not_called()