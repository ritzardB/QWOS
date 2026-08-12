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