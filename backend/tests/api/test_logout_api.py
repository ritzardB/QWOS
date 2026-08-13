"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_logout_api.py

Description:
    API validation and delegation tests for terminating an authenticated
    user's session.

Responsibilities:
    - Verify successful logout responses
    - Verify request-to-command mapping
    - Verify SecretStr refresh token handling
    - Verify tenant context propagation
    - Verify request validation
    - Verify response contract does not leak the refresh token

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies.identity import (
    get_logout_user_use_case,
    get_request_context,
)
from qwos.main import app

SUCCESS_MESSAGE = "User logged out successfully."

REFRESH_TOKEN = (
    "eyJhbGciOiJIUzI1NiIs"
    ".eyJzdWIiOiIwMVVTRVIwMDAwMDAwMDAwMDAwMDAwMDAwMSIs"
    ".test-signature"
)


def make_request_context() -> RequestContext:
    return RequestContext(
        tenant_id="01HTENANT000000000000000001",
        user_id="01USER000000000000000000001",
        correlation_id="test-correlation-id",
        request_id="test-request-id",
        locale="en-US",
        timezone="UTC",
        ip_address="127.0.0.1",
        user_agent="pytest",
    )


def make_successful_response() -> object:
    return type(
        "LogoutUserResponse",
        (),
        {
            "success": True,
            "message": SUCCESS_MESSAGE,
        },
    )()


def test_logout_returns_success_response() -> None:
    use_case = AsyncMock()
    use_case.execute.return_value = make_successful_response()

    request_context = make_request_context()

    app.dependency_overrides[get_logout_user_use_case] = (
        lambda: use_case
    )
    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/logout",
            json={
                "refresh_token": REFRESH_TOKEN,
            },
        )

        assert response.status_code == 200

        assert response.json() == {
            "success": True,
            "message": SUCCESS_MESSAGE,
        }

        use_case.execute.assert_awaited_once()

    finally:
        app.dependency_overrides.clear()


def test_logout_maps_refresh_token_to_command() -> None:
    use_case = AsyncMock()
    use_case.execute.return_value = make_successful_response()

    request_context = make_request_context()

    app.dependency_overrides[get_logout_user_use_case] = (
        lambda: use_case
    )
    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/logout",
            json={
                "refresh_token": REFRESH_TOKEN,
            },
        )

        assert response.status_code == 200

        command = use_case.execute.await_args.args[0]

        assert command.refresh_token == REFRESH_TOKEN

    finally:
        app.dependency_overrides.clear()


def test_logout_unwraps_refresh_token_before_use_case() -> None:
    use_case = AsyncMock()
    use_case.execute.return_value = make_successful_response()

    request_context = make_request_context()

    app.dependency_overrides[get_logout_user_use_case] = (
        lambda: use_case
    )
    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/logout",
            json={
                "refresh_token": REFRESH_TOKEN,
            },
        )

        assert response.status_code == 200

        command = use_case.execute.await_args.args[0]

        assert isinstance(command.refresh_token, str)
        assert command.refresh_token == REFRESH_TOKEN

    finally:
        app.dependency_overrides.clear()


def test_logout_propagates_tenant_context_to_command() -> None:
    use_case = AsyncMock()
    use_case.execute.return_value = make_successful_response()

    request_context = make_request_context()

    app.dependency_overrides[get_logout_user_use_case] = (
        lambda: use_case
    )
    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/logout",
            json={
                "refresh_token": REFRESH_TOKEN,
            },
        )

        assert response.status_code == 200

        command = use_case.execute.await_args.args[0]

        assert command.tenant_id == request_context.tenant_id

    finally:
        app.dependency_overrides.clear()


def test_logout_rejects_missing_refresh_token() -> None:
    use_case = AsyncMock()

    app.dependency_overrides[get_logout_user_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/logout",
            json={},
        )

        assert response.status_code == 422

        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_logout_rejects_null_refresh_token() -> None:
    use_case = AsyncMock()

    app.dependency_overrides[get_logout_user_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/logout",
            json={
                "refresh_token": None,
            },
        )

        assert response.status_code == 422

        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_logout_rejects_extra_fields() -> None:
    use_case = AsyncMock()

    app.dependency_overrides[get_logout_user_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/logout",
            json={
                "refresh_token": REFRESH_TOKEN,
                "unexpected": "value",
            },
        )

        assert response.status_code == 422

        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_logout_does_not_expose_refresh_token_in_response() -> None:
    use_case = AsyncMock()
    use_case.execute.return_value = make_successful_response()

    request_context = make_request_context()

    app.dependency_overrides[get_logout_user_use_case] = (
        lambda: use_case
    )
    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/logout",
            json={
                "refresh_token": REFRESH_TOKEN,
            },
        )

        assert response.status_code == 200

        body = response.json()

        assert "refresh_token" not in body
        assert "token" not in body

    finally:
        app.dependency_overrides.clear()


def test_logout_does_not_expose_internal_identity_fields() -> None:
    use_case = AsyncMock()
    use_case.execute.return_value = make_successful_response()

    request_context = make_request_context()

    app.dependency_overrides[get_logout_user_use_case] = (
        lambda: use_case
    )
    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/logout",
            json={
                "refresh_token": REFRESH_TOKEN,
            },
        )

        assert response.status_code == 200

        body = response.json()

        assert "user_id" not in body
        assert "session_id" not in body
        assert "tenant_id" not in body

    finally:
        app.dependency_overrides.clear()