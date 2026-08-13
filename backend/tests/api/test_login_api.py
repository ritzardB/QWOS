"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_login_api.py

Description:
    API validation and contract tests for user authentication.

Responsibilities:
    - Verify successful login responses
    - Verify request-to-command mapping
    - Verify SecretStr password handling
    - Verify tenant context propagation
    - Verify request validation
    - Verify response contract does not leak internal fields

Author:
    Richard Balabarcon
===============================================================================
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies.identity import (
    get_authenticate_user_use_case,
    get_request_context,
)
from qwos.main import app


def make_request_context() -> RequestContext:
    return RequestContext(
        tenant_id="01HTENANT000000000000000001",
        user_id=None,
        correlation_id="test-correlation-id",
        request_id="test-request-id",
        locale="en-US",
        timezone="UTC",
        ip_address="127.0.0.1",
        user_agent="pytest",
    )


def make_successful_response() -> object:
    return type(
        "AuthenticateUserResponse",
        (),
        {
            "access_token": "access-token",
            "refresh_token": "refresh-token",
            "token_type": "Bearer",
            "expires_at": datetime(
                2026,
                8,
                12,
                10,
                30,
                tzinfo=timezone.utc,
            ),
            "user_id": "01USER000000000000000000001",
            "session_id": "01SESSION000000000000000001",
        },
    )()


def test_login_returns_successful_authentication_response() -> None:
    use_case = AsyncMock()
    use_case.execute.return_value = make_successful_response()

    request_context = make_request_context()

    app.dependency_overrides[get_authenticate_user_use_case] = (
        lambda: use_case
    )
    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/login",
            json={
                "email": "richard@example.com",
                "password": "SecurePassword123!",
                "remember_me": False,
            },
        )

        assert response.status_code == 200

        assert response.json() == {
            "access_token": "access-token",
            "refresh_token": "refresh-token",
            "token_type": "Bearer",
            "expires_at": "2026-08-12T10:30:00Z",
        }

        use_case.execute.assert_awaited_once()

    finally:
        app.dependency_overrides.clear()


def test_login_maps_email_to_command() -> None:
    use_case = AsyncMock()
    use_case.execute.return_value = make_successful_response()

    request_context = make_request_context()

    app.dependency_overrides[get_authenticate_user_use_case] = (
        lambda: use_case
    )
    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/login",
            json={
                "email": "richard@example.com",
                "password": "SecurePassword123!",
            },
        )

        assert response.status_code == 200

        command = use_case.execute.await_args.args[0]

        assert command.email == "richard@example.com"

    finally:
        app.dependency_overrides.clear()


def test_login_unwraps_password_before_application_boundary() -> None:
    use_case = AsyncMock()
    use_case.execute.return_value = make_successful_response()

    request_context = make_request_context()

    app.dependency_overrides[get_authenticate_user_use_case] = (
        lambda: use_case
    )
    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/login",
            json={
                "email": "richard@example.com",
                "password": "SecurePassword123!",
            },
        )

        assert response.status_code == 200

        command = use_case.execute.await_args.args[0]

        assert command.password == "SecurePassword123!"

    finally:
        app.dependency_overrides.clear()


def test_login_maps_remember_me_to_command() -> None:
    use_case = AsyncMock()
    use_case.execute.return_value = make_successful_response()

    request_context = make_request_context()

    app.dependency_overrides[get_authenticate_user_use_case] = (
        lambda: use_case
    )
    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/login",
            json={
                "email": "richard@example.com",
                "password": "SecurePassword123!",
                "remember_me": True,
            },
        )

        assert response.status_code == 200

        command = use_case.execute.await_args.args[0]

        assert command.remember_me is True

    finally:
        app.dependency_overrides.clear()


def test_login_propagates_tenant_context_to_command() -> None:
    use_case = AsyncMock()
    use_case.execute.return_value = make_successful_response()

    request_context = make_request_context()

    app.dependency_overrides[get_authenticate_user_use_case] = (
        lambda: use_case
    )
    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/login",
            json={
                "email": "richard@example.com",
                "password": "SecurePassword123!",
            },
        )

        assert response.status_code == 200

        command = use_case.execute.await_args.args[0]

        assert command.tenant_id == request_context.tenant_id

    finally:
        app.dependency_overrides.clear()


def test_login_defaults_remember_me_to_false() -> None:
    use_case = AsyncMock()
    use_case.execute.return_value = make_successful_response()

    request_context = make_request_context()

    app.dependency_overrides[get_authenticate_user_use_case] = (
        lambda: use_case
    )
    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/login",
            json={
                "email": "richard@example.com",
                "password": "SecurePassword123!",
            },
        )

        assert response.status_code == 200

        command = use_case.execute.await_args.args[0]

        assert command.remember_me is False

    finally:
        app.dependency_overrides.clear()


def test_login_rejects_missing_email() -> None:
    use_case = AsyncMock()
    request_context = make_request_context()

    app.dependency_overrides[get_authenticate_user_use_case] = (
        lambda: use_case
    )
    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/login",
            json={
                "password": "SecurePassword123!",
            },
        )

        assert response.status_code == 422

        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_login_rejects_invalid_email() -> None:
    use_case = AsyncMock()
    request_context = make_request_context()

    app.dependency_overrides[get_authenticate_user_use_case] = (
        lambda: use_case
    )
    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/login",
            json={
                "email": "not-an-email",
                "password": "SecurePassword123!",
            },
        )

        assert response.status_code == 422

        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_login_rejects_missing_password() -> None:
    use_case = AsyncMock()
    request_context = make_request_context()

    app.dependency_overrides[get_authenticate_user_use_case] = (
        lambda: use_case
    )
    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/login",
            json={
                "email": "richard@example.com",
            },
        )

        assert response.status_code == 422

        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_login_rejects_short_password() -> None:
    use_case = AsyncMock()
    request_context = make_request_context()

    app.dependency_overrides[get_authenticate_user_use_case] = (
        lambda: use_case
    )
    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/login",
            json={
                "email": "richard@example.com",
                "password": "short",
            },
        )

        assert response.status_code == 422

        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_login_does_not_expose_internal_identity_fields() -> None:
    use_case = AsyncMock()
    use_case.execute.return_value = make_successful_response()

    request_context = make_request_context()

    app.dependency_overrides[get_authenticate_user_use_case] = (
        lambda: use_case
    )
    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/login",
            json={
                "email": "richard@example.com",
                "password": "SecurePassword123!",
            },
        )

        assert response.status_code == 200

        body = response.json()

        assert "user_id" not in body
        assert "session_id" not in body

    finally:
        app.dependency_overrides.clear()