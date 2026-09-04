"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_create_leave_type_api.py

Description:
    API tests for the Create Leave Type endpoint.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies import get_request_context
from qwos.application.common.dependencies.authentication import (
    get_authenticated_request_context,
)
from qwos.application.common.dependencies.leave import (
    get_create_leave_type_use_case,
)
from qwos.main import app

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
USER_ID = "01KZYTCWRF8S12V28R9NX6JXS5"


def make_payload() -> dict[str, object]:
    return {
        "leave_code": "annual",
        "leave_name": "Annual Leave",
        "description": "Paid annual vacation leave.",
        "is_paid": True,
        "is_active": True,
    }


def make_request_context() -> RequestContext:
    return RequestContext(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        correlation_id="test-correlation-id",
        request_id="test-request-id",
        locale="en-US",
        timezone="UTC",
        ip_address=None,
        user_agent=None,
    )


def make_use_case() -> AsyncMock:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "CreateLeaveTypeResponse",
        (),
        {
            "id": "01K2TESTLEAVETYPE00000001",
            "leave_code": "annual",
            "leave_name": "Annual Leave",
            "description": "Paid annual vacation leave.",
            "is_paid": True,
            "is_active": True,
            "created_at": datetime(
                2026,
                9,
                1,
                4,
                0,
                tzinfo=timezone.utc,
            ),
        },
    )()

    return use_case


def install_overrides(
    use_case: AsyncMock,
) -> None:
    request_context = make_request_context()

    app.dependency_overrides[get_create_leave_type_use_case] = (
        lambda: use_case
    )

    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    app.dependency_overrides[get_authenticated_request_context] = (
        lambda: request_context
    )


def test_create_leave_type_returns_created_response() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/leave/types",
            json=make_payload(),
        )

        assert response.status_code == 201

        assert response.json() == {
            "id": "01K2TESTLEAVETYPE00000001",
            "leave_code": "annual",
            "leave_name": "Annual Leave",
            "description": "Paid annual vacation leave.",
            "is_paid": True,
            "is_active": True,
            "created_at": "2026-09-01T04:00:00Z",
        }

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.tenant_id == TENANT_ID
        assert command.leave_code == "annual"
        assert command.leave_name == "Annual Leave"
        assert command.description == "Paid annual vacation leave."
        assert command.is_paid is True
        assert command.is_active is True

    finally:
        app.dependency_overrides.clear()


def test_create_leave_type_does_not_accept_client_tenant_id() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["tenant_id"] = "ATTACKER_TENANT"

        response = client.post(
            "/api/v1/leave/types",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_leave_type_defaults_to_paid() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("is_paid")

        response = client.post(
            "/api/v1/leave/types",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.is_paid is True

    finally:
        app.dependency_overrides.clear()


def test_create_leave_type_defaults_to_active() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("is_active")

        response = client.post(
            "/api/v1/leave/types",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.is_active is True

    finally:
        app.dependency_overrides.clear()


def test_create_leave_type_rejects_missing_leave_code() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("leave_code")

        response = client.post(
            "/api/v1/leave/types",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_leave_type_rejects_missing_leave_name() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("leave_name")

        response = client.post(
            "/api/v1/leave/types",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_leave_type_accepts_unpaid_leave() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["is_paid"] = False

        response = client.post(
            "/api/v1/leave/types",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.is_paid is False

    finally:
        app.dependency_overrides.clear()