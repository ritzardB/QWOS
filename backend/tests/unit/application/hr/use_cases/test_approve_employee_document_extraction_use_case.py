"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

HR Module

File:
    test_approve_employee_document_extraction_use_case.py

Description:
    Unit tests for ApproveEmployeeDocumentExtractionUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date
from unittest.mock import AsyncMock, MagicMock

import pytest

from qwos.application.common.exceptions.forbidden_exception import (
    ForbiddenException,
)
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.hr.commands.approve_employee_document_extraction_command import (
    ApprovedEmployeeDocumentField,
    ApproveEmployeeDocumentExtractionCommand,
)
from qwos.application.hr.use_cases.approve_employee_document_extraction_use_case import (
    ApproveEmployeeDocumentExtractionUseCase,
)


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
EMPLOYEE_ID = "01M03ZJQ8XMGC7424THFKH4HVD"
DOCUMENT_ID = "01M03DOCUMENT00000000000001"
PROFILE_ID = "01M03PROFILE000000000000001"
IMMIGRATION_ID = "01M03IMMIGRATION00000000001"
RESULT_ID = "01M03RESULT000000000000001"
FIELD_ID = "01M03FIELD000000000000000001"
USER_ID = "01M03USER000000000000000001"


def make_context() -> MagicMock:
    context = MagicMock()
    context.tenant_id = TENANT_ID
    context.user_id = USER_ID
    return context


def make_document(
    *,
    immigration_id: str | None = None,
) -> MagicMock:
    document = MagicMock()
    document.id = DOCUMENT_ID
    document.tenant_id = TENANT_ID
    document.employee_id = EMPLOYEE_ID
    document.deleted_at = None
    document.immigration_id = immigration_id
    return document


def make_extraction_result(
    *,
    result_id: str = RESULT_ID,
    field_id: str = FIELD_ID,
) -> MagicMock:
    result = MagicMock()
    result.id = result_id
    result.employee_document_id = DOCUMENT_ID
    result.document_definition_field_id = field_id
    return result


def make_field(
    *,
    field_code: str = "document_number",
    field_label: str = "Document Number",
    target_entity: str | None = "employee_profile",
    target_field: str | None = "date_of_birth",
    data_type: str = "date",
    is_hr_updateable: bool = True,
    validation_pattern: str | None = None,
) -> MagicMock:
    field = MagicMock()

    field.id = FIELD_ID
    field.field_code = field_code
    field.field_label = field_label
    field.data_type = data_type
    field.is_required = False
    field.is_extractable = True
    field.sort_order = 0
    field.is_hr_updateable = is_hr_updateable
    field.target_entity = target_entity
    field.target_field = target_field
    field.validation_pattern = validation_pattern
    field.is_active = True

    return field

def make_profile() -> MagicMock:
    profile = MagicMock()
    profile.id = PROFILE_ID
    profile.employee_id = EMPLOYEE_ID
    profile.date_of_birth = None
    profile.gender = None
    profile.nationality = None
    profile.marital_status = None
    profile.personal_email = None
    profile.personal_phone = None
    profile.address_line_1 = None
    profile.address_line_2 = None
    profile.city = None
    profile.state_province = None
    profile.postal_code = None
    profile.country_code = None
    profile.emergency_contact_name = None
    profile.emergency_contact_relationship = None
    profile.emergency_contact_phone = None
    return profile


def make_immigration() -> MagicMock:
    immigration = MagicMock()
    immigration.id = IMMIGRATION_ID
    immigration.employee_id = EMPLOYEE_ID
    immigration.tenant_id = TENANT_ID
    immigration.document_number = None
    immigration.issuing_authority = None
    immigration.issue_date = None
    immigration.expiry_date = None
    immigration.immigration_type = "residence visa"
    immigration.status = "active"
    immigration.sponsor_name = None
    immigration.notes = None
    return immigration


def make_unit_of_work() -> MagicMock:
    unit_of_work = MagicMock()
    unit_of_work.__enter__.return_value = unit_of_work
    unit_of_work.__exit__.return_value = None
    return unit_of_work


def make_use_case() -> tuple[
    ApproveEmployeeDocumentExtractionUseCase,
    dict[str, MagicMock],
]:
    employee_document_repository = MagicMock()
    document_definition_field_repository = MagicMock()
    document_extraction_result_repository = MagicMock()
    employee_profile_repository = MagicMock()
    employee_immigration_repository = MagicMock()

    authorization_service = MagicMock()
    authorization_service.has_permission = AsyncMock(
        return_value=True,
    )

    unit_of_work = make_unit_of_work()

    context = make_context()

    use_case = ApproveEmployeeDocumentExtractionUseCase(
        employee_document_repository=employee_document_repository,
        document_definition_field_repository=(
            document_definition_field_repository
        ),
        document_extraction_result_repository=(
            document_extraction_result_repository
        ),
        employee_profile_repository=employee_profile_repository,
        employee_immigration_repository=(
            employee_immigration_repository
        ),
        authorization_service=authorization_service,
        unit_of_work=unit_of_work,
        request_context=context,
    )

    return use_case, {
        "employee_document_repository": employee_document_repository,
        "document_definition_field_repository": (
            document_definition_field_repository
        ),
        "document_extraction_result_repository": (
            document_extraction_result_repository
        ),
        "employee_profile_repository": employee_profile_repository,
        "employee_immigration_repository": (
            employee_immigration_repository
        ),
        "authorization_service": authorization_service,
        "unit_of_work": unit_of_work,
    }


@pytest.mark.anyio
async def test_rejects_when_permission_is_missing() -> None:
    use_case, dependencies = make_use_case()

    dependencies[
        "authorization_service"
    ].has_permission.return_value = False

    command = ApproveEmployeeDocumentExtractionCommand(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        document_id=DOCUMENT_ID,
        fields=(),
    )

    with pytest.raises(
        ForbiddenException,
        match="not authorized",
    ):
        await use_case.execute(command)


@pytest.mark.anyio
async def test_rejects_missing_document() -> None:
    use_case, dependencies = make_use_case()

    dependencies[
        "employee_document_repository"
    ].get_by_id.return_value = None

    command = ApproveEmployeeDocumentExtractionCommand(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        document_id=DOCUMENT_ID,
        fields=(),
    )

    with pytest.raises(
        ResourceNotFoundException,
    ):
        await use_case.execute(command)


@pytest.mark.anyio
async def test_rejects_document_from_another_tenant() -> None:
    use_case, dependencies = make_use_case()

    document = make_document()
    document.tenant_id = "01OTHER00000000000000000001"

    dependencies[
        "employee_document_repository"
    ].get_by_id.return_value = document

    command = ApproveEmployeeDocumentExtractionCommand(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        document_id=DOCUMENT_ID,
        fields=(),
    )

    with pytest.raises(
        ResourceNotFoundException,
    ):
        await use_case.execute(command)


@pytest.mark.anyio
async def test_rejects_document_for_another_employee() -> None:
    use_case, dependencies = make_use_case()

    document = make_document()
    document.employee_id = "01OTHEREMPLOYEE00000000001"

    dependencies[
        "employee_document_repository"
    ].get_by_id.return_value = document

    command = ApproveEmployeeDocumentExtractionCommand(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        document_id=DOCUMENT_ID,
        fields=(),
    )

    with pytest.raises(
        ResourceNotFoundException,
    ):
        await use_case.execute(command)


@pytest.mark.anyio
async def test_rejects_missing_extraction_result() -> None:
    use_case, dependencies = make_use_case()

    dependencies[
        "employee_document_repository"
    ].get_by_id.return_value = make_document()

    dependencies[
        "document_extraction_result_repository"
    ].list_by_document_id.return_value = []

    command = ApproveEmployeeDocumentExtractionCommand(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        document_id=DOCUMENT_ID,
        fields=(
            ApprovedEmployeeDocumentField(
                extraction_result_id=RESULT_ID,
                value="1971-04-06",
            ),
        ),
    )

    with pytest.raises(
        ResourceNotFoundException,
    ):
        await use_case.execute(command)


@pytest.mark.anyio
async def test_rejects_non_updateable_field() -> None:
    use_case, dependencies = make_use_case()

    dependencies[
        "employee_document_repository"
    ].get_by_id.return_value = make_document()

    dependencies[
        "document_extraction_result_repository"
    ].list_by_document_id.return_value = [
        make_extraction_result(),
    ]

    dependencies[
        "document_definition_field_repository"
    ].get_by_id.return_value = make_field(
        is_hr_updateable=False,
    )

    command = ApproveEmployeeDocumentExtractionCommand(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        document_id=DOCUMENT_ID,
        fields=(
            ApprovedEmployeeDocumentField(
                extraction_result_id=RESULT_ID,
                value="1971-04-06",
            ),
        ),
    )

    with pytest.raises(
        ValueError,
        match="not configured for HR updates",
    ):
        await use_case.execute(command)


@pytest.mark.anyio
async def test_updates_employee_profile_date_of_birth() -> None:
    use_case, dependencies = make_use_case()

    profile = make_profile()

    dependencies[
        "employee_document_repository"
    ].get_by_id.return_value = make_document()

    dependencies[
        "document_extraction_result_repository"
    ].list_by_document_id.return_value = [
        make_extraction_result(),
    ]

    dependencies[
        "document_definition_field_repository"
    ].get_by_id.return_value = make_field(
        field_code="date_of_birth",
        target_entity="employee_profile",
        target_field="date_of_birth",
        data_type="date",
    )

    dependencies[
        "employee_profile_repository"
    ].get_by_employee_id.return_value = profile

    command = ApproveEmployeeDocumentExtractionCommand(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        document_id=DOCUMENT_ID,
        fields=(
            ApprovedEmployeeDocumentField(
                extraction_result_id=RESULT_ID,
                value="1971-04-06",
            ),
        ),
    )

    response = await use_case.execute(command)

    profile.update.assert_called_once()

    update_kwargs = profile.update.call_args.kwargs

    assert update_kwargs["date_of_birth"] == date(
        1971,
        4,
        6,
    )
    assert update_kwargs["updated_by"] == USER_ID

    dependencies[
        "employee_profile_repository"
    ].save.assert_called_once_with(profile)

    assert response.document_id == DOCUMENT_ID
    assert response.employee_id == EMPLOYEE_ID
    assert len(response.approved_fields) == 1
    assert (
        response.approved_fields[0].field_code
        == "date_of_birth"
    )


@pytest.mark.anyio
async def test_updates_employee_profile_nationality() -> None:
    use_case, dependencies = make_use_case()

    profile = make_profile()

    dependencies[
        "employee_document_repository"
    ].get_by_id.return_value = make_document()

    dependencies[
        "document_extraction_result_repository"
    ].list_by_document_id.return_value = [
        make_extraction_result(),
    ]

    dependencies[
        "document_definition_field_repository"
    ].get_by_id.return_value = make_field(
        field_code="nationality",
        target_entity="employee_profile",
        target_field="nationality",
        data_type="string",
    )

    dependencies[
        "employee_profile_repository"
    ].get_by_employee_id.return_value = profile

    command = ApproveEmployeeDocumentExtractionCommand(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        document_id=DOCUMENT_ID,
        fields=(
            ApprovedEmployeeDocumentField(
                extraction_result_id=RESULT_ID,
                value="PHL",
            ),
        ),
    )

    response = await use_case.execute(command)

    update_kwargs = profile.update.call_args.kwargs

    assert update_kwargs["nationality"] == "PHL"
    assert response.approved_fields[0].target_entity == (
        "employee_profile"
    )


@pytest.mark.anyio
async def test_updates_employee_immigration() -> None:
    use_case, dependencies = make_use_case()

    document = make_document(
        immigration_id=IMMIGRATION_ID,
    )
    immigration = make_immigration()

    dependencies[
        "employee_document_repository"
    ].get_by_id.return_value = document

    dependencies[
        "document_extraction_result_repository"
    ].list_by_document_id.return_value = [
        make_extraction_result(),
    ]

    dependencies[
        "document_definition_field_repository"
    ].get_by_id.return_value = make_field(
        field_code="expiry_date",
        target_entity="employee_immigration",
        target_field="expiry_date",
        data_type="date",
    )

    dependencies[
        "employee_immigration_repository"
    ].get_by_id.return_value = immigration

    command = ApproveEmployeeDocumentExtractionCommand(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        document_id=DOCUMENT_ID,
        fields=(
            ApprovedEmployeeDocumentField(
                extraction_result_id=RESULT_ID,
                value="2028-04-24",
            ),
        ),
    )

    response = await use_case.execute(command)

    immigration.update.assert_called_once()

    update_kwargs = immigration.update.call_args.kwargs

    assert update_kwargs["expiry_date"] == date(
        2028,
        4,
        24,
    )
    assert update_kwargs["updated_by"] == USER_ID

    dependencies[
        "employee_immigration_repository"
    ].save.assert_called_once_with(
        immigration,
    )

    assert response.approved_fields[0].target_entity == (
        "employee_immigration"
    )


@pytest.mark.anyio
async def test_rejects_immigration_update_without_linked_record() -> None:
    use_case, dependencies = make_use_case()

    dependencies[
        "employee_document_repository"
    ].get_by_id.return_value = make_document(
        immigration_id=None,
    )

    dependencies[
        "document_extraction_result_repository"
    ].list_by_document_id.return_value = [
        make_extraction_result(),
    ]

    dependencies[
        "document_definition_field_repository"
    ].get_by_id.return_value = make_field(
        field_code="expiry_date",
        target_entity="employee_immigration",
        target_field="expiry_date",
        data_type="date",
    )

    command = ApproveEmployeeDocumentExtractionCommand(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        document_id=DOCUMENT_ID,
        fields=(
            ApprovedEmployeeDocumentField(
                extraction_result_id=RESULT_ID,
                value="2028-04-24",
            ),
        ),
    )

    with pytest.raises(
        ValueError,
        match="not linked to an immigration record",
    ):
        await use_case.execute(command)


@pytest.mark.anyio
async def test_rejects_invalid_date_value() -> None:
    use_case, dependencies = make_use_case()

    dependencies[
        "employee_document_repository"
    ].get_by_id.return_value = make_document()

    dependencies[
        "document_extraction_result_repository"
    ].list_by_document_id.return_value = [
        make_extraction_result(),
    ]

    dependencies[
        "document_definition_field_repository"
    ].get_by_id.return_value = make_field(
        field_code="date_of_birth",
        target_entity="employee_profile",
        target_field="date_of_birth",
        data_type="date",
    )

    with pytest.raises(
        ValueError,
    ):
        await use_case.execute(
            ApproveEmployeeDocumentExtractionCommand(
                tenant_id=TENANT_ID,
                employee_id=EMPLOYEE_ID,
                document_id=DOCUMENT_ID,
                fields=(
                    ApprovedEmployeeDocumentField(
                        extraction_result_id=RESULT_ID,
                        value="not-a-date",
                    ),
                ),
            ),
        )


@pytest.mark.anyio
async def test_rejects_unsupported_target_entity() -> None:
    use_case, dependencies = make_use_case()

    dependencies[
        "employee_document_repository"
    ].get_by_id.return_value = make_document()

    dependencies[
        "document_extraction_result_repository"
    ].list_by_document_id.return_value = [
        make_extraction_result(),
    ]

    dependencies[
        "document_definition_field_repository"
    ].get_by_id.return_value = make_field(
        field_code="test_field",
        target_entity="unknown_entity",
        target_field="unknown_field",
        data_type="string",
    )

    with pytest.raises(
        ValueError,
        match="Unsupported HR target entity",
    ):
        await use_case.execute(
            ApproveEmployeeDocumentExtractionCommand(
                tenant_id=TENANT_ID,
                employee_id=EMPLOYEE_ID,
                document_id=DOCUMENT_ID,
                fields=(
                    ApprovedEmployeeDocumentField(
                        extraction_result_id=RESULT_ID,
                        value="test",
                    ),
                ),
            ),
        )