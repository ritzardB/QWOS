"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_create_employee_leave_assignment_api.py

Description:
    API tests for the Create Employee Leave Assignment endpoint.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies import get_request_context
from qwos.application.common.dependencies.authentication import (
    get_authenticated_request_context,
)
from qwos.application.common.dependencies.leave import (
    get_create_employee_leave_assignment_use_case,
)
from qwos.main import app

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
USER_ID = "01KZYTCWRF8S12V28R9NX6JXS5"
EMPLOYEE_ID = "01K2TESTEMPLOYEE00000001"
LEAVE_POLICY_ID = "01K2TESTLEAVEPOLICY0000001"


def make_payload() -> dict[str, object]:
    return {
        "employee_id": EMPLOYEE_ID,
        "leave_policy_id": LEAVE_POLICY_ID,
        "effective_from": "2026-09-01",
        "effective_until": "2026-12-31",
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
        "CreateEmployeeLeaveAssignmentResponse",
        (),
        {
            "id": "01K2TESTLEAVEASSIGNMENT01",
            "employee_id": EMPLOYEE_ID,
            "leave_policy_id": LEAVE_POLICY_ID,
            "effective_from": date(2026, 9, 1),
            "effective_until": date(2026, 12, 31),
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

    app.dependency_overrides[get_create_employee_leave_assignment_use_case] = (
        lambda: use_case
    )

    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    app.dependency_overrides[get_authenticated_request_context] = (
        lambda: request_context
    )


def test_create_employee_leave_assignment_returns_created_response() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/leave/employee-assignments",
            json=make_payload(),
        )

        assert response.status_code == 201

        assert response.json() == {
            "id": "01K2TESTLEAVEASSIGNMENT01",
            "employee_id": EMPLOYEE_ID,
            "leave_policy_id": LEAVE_POLICY_ID,
            "effective_from": "2026-09-01",
            "effective_until": "2026-12-31",
            "is_active": True,
            "created_at": "2026-09-01T04:00:00Z",
        }

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.tenant_id == TENANT_ID
        assert command.employee_id == EMPLOYEE_ID
        assert command.leave_policy_id == LEAVE_POLICY_ID
        assert command.effective_from == date(2026, 9, 1)
        assert command.effective_until == date(2026, 12, 31)
        assert command.is_active is True

    finally:
        app.dependency_overrides.clear()


def test_create_employee_leave_assignment_does_not_accept_client_tenant_id() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["tenant_id"] = "ATTACKER_TENANT"

        response = client.post(
            "/api/v1/leave/employee-assignments",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_leave_assignment_allows_open_ended_assignment() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["effective_until"] = None

        response = client.post(
            "/api/v1/leave/employee-assignments",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.effective_until is None

    finally:
        app.dependency_overrides.clear()


def test_create_employee_leave_assignment_defaults_to_active() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("is_active")

        response = client.post(
            "/api/v1/leave/employee-assignments",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.is_active is True

    finally:
        app.dependency_overrides.clear()


def test_create_employee_leave_assignment_requires_employee_id() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("employee_id")

        response = client.post(
            "/api/v1/leave/employee-assignments",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_leave_assignment_requires_leave_policy_id() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("leave_policy_id")

        response = client.post(
            "/api/v1/leave/employee-assignments",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_leave_assignment_requires_effective_from() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("effective_from")

        response = client.post(
            "/api/v1/leave/employee-assignments",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_leave_assignment_rejects_invalid_date_range() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["effective_from"] = "2026-12-31"
        payload["effective_until"] = "2026-09-01"

        response = client.post(
            "/api/v1/leave/employee-assignments",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.effective_from == date(2026, 12, 31)
        assert command.effective_until == date(2026, 9, 1)

    finally:
        app.dependency_overrides.clear()