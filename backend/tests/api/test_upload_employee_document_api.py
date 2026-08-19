"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_upload_employee_document_api.py

Description:
    API tests for the Employee Document upload endpoint.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies import get_request_context
from qwos.application.common.dependencies.hr import (
    get_upload_employee_document_use_case,
)
from qwos.application.common.exceptions.forbidden_exception import (
    ForbiddenException,
)
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.main import app

EMPLOYEE_ID = "01M03ZJQ8XMGC7424THFKH4HVD"
TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
USER_ID = "01KZYTCWRF8S12V28R9NX6JXS5"
IMMIGRATION_ID = "01M0IMMIGRATION00000000001"
DOCUMENT_ID = "01M0DOCUMENT000000000000001"


def make_use_case() -> AsyncMock:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "UploadEmployeeDocumentResponse",
        (),
        {
            "id": DOCUMENT_ID,
            "employee_id": EMPLOYEE_ID,
            "immigration_id": IMMIGRATION_ID,
            "document_name": "Residence Visa",
            "document_category": "residence visa",
            "original_filename": "visa_scan.pdf",
            "stored_filename": (
                "QW-00002_RESIDENCE-VISA_"
                "2026-08-16_2027-08-15_V01.pdf"
            ),
            "mime_type": "application/pdf",
            "file_extension": "pdf",
            "file_size_bytes": 18,
            "storage_provider": "local",
            "storage_key": (
                "employees/QW-00002/documents/residence-visa/"
                "QW-00002_RESIDENCE-VISA_"
                "2026-08-16_2027-08-15_V01.pdf"
            ),
            "checksum_sha256": "a" * 64,
            "document_version": 1,
        },
    )()

    return use_case


def install_overrides(
    use_case: AsyncMock,
) -> None:
    request_context = RequestContext(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        correlation_id="test-correlation-id",
        request_id="test-request-id",
        locale="en-US",
        timezone="UTC",
        ip_address=None,
        user_agent=None,
    )

    app.dependency_overrides[
        get_upload_employee_document_use_case
    ] = lambda: use_case

    app.dependency_overrides[
        get_request_context
    ] = lambda: request_context


def test_upload_employee_document_returns_created_response() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/documents",
            data={
                "document_name": "Residence Visa",
                "document_category": "residence visa",
                "immigration_id": IMMIGRATION_ID,
            },
            files={
                "file": (
                    "visa_scan.pdf",
                    b"visa document data",
                    "application/pdf",
                ),
            },
        )

        assert response.status_code == 201

        assert response.json() == {
            "id": DOCUMENT_ID,
            "employee_id": EMPLOYEE_ID,
            "immigration_id": IMMIGRATION_ID,
            "document_name": "Residence Visa",
            "document_category": "residence visa",
            "original_filename": "visa_scan.pdf",
            "stored_filename": (
                "QW-00002_RESIDENCE-VISA_"
                "2026-08-16_2027-08-15_V01.pdf"
            ),
            "mime_type": "application/pdf",
            "file_extension": "pdf",
            "file_size_bytes": 18,
            "storage_provider": "local",
            "storage_key": (
                "employees/QW-00002/documents/residence-visa/"
                "QW-00002_RESIDENCE-VISA_"
                "2026-08-16_2027-08-15_V01.pdf"
            ),
            "checksum_sha256": "a" * 64,
            "document_version": 1,
        }

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.tenant_id == TENANT_ID
        assert command.employee_id == EMPLOYEE_ID
        assert command.document_name == "Residence Visa"
        assert command.document_category == "residence visa"
        assert command.original_filename == "visa_scan.pdf"
        assert command.mime_type == "application/pdf"
        assert command.file_extension == "pdf"
        assert command.content == b"visa document data"
        assert command.immigration_id == IMMIGRATION_ID

    finally:
        app.dependency_overrides.clear()


def test_upload_employee_document_uses_employee_id_from_path() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    other_employee_id = "01OTHEREMPLOYEE00000000000001"

    try:
        client = TestClient(app)

        response = client.post(
            f"/api/v1/hr/employees/{other_employee_id}/documents",
            data={
                "document_name": "Passport",
                "document_category": "passport",
            },
            files={
                "file": (
                    "passport.pdf",
                    b"passport data",
                    "application/pdf",
                ),
            },
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.employee_id == other_employee_id

    finally:
        app.dependency_overrides.clear()


def test_upload_employee_document_returns_forbidden() -> None:
    use_case = make_use_case()

    async def raise_forbidden(command: object) -> None:
        raise ForbiddenException(
            message="User is not authorized to upload employee documents.",
        )

    use_case.execute.side_effect = raise_forbidden
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/documents",
            data={
                "document_name": "Passport",
                "document_category": "passport",
            },
            files={
                "file": (
                    "passport.pdf",
                    b"passport data",
                    "application/pdf",
                ),
            },
        )

        assert response.status_code == 403

        body = response.json()

        assert body["success"] is False
        assert (
            body["message"]
            == "User is not authorized to upload employee documents."
        )

    finally:
        app.dependency_overrides.clear()


def test_upload_employee_document_returns_not_found_for_employee() -> None:
    use_case = make_use_case()

    async def raise_not_found(command: object) -> None:
        raise ResourceNotFoundException(
            resource="Employee",
            identifier=EMPLOYEE_ID,
        )

    use_case.execute.side_effect = raise_not_found
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/documents",
            data={
                "document_name": "Passport",
                "document_category": "passport",
            },
            files={
                "file": (
                    "passport.pdf",
                    b"passport data",
                    "application/pdf",
                ),
            },
        )

        assert response.status_code == 404

        body = response.json()

        assert body["success"] is False
        assert body["errors"][0]["code"] == (
            "ResourceNotFoundException"
        )

    finally:
        app.dependency_overrides.clear()


def test_upload_employee_document_returns_not_found_for_immigration() -> None:
    use_case = make_use_case()

    async def raise_not_found(command: object) -> None:
        raise ResourceNotFoundException(
            resource="EmployeeImmigration",
            identifier=IMMIGRATION_ID,
        )

    use_case.execute.side_effect = raise_not_found
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/documents",
            data={
                "document_name": "Residence Visa",
                "document_category": "residence visa",
                "immigration_id": IMMIGRATION_ID,
            },
            files={
                "file": (
                    "visa.pdf",
                    b"visa data",
                    "application/pdf",
                ),
            },
        )

        assert response.status_code == 404

        body = response.json()

        assert body["success"] is False
        assert body["errors"][0]["code"] == (
            "ResourceNotFoundException"
        )

    finally:
        app.dependency_overrides.clear()


def test_upload_employee_document_rejects_missing_filename() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/documents",
            data={
                "document_name": "Passport",
                "document_category": "passport",
            },
            files={
                "file": (
                    "",
                    b"passport data",
                    "application/pdf",
                ),
            },
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_upload_employee_document_rejects_missing_extension() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/documents",
            data={
                "document_name": "Passport",
                "document_category": "passport",
            },
            files={
                "file": (
                    "passport",
                    b"passport data",
                    "application/pdf",
                ),
            },
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()