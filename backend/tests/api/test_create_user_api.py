from datetime import datetime, timezone
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies.identity import (
    get_create_user_use_case,
    get_request_context,
)
from qwos.domains.identity.enums.account_status import AccountStatus
from qwos.domains.identity.enums.user_type import UserType
from qwos.main import app


def test_create_user_returns_created_response() -> None:
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

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/identity/users",
            json={
                "email": "richard@example.com",
                "username": "richard",
                "password": "SecurePassword123!",
                "first_name": "Richard",
                "middle_name": None,
                "last_name": "Balabarcon",
                "preferred_name": "Richard",
                "user_type": "EMPLOYEE",
            },
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