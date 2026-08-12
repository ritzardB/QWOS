from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.dependencies.identity import (
    get_request_password_reset_use_case,
)
from qwos.main import app


def test_forgot_password_returns_success_response() -> None:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "RequestPasswordResetResponse",
        (),
        {
            "success": True,
            "message": (
                "If an account exists for this email address, "
                "a password reset request has been created."
            ),
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
            "message": (
                "If an account exists for this email address, "
                "a password reset request has been created."
            ),
        }

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.email == "richard@example.com"

    finally:
        app.dependency_overrides.clear()