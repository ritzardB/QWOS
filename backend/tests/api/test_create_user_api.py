"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_create_user_api.py

Description:
    API tests for the Create User endpoint.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies.identity import (
    get_create_user_use_case,
    get_request_context,
)
from qwos.domains.identity.enums.account_status import AccountStatus
from qwos.domains.identity.enums.user_type import UserType
from qwos.main import app


def make_create_user_payload() -> dict[str, object]:
    return {
        "email": "richard@example.com",
        "username": "richard",
        "password": "SecurePassword123!",
        "first_name": "Richard",
        "middle_name": None,
        "last_name": "Balabarcon",
        "preferred_name": "Richard",
        "user_type": "EMPLOYEE",
    }


def make_create_user_use_case() -> AsyncMock:
    use_case = AsyncMock()

    created_at = datetime(
        2026,
        8,
        12,
        10,
        30,
        tzinfo=timezone.utc,
    )

    use_case.execute.return_value = type(
        "CreateUserResponse",
        (),
        {
            "id": "01K2TESTUSER00000000000000",
            "first_name": "Richard",
            "last_name": "Balabarcon",
            "email": "richard@example.com",
            "username": "richard",
            "user_type": UserType.EMPLOYEE,
            "account_status": AccountStatus.PENDING,
            "created_at": created_at,
        },
    )()

    return use_case


def install_create_user_overrides(
    use_case: AsyncMock,
) -> None:
    request_context = RequestContext(
        tenant_id="default",
        user_id=None,
        correlation_id="test-correlation-id",
        request_id="test-request-id",
        locale="en-US",
        timezone="UTC",
        ip_address=None,
        user_agent=None,
    )

    app.dependency_overrides[get_create_user_use_case] = (
        lambda: use_case
    )
    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )


def test_create_user_returns_created_response() -> None:
    use_case = make_create_user_use_case()
    install_create_user_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/users",
            json=make_create_user_payload(),
        )

        assert response.status_code == 201

        assert response.json() == {
            "id": "01K2TESTUSER00000000000000",
            "email": "richard@example.com",
            "username": "richard",
            "user_type": "EMPLOYEE",
            "account_status": "PENDING",
            "created_at": "2026-08-12T10:30:00Z",
        }

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.email == "richard@example.com"
        assert command.username == "richard"
        assert command.password == "SecurePassword123!"
        assert command.first_name == "Richard"
        assert command.middle_name is None
        assert command.last_name == "Balabarcon"
        assert command.preferred_name == "Richard"
        assert command.user_type == UserType.EMPLOYEE
        assert command.tenant_id == "default"

    finally:
        app.dependency_overrides.clear()


def test_create_user_defaults_user_type_to_employee() -> None:
    use_case = make_create_user_use_case()
    install_create_user_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_create_user_payload()
        payload.pop("user_type")

        response = client.post(
            "/api/v1/identity/users",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.user_type == UserType.EMPLOYEE

    finally:
        app.dependency_overrides.clear()


@pytest.mark.parametrize(
    "field",
    [
        "email",
        "username",
        "password",
        "first_name",
        "last_name",
    ],
)
def test_create_user_rejects_missing_required_field(
    field: str,
) -> None:
    use_case = make_create_user_use_case()
    install_create_user_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_create_user_payload()
        payload.pop(field)

        response = client.post(
            "/api/v1/identity/users",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_user_rejects_invalid_email() -> None:
    use_case = make_create_user_use_case()
    install_create_user_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_create_user_payload()
        payload["email"] = "not-an-email"

        response = client.post(
            "/api/v1/identity/users",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_user_rejects_short_username() -> None:
    use_case = make_create_user_use_case()
    install_create_user_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_create_user_payload()
        payload["username"] = "ab"

        response = client.post(
            "/api/v1/identity/users",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_user_rejects_short_password() -> None:
    use_case = make_create_user_use_case()
    install_create_user_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_create_user_payload()
        payload["password"] = "short"

        response = client.post(
            "/api/v1/identity/users",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_user_rejects_invalid_user_type() -> None:
    use_case = make_create_user_use_case()
    install_create_user_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_create_user_payload()
        payload["user_type"] = "INVALID_USER_TYPE"

        response = client.post(
            "/api/v1/identity/users",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_user_maps_optional_fields() -> None:
    use_case = make_create_user_use_case()
    install_create_user_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_create_user_payload()
        payload["middle_name"] = "Michael"
        payload["preferred_name"] = "Rick"

        response = client.post(
            "/api/v1/identity/users",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.middle_name == "Michael"
        assert command.preferred_name == "Rick"

    finally:
        app.dependency_overrides.clear()