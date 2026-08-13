"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_reset_password_api.py

Description:
    API tests for the reset-password endpoint.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.dependencies.identity import (
    get_reset_password_use_case,
)
from qwos.main import app


def test_reset_password_returns_success_response() -> None:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "ResetPasswordResponse",
        (),
        {
            "success": True,
            "message": "Password reset successfully.",
        },
    )()

    app.dependency_overrides[get_reset_password_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/reset-password",
            json={
                "token": "test-reset-token",
                "new_password": "SecurePassword123!",
                "confirm_password": "SecurePassword123!",
            },
        )

        assert response.status_code == 200

        assert response.json() == {
            "success": True,
            "message": "Password reset successfully.",
        }

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.token == "test-reset-token"
        assert command.new_password == "SecurePassword123!"
        assert command.confirm_password == "SecurePassword123!"

    finally:
        app.dependency_overrides.clear()


def test_reset_password_rejects_missing_token() -> None:
    use_case = AsyncMock()

    app.dependency_overrides[get_reset_password_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/reset-password",
            json={
                "new_password": "SecurePassword123!",
                "confirm_password": "SecurePassword123!",
            },
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_reset_password_rejects_short_new_password() -> None:
    use_case = AsyncMock()

    app.dependency_overrides[get_reset_password_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/reset-password",
            json={
                "token": "test-reset-token",
                "new_password": "short",
                "confirm_password": "short",
            },
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_reset_password_rejects_short_confirm_password() -> None:
    use_case = AsyncMock()

    app.dependency_overrides[get_reset_password_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/reset-password",
            json={
                "token": "test-reset-token",
                "new_password": "SecurePassword123!",
                "confirm_password": "short",
            },
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_reset_password_rejects_missing_new_password() -> None:
    use_case = AsyncMock()

    app.dependency_overrides[get_reset_password_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/reset-password",
            json={
                "token": "test-reset-token",
                "confirm_password": "SecurePassword123!",
            },
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_reset_password_rejects_missing_confirm_password() -> None:
    use_case = AsyncMock()

    app.dependency_overrides[get_reset_password_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/reset-password",
            json={
                "token": "test-reset-token",
                "new_password": "SecurePassword123!",
            },
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_reset_password_unwraps_secret_passwords_before_use_case() -> None:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "ResetPasswordResponse",
        (),
        {
            "success": True,
            "message": "Password reset successfully.",
        },
    )()

    app.dependency_overrides[get_reset_password_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/reset-password",
            json={
                "token": "test-reset-token",
                "new_password": "SecurePassword123!",
                "confirm_password": "SecurePassword123!",
            },
        )

        assert response.status_code == 200

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        # AuthenticationMapper explicitly unwraps SecretStr.
        assert command.new_password == "SecurePassword123!"
        assert command.confirm_password == "SecurePassword123!"

    finally:
        app.dependency_overrides.clear()