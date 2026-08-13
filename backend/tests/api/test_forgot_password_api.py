"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_forgot_password_api.py

Description:
    API tests for the forgot-password endpoint.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.dependencies.identity import (
    get_request_password_reset_use_case,
)
from qwos.main import app

RESET_MESSAGE = (
    "If an account exists for this email address, "
    "a password reset request has been created."
)


def test_forgot_password_returns_success_response() -> None:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "RequestPasswordResetResponse",
        (),
        {
            "success": True,
            "message": RESET_MESSAGE,
        },
    )()

    app.dependency_overrides[get_request_password_reset_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/forgot-password",
            json={
                "email": "richard@example.com",
            },
        )

        assert response.status_code == 200

        assert response.json() == {
            "success": True,
            "message": RESET_MESSAGE,
        }

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.email == "richard@example.com"

    finally:
        app.dependency_overrides.clear()


def test_forgot_password_maps_email_to_command() -> None:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "RequestPasswordResetResponse",
        (),
        {
            "success": True,
            "message": RESET_MESSAGE,
        },
    )()

    app.dependency_overrides[get_request_password_reset_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/forgot-password",
            json={
                "email": "RICHARD@EXAMPLE.COM",
            },
        )

        assert response.status_code == 200

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        # The API mapper preserves the EmailStr value as a string.
        # EmailStr normalizes the domain portion before mapping.
        assert command.email == "RICHARD@example.com"

    finally:
        app.dependency_overrides.clear()


def test_forgot_password_rejects_invalid_email() -> None:
    use_case = AsyncMock()

    app.dependency_overrides[get_request_password_reset_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/forgot-password",
            json={
                "email": "not-an-email",
            },
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_forgot_password_rejects_missing_email() -> None:
    use_case = AsyncMock()

    app.dependency_overrides[get_request_password_reset_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/forgot-password",
            json={},
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()