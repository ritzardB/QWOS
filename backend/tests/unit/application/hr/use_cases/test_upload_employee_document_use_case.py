"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

HR Module

File:
    test_upload_employee_document_use_case.py

Description:
    Unit tests for UploadEmployeeDocumentUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date
from unittest.mock import AsyncMock, MagicMock

import pytest

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.forbidden_exception import (
    ForbiddenException,
)
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.common.ports.document_storage import StoredDocument
from qwos.application.hr.commands.upload_employee_document_command import (
    UploadEmployeeDocumentCommand,
)
from qwos.application.hr.use_cases.upload_employee_document_use_case import (
    UploadEmployeeDocumentUseCase,
)

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
USER_ID = "01KZYTCWRF8S12V28R9NX6JXS5"
EMPLOYEE_ID = "01M03ZJQ8XMGC7424THFKH4HVD"
IMMIGRATION_ID = "01M0IMMIGRATION00000000001"
DOCUMENT_ID = "01M0DOCUMENT000000000000001"


def make_command(
    *,
    immigration_id: str | None = IMMIGRATION_ID,
) -> UploadEmployeeDocumentCommand:
    return UploadEmployeeDocumentCommand(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        document_name="Residence Visa",
        document_category="residence visa",
        original_filename="visa_scan.pdf",
        mime_type="application/pdf",
        file_extension="pdf",
        content=b"visa document",
        immigration_id=immigration_id,
    )


def make_employee() -> MagicMock:
    employee = MagicMock()
    employee.id = EMPLOYEE_ID
    employee.tenant_id = TENANT_ID
    employee.employee_number = "QW-00002"
    return employee


def make_immigration() -> MagicMock:
    immigration = MagicMock()
    immigration.id = IMMIGRATION_ID
    immigration.tenant_id = TENANT_ID
    immigration.employee_id = EMPLOYEE_ID
    immigration.issue_date = date(2026, 8, 16)
    immigration.expiry_date = date(2027, 8, 15)
    return immigration


def make_storage_result() -> StoredDocument:
    return StoredDocument(
        storage_provider="local",
        storage_key=(
            "employees/QW-00002/documents/residence-visa/"
            "QW-00002_RESIDENCE-VISA_2026-08-16_2027-08-15_V01.pdf"
        ),
        stored_filename=(
            "QW-00002_RESIDENCE-VISA_2026-08-16_2027-08-15_V01.pdf"
        ),
        file_size_bytes=len(b"visa document"),
        checksum_sha256=(
            "a" * 64
        ),
    )


def make_use_case() -> tuple[
    UploadEmployeeDocumentUseCase,
    MagicMock,
    MagicMock,
    MagicMock,
    AsyncMock,
    MagicMock,
    MagicMock,
    MagicMock,
    MagicMock,
]:
    employee_repository = MagicMock()
    employee_immigration_repository = MagicMock()
    employee_document_repository = MagicMock()
    authorization_service = AsyncMock()
    filename_generator = MagicMock()
    storage_key_generator = MagicMock()
    document_storage = MagicMock()
    id_generator = MagicMock()
    unit_of_work = MagicMock()

    request_context = MagicMock(spec=RequestContext)
    request_context.tenant_id = TENANT_ID
    request_context.user_id = USER_ID

    use_case = UploadEmployeeDocumentUseCase(
        employee_repository=employee_repository,
        employee_immigration_repository=employee_immigration_repository,
        employee_document_repository=employee_document_repository,
        authorization_service=authorization_service,
        filename_generator=filename_generator,
        storage_key_generator=storage_key_generator,
        document_storage=document_storage,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        request_context=request_context,
    )

    return (
        use_case,
        employee_repository,
        employee_immigration_repository,
        employee_document_repository,
        authorization_service,
        filename_generator,
        storage_key_generator,
        document_storage,
        id_generator,
        unit_of_work,
    )


@pytest.mark.anyio
async def test_upload_document_succeeds_when_authorized() -> None:
    (
        use_case,
        employees,
        immigrations,
        documents,
        authorization,
        filename_generator,
        storage_keys,
        storage,
        id_generator,
        unit_of_work
    ) = make_use_case()

    authorization.has_permission.return_value = True
    employees.get_by_id_for_tenant.return_value = make_employee()
    immigrations.get_by_id.return_value = make_immigration()
    documents.get_next_version.return_value = 1
    filename_generator.generate.return_value = (
        "QW-00002_RESIDENCE-VISA_2026-08-16_2027-08-15_V01.pdf"
    )
    storage_keys.generate.return_value = (
        "employees/QW-00002/documents/residence-visa/"
        "QW-00002_RESIDENCE-VISA_2026-08-16_2027-08-15_V01.pdf"
    )
    storage.store.return_value = make_storage_result()
    id_generator.generate.return_value = DOCUMENT_ID

    result = await use_case.execute(make_command())

    authorization.has_permission.assert_awaited_once_with(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        permission_code="HR_DOCUMENT_UPLOAD",
    )

    employees.get_by_id_for_tenant.assert_called_once_with(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
    )

    immigrations.get_by_id.assert_called_once_with(
        IMMIGRATION_ID,
    )

    documents.get_next_version.assert_called_once_with(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        document_category="residence visa",
        immigration_id=IMMIGRATION_ID,
    )

    storage.store.assert_called_once()

    documents.save.assert_called_once()
    unit_of_work.flush.assert_called_once()

    assert result.id == DOCUMENT_ID
    assert result.document_version == 1
    assert result.stored_filename == (
        "QW-00002_RESIDENCE-VISA_2026-08-16_2027-08-15_V01.pdf"
    )


