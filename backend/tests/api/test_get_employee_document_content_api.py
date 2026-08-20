"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_get_employee_document_content_api.py

Description:
    API tests for retrieving employee document content.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies import (
    get_authenticated_request_context,
)
from qwos.application.common.dependencies.hr import (
    get_get_employee_document_content_use_case,
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
DOCUMENT_ID = "01M0DOCUMENT000000000000001"


def make_use_case() -> AsyncMock:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "GetEmployeeDocumentContentResponse",
        (),
        {
            "id": DOCUMENT_ID,
            "employee_id": EMPLOYEE_ID,
            "filename": "richard Passport_new.jpg",
            "mime_type": "image/jpeg",
            "content": b"passport image data",
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
        get_get_employee_document_content_use_case
    ] = lambda: use_case

    app.dependency_overrides[
        get_authenticated_request_context
    ] = lambda: request_context


def test_get_employee_document_content_returns_file() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/documents/{DOCUMENT_ID}/content",
        )

        assert response.status_code == 200
        assert response.content == b"passport image data"

        assert response.headers["content-type"] == (
            "image/jpeg"
        )

        assert response.headers["content-disposition"] == (
            'inline; filename="richard Passport_new.jpg"'
        )

        use_case.execute.assert_awaited_once()

        call = use_case.execute.await_args.kwargs

        assert call["employee_id"] == EMPLOYEE_ID
        assert call["document_id"] == DOCUMENT_ID

    finally:
        app.dependency_overrides.clear()


def test_get_employee_document_content_returns_pdf() -> None:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "GetEmployeeDocumentContentResponse",
        (),
        {
            "id": DOCUMENT_ID,
            "employee_id": EMPLOYEE_ID,
            "filename": "residence_visa.pdf",
            "mime_type": "application/pdf",
            "content": b"%PDF-test-content",
        },
    )()

    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/documents/{DOCUMENT_ID}/content",
        )

        assert response.status_code == 200
        assert response.content == b"%PDF-test-content"

        assert response.headers["content-type"] == (
            "application/pdf"
        )

        assert response.headers["content-disposition"] == (
            'inline; filename="residence_visa.pdf"'
        )

    finally:
        app.dependency_overrides.clear()


def test_get_employee_document_content_returns_forbidden() -> None:
    use_case = make_use_case()

    async def raise_forbidden(
        **_: object,
    ) -> None:
        raise ForbiddenException(
            message=(
                "User is not authorized to view "
                "employee documents."
            ),
        )

    use_case.execute.side_effect = raise_forbidden

    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/documents/{DOCUMENT_ID}/content",
        )

        assert response.status_code == 403

        body = response.json()

        assert body["success"] is False
        assert (
            body["message"]
            == (
                "User is not authorized to view "
                "employee documents."
            )
        )

        use_case.execute.assert_awaited_once()

    finally:
        app.dependency_overrides.clear()


def test_get_employee_document_content_returns_not_found() -> None:
    use_case = make_use_case()

    async def raise_not_found(
        **_: object,
    ) -> None:
        raise ResourceNotFoundException(
            resource="EmployeeDocument",
            identifier=DOCUMENT_ID,
        )

    use_case.execute.side_effect = raise_not_found

    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/documents/{DOCUMENT_ID}/content",
        )

        assert response.status_code == 404

        body = response.json()

        assert body["success"] is False
        assert body["errors"][0]["code"] == (
            "ResourceNotFoundException"
        )

        use_case.execute.assert_awaited_once()

    finally:
        app.dependency_overrides.clear()


def test_get_employee_document_content_uses_employee_id_from_path() -> None:
    use_case = make_use_case()

    other_employee_id = (
        "01OTHEREMPLOYEE00000000000001"
    )

    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            f"/api/v1/hr/employees/"
            f"{other_employee_id}/documents/"
            f"{DOCUMENT_ID}/content",
        )

        assert response.status_code == 200

        use_case.execute.assert_awaited_once()

        call = use_case.execute.await_args.kwargs

        assert call["employee_id"] == (
            other_employee_id
        )
        assert call["document_id"] == DOCUMENT_ID

    finally:
        app.dependency_overrides.clear()


def test_get_employee_document_content_handles_unknown_mime_type() -> None:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "GetEmployeeDocumentContentResponse",
        (),
        {
            "id": DOCUMENT_ID,
            "employee_id": EMPLOYEE_ID,
            "filename": "unknown_file.bin",
            "mime_type": None,
            "content": b"binary document content",
        },
    )()

    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/documents/{DOCUMENT_ID}/content",
        )

        assert response.status_code == 200
        assert response.content == (
            b"binary document content"
        )

        assert response.headers["content-type"] == (
            "application/octet-stream"
        )

    finally:
        app.dependency_overrides.clear()


def test_get_employee_document_content_sanitizes_filename() -> None:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "GetEmployeeDocumentContentResponse",
        (),
        {
            "id": DOCUMENT_ID,
            "employee_id": EMPLOYEE_ID,
            "filename": 'passport "final".jpg',
            "mime_type": "image/jpeg",
            "content": b"passport data",
        },
    )()

    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/documents/{DOCUMENT_ID}/content",
        )

        assert response.status_code == 200

        content_disposition = response.headers[
            "content-disposition"
        ]

        assert '"' not in content_disposition[
            len("inline; filename=") + 1 : -1
        ]

    finally:
        app.dependency_overrides.clear()