"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_refresh_token_api.py

Description:
    API validation and delegation tests for refreshing authentication tokens.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.dependencies.identity import (
    get_refresh_access_token_use_case,
)
from qwos.main import app


def make_successful_response() -> object:
    return type(
        "RefreshAccessTokenResponse",
        (),
        {
            "access_token": "new-access-token",
            "refresh_token": "new-refresh-token",
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


def test_refresh_token_returns_successful_response() -> None:
    use_case = AsyncMock()
    use_case.execute.return_value = make_successful_response()

    app.dependency_overrides[get_refresh_access_token_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/refresh",
            json={
                "refresh_token": "refresh-token",
            },
        )

        assert response.status_code == 200

        assert response.json() == {
            "access_token": "new-access-token",
            "refresh_token": "new-refresh-token",
            "expires_at": "2026-08-12T10:30:00Z",
        }

        use_case.execute.assert_awaited_once()

    finally:
        app.dependency_overrides.clear()


def test_refresh_token_maps_request_to_command() -> None:
    use_case = AsyncMock()
    use_case.execute.return_value = make_successful_response()

    app.dependency_overrides[get_refresh_access_token_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/refresh",
            json={
                "refresh_token": "refresh-token",
            },
        )

        assert response.status_code == 200

        command = use_case.execute.await_args.args[0]

        assert command.refresh_token == "refresh-token"

    finally:
        app.dependency_overrides.clear()


def test_refresh_token_unwraps_secret_token_before_use_case() -> None:
    use_case = AsyncMock()
    use_case.execute.return_value = make_successful_response()

    app.dependency_overrides[get_refresh_access_token_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/refresh",
            json={
                "refresh_token": "refresh-token",
            },
        )

        assert response.status_code == 200

        command = use_case.execute.await_args.args[0]

        assert isinstance(command.refresh_token, str)
        assert command.refresh_token == "refresh-token"

    finally:
        app.dependency_overrides.clear()


def test_refresh_token_rejects_missing_refresh_token() -> None:
    use_case = AsyncMock()

    app.dependency_overrides[get_refresh_access_token_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/refresh",
            json={},
        )

        assert response.status_code == 422

        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_refresh_token_rejects_extra_fields() -> None:
    use_case = AsyncMock()

    app.dependency_overrides[get_refresh_access_token_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/refresh",
            json={
                "refresh_token": "refresh-token",
                "unexpected": "value",
            },
        )

        assert response.status_code == 422

        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_refresh_token_does_not_expose_internal_identity_fields() -> None:
    use_case = AsyncMock()
    use_case.execute.return_value = make_successful_response()

    app.dependency_overrides[get_refresh_access_token_use_case] = (
        lambda: use_case
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/authentication/refresh",
            json={
                "refresh_token": "refresh-token",
            },
        )

        assert response.status_code == 200

        body = response.json()

        assert "user_id" not in body
        assert "session_id" not in body
        assert "token_type" not in body

    finally:
        app.dependency_overrides.clear()