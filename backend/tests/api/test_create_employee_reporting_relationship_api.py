"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_create_employee_reporting_relationship_api.py
===============================================================================
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies import get_request_context
from qwos.application.common.dependencies.hr import (
    get_create_employee_reporting_relationship_use_case,
)
from qwos.main import app

EMPLOYEE_ID = "01M041AZVQKK21B7RHTZ09HJXA"
MANAGER_EMPLOYEE_ID = "01M03ZJQ8XMGC7424THFKH4HVD"
TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"


def make_payload() -> dict[str, object]:
    return {
        "manager_employee_id": MANAGER_EMPLOYEE_ID,
        "relationship_type": "primary_manager",
        "effective_from": "2026-08-16",
        "is_primary": True,
    }


def make_use_case() -> AsyncMock:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "Response",
        (),
        {
            "id": "01RELATIONSHIP00000000000001",
            "employee_id": EMPLOYEE_ID,
            "manager_employee_id": MANAGER_EMPLOYEE_ID,
            "relationship_type": "primary_manager",
            "effective_from": date(2026, 8, 16),
            "effective_to": None,
            "is_primary": True,
            "created_at": datetime(
                2026,
                8,
                16,
                12,
                0,
                tzinfo=timezone.utc,
            ),
        },
    )()

    return use_case


def install_overrides(use_case: AsyncMock) -> None:
    request_context = RequestContext(
        tenant_id=TENANT_ID,
        user_id="01KZYTCWRF8S12V28R9NX6JXS5",
        correlation_id="test-correlation-id",
        request_id="test-request-id",
        locale="en-US",
        timezone="UTC",
        ip_address=None,
        user_agent="pytest",
    )

    app.dependency_overrides[
        get_create_employee_reporting_relationship_use_case
    ] = lambda: use_case

    app.dependency_overrides[
        get_request_context
    ] = lambda: request_context


def test_assign_employee_manager_returns_created_response() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/manager",
            json=make_payload(),
        )

        assert response.status_code == 201

        assert response.json() == {
            "id": "01RELATIONSHIP00000000000001",
            "employee_id": EMPLOYEE_ID,
            "manager_employee_id": MANAGER_EMPLOYEE_ID,
            "relationship_type": "primary_manager",
            "effective_from": "2026-08-16",
            "effective_to": None,
            "is_primary": True,
            "created_at": "2026-08-16T12:00:00Z",
        }

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.tenant_id == TENANT_ID
        assert command.employee_id == EMPLOYEE_ID
        assert command.manager_employee_id == MANAGER_EMPLOYEE_ID

    finally:
        app.dependency_overrides.clear()


def test_manager_id_is_not_taken_from_employee_id_path() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["employee_id"] = "ATTACKER_EMPLOYEE"

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/manager",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_tenant_id_is_not_accepted_in_request() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["tenant_id"] = "ATTACKER_TENANT"

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/manager",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()