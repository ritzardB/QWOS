"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_change_password_api.py

Description:
    API validation and delegation tests for changing an authenticated
    user's password.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.dependencies.identity import (
    get_change_password_use_case,
)
from qwos.main import app

SUCCESS_MESSAGE = "Password changed successfully."


def test_change_password_returns_success_response() -> None:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "ChangePasswordResponse",
        (),
        {
            "success": True,
            "message": SUCCESS_MESSAGE,
        },
    )()

    app.dependency_overrides[get_change_password_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/change-password",
            json={
                "current_password": "CurrentPassword123!",
                "new_password": "NewPassword123!",
                "confirm_password": "NewPassword123!",
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


def test_change_password_maps_request_to_command() -> None:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "ChangePasswordResponse",
        (),
        {
            "success": True,
            "message": SUCCESS_MESSAGE,
        },
    )()

    app.dependency_overrides[get_change_password_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/change-password",
            json={
                "current_password": "CurrentPassword123!",
                "new_password": "NewPassword123!",
                "confirm_password": "NewPassword123!",
            },
        )

        assert response.status_code == 200

        command = use_case.execute.await_args.args[0]

        assert command.current_password == "CurrentPassword123!"
        assert command.new_password == "NewPassword123!"

    finally:
        app.dependency_overrides.clear()


def test_change_password_unwraps_secret_passwords_before_use_case() -> None:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "ChangePasswordResponse",
        (),
        {
            "success": True,
            "message": SUCCESS_MESSAGE,
        },
    )()

    app.dependency_overrides[get_change_password_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        client.post(
            "/api/v1/identity/authentication/change-password",
            json={
                "current_password": "CurrentPassword123!",
                "new_password": "NewPassword123!",
                "confirm_password": "NewPassword123!",
            },
        )

        command = use_case.execute.await_args.args[0]

        assert isinstance(command.current_password, str)
        assert isinstance(command.new_password, str)

        assert command.current_password == "CurrentPassword123!"
        assert command.new_password == "NewPassword123!"

    finally:
        app.dependency_overrides.clear()


def test_change_password_rejects_missing_current_password() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/v1/identity/authentication/change-password",
        json={
            "new_password": "NewPassword123!",
            "confirm_password": "NewPassword123!",
        },
    )

    assert response.status_code == 422


def test_change_password_rejects_missing_new_password() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/v1/identity/authentication/change-password",
        json={
            "current_password": "CurrentPassword123!",
            "confirm_password": "NewPassword123!",
        },
    )

    assert response.status_code == 422


def test_change_password_rejects_short_new_password() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/v1/identity/authentication/change-password",
        json={
            "current_password": "CurrentPassword123!",
            "new_password": "short",
            "confirm_password": "short",
        },
    )

    assert response.status_code == 422


def test_change_password_rejects_missing_confirm_password() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/v1/identity/authentication/change-password",
        json={
            "current_password": "CurrentPassword123!",
            "new_password": "NewPassword123!",
        },
    )

    assert response.status_code == 422


def test_change_password_rejects_extra_fields() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/v1/identity/authentication/change-password",
        json={
            "current_password": "CurrentPassword123!",
            "new_password": "NewPassword123!",
            "confirm_password": "NewPassword123!",
            "unexpected": "value",
        },
    )

    assert response.status_code == 422