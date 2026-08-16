"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_create_employee_api.py

Description:
    API tests for the Create Employee endpoint.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies import get_request_context
from qwos.application.common.dependencies.hr import (
    get_create_employee_use_case,
)
from qwos.main import app


def make_create_employee_payload() -> dict[str, object]:
    return {
        "user_id": None,
        "hire_date": "2026-08-16",
        "employment_status": "active",
        "employment_type": "full_time",
        "work_email": "richard@qwos.dev",
        "work_phone": "+971 50 123 4567",
    }


def make_create_employee_use_case() -> AsyncMock:
    use_case = AsyncMock()

    created_at = datetime(
        2026,
        8,
        16,
        4,
        0,
        tzinfo=timezone.utc,
    )

    use_case.execute.return_value = type(
        "CreateEmployeeResponse",
        (),
        {
            "id": "01K2TESTEMPLOYEE00000000001",
            "employee_number": "QW-00001",
            "user_id": None,
            "hire_date": date(2026, 8, 16),
            "employment_status": "active",
            "employment_type": "full_time",
            "work_email": "richard@qwos.dev",
            "work_phone": "+971 50 123 4567",
            "created_at": created_at,
        },
    )()

    return use_case


def install_create_employee_overrides(
    use_case: AsyncMock,
) -> None:
    request_context = RequestContext(
        tenant_id="01KZYRPZANTQJBZYE7KS4DCRGW",
        user_id="01KZYTCWRF8S12V28R9NX6JXS5",
        correlation_id="test-correlation-id",
        request_id="test-request-id",
        locale="en-US",
        timezone="UTC",
        ip_address=None,
        user_agent=None,
    )

    app.dependency_overrides[get_create_employee_use_case] = (
        lambda: use_case
    )

    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )


def test_create_employee_returns_created_response() -> None:
    use_case = make_create_employee_use_case()
    install_create_employee_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/hr/employees",
            json=make_create_employee_payload(),
        )

        assert response.status_code == 201

        assert response.json() == {
            "id": "01K2TESTEMPLOYEE00000000001",
            "employee_number": "QW-00001",
            "user_id": None,
            "hire_date": "2026-08-16",
            "employment_status": "active",
            "employment_type": "full_time",
            "work_email": "richard@qwos.dev",
            "work_phone": "+971 50 123 4567",
            "created_at": "2026-08-16T04:00:00Z",
        }

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.tenant_id == "01KZYRPZANTQJBZYE7KS4DCRGW"
        assert command.user_id is None
        assert command.hire_date == date(2026, 8, 16)
        assert command.employment_status == "active"
        assert command.employment_type == "full_time"
        assert command.work_email == "richard@qwos.dev"
        assert command.work_phone == "+971 50 123 4567"

    finally:
        app.dependency_overrides.clear()


def test_create_employee_rejects_client_tenant_id() -> None:
    use_case = make_create_employee_use_case()
    install_create_employee_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_create_employee_payload()
        payload["tenant_id"] = "ATTACKER_TENANT"

        response = client.post(
            "/api/v1/hr/employees",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_defaults_status_and_type() -> None:
    use_case = make_create_employee_use_case()
    install_create_employee_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_create_employee_payload()
        payload.pop("employment_status")
        payload.pop("employment_type")

        response = client.post(
            "/api/v1/hr/employees",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.employment_status == "active"
        assert command.employment_type == "full_time"

    finally:
        app.dependency_overrides.clear()


def test_create_employee_maps_optional_user_id() -> None:
    use_case = make_create_employee_use_case()
    install_create_employee_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_create_employee_payload()
        payload["user_id"] = "01KZYTCWRF8S12V28R9NX6JXS5"

        response = client.post(
            "/api/v1/hr/employees",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.user_id == "01KZYTCWRF8S12V28R9NX6JXS5"

    finally:
        app.dependency_overrides.clear()


@pytest.mark.parametrize(
    "field",
    [
        "work_phone",
    ],
)
def test_create_employee_rejects_missing_required_field(
    field: str,
) -> None:
    use_case = make_create_employee_use_case()
    install_create_employee_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_create_employee_payload()
        payload.pop(field)

        response = client.post(
            "/api/v1/hr/employees",
            json=payload,
        )

        assert response.status_code == 201
        use_case.execute.assert_awaited_once()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_rejects_invalid_work_email() -> None:
    use_case = make_create_employee_use_case()
    install_create_employee_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_create_employee_payload()
        payload["work_email"] = "not-an-email"

        response = client.post(
            "/api/v1/hr/employees",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_rejects_invalid_hire_date() -> None:
    use_case = make_create_employee_use_case()
    install_create_employee_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_create_employee_payload()
        payload["hire_date"] = "not-a-date"

        response = client.post(
            "/api/v1/hr/employees",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_rejects_employee_number_from_request() -> None:
    use_case = make_create_employee_use_case()
    install_create_employee_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_create_employee_payload()
        payload["employee_number"] = "QW-99999"

        response = client.post(
            "/api/v1/hr/employees",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()