@pytest.mark.anyio
async def test_upload_document_rejects_missing_permission() -> None:
    (
        use_case,
        employees,
        immigrations,
        documents,
        authorization,
        filename_generator,
        storage_keys,
        storage,
        id_generator,
        unit_of_work,
    ) = make_use_case()

    authorization.has_permission.return_value = False

    with pytest.raises(ForbiddenException):
        await use_case.execute(make_command())

    employees.get_by_id_for_tenant.assert_not_called()
    immigrations.get_by_id.assert_not_called()
    documents.save.assert_not_called()
    storage.store.assert_not_called()
    filename_generator.generate.assert_not_called()
    storage_keys.generate.assert_not_called()
    id_generator.generate.assert_not_called()


@pytest.mark.anyio
async def test_upload_document_rejects_unknown_employee() -> None:
    (
        use_case,
        employees,
        immigrations,
        documents,
        authorization,
        filename_generator,
        storage_keys,
        storage,
        id_generator,
        unit_of_work,
    ) = make_use_case()

    authorization.has_permission.return_value = True
    employees.get_by_id_for_tenant.return_value = None

    with pytest.raises(ResourceNotFoundException):
        await use_case.execute(make_command())

    immigrations.get_by_id.assert_not_called()
    documents.save.assert_not_called()
    storage.store.assert_not_called()


@pytest.mark.anyio
async def test_upload_document_rejects_unknown_immigration() -> None:
    (
        use_case,
        employees,
        immigrations,
        documents,
        authorization,
        filename_generator,
        storage_keys,
        storage,
        id_generator,
        unit_of_work,
    ) = make_use_case()

    authorization.has_permission.return_value = True
    employees.get_by_id_for_tenant.return_value = make_employee()
    immigrations.get_by_id.return_value = None

    with pytest.raises(ResourceNotFoundException):
        await use_case.execute(make_command())

    documents.save.assert_not_called()
    storage.store.assert_not_called()


@pytest.mark.anyio
async def test_upload_document_rejects_immigration_from_another_employee() -> None:
    (
        use_case,
        employees,
        immigrations,
        documents,
        authorization,
        filename_generator,
        storage_keys,
        storage,
        id_generator,
        unit_of_work,
    ) = make_use_case()

    authorization.has_permission.return_value = True
    employees.get_by_id_for_tenant.return_value = make_employee()

    immigration = make_immigration()
    immigration.employee_id = "01OTHEREMPLOYEE00000000000001"

    immigrations.get_by_id.return_value = immigration

    with pytest.raises(ResourceNotFoundException):
        await use_case.execute(make_command())

    documents.save.assert_not_called()
    storage.store.assert_not_called()


@pytest.mark.anyio
async def test_upload_document_cleans_up_file_when_metadata_save_fails() -> None:
    (
        use_case,
        employees,
        immigrations,
        documents,
        authorization,
        filename_generator,
        storage_keys,
        storage,
        id_generator,
        unit_of_work,
    ) = make_use_case()

    authorization.has_permission.return_value = True
    employees.get_by_id_for_tenant.return_value = make_employee()
    immigrations.get_by_id.return_value = make_immigration()
    documents.get_next_version.return_value = 1
    filename_generator.generate.return_value = (
        "QW-00002_RESIDENCE-VISA_2026-08-16_2027-08-15_V01.pdf"
    )
    storage_keys.generate.return_value = (
        "employees/QW-00002/documents/residence-visa/"
        "QW-00002_RESIDENCE-VISA_2026-08-16_2027-08-15_V01.pdf"
    )
    storage.store.return_value = make_storage_result()
    id_generator.generate.return_value = DOCUMENT_ID

    documents.save.side_effect = RuntimeError(
        "database failure",
    )

    with pytest.raises(
        RuntimeError,
        match="database failure",
    ):
        await use_case.execute(make_command())

    storage.delete.assert_called_once_with(
        storage_key=(
            "employees/QW-00002/documents/residence-visa/"
            "QW-00002_RESIDENCE-VISA_2026-08-16_2027-08-15_V01.pdf"
        ),
    )