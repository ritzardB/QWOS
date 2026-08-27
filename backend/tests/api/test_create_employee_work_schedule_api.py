"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_create_employee_work_schedule_api.py

Description:
    API tests for the Create Employee Work Schedule endpoint.

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
from qwos.application.common.dependencies.attendance import (
    get_create_employee_work_schedule_use_case,
)
from qwos.application.common.dependencies.authentication import (
    get_authenticated_request_context,
)
from qwos.main import app

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
USER_ID = "01KZYTCWRF8S12V28R9NX6JXS5"
EMPLOYEE_ID = "01K2TESTEMPLOYEE00000000001"
SCHEDULE_ID = "01K2TESTSCHEDULE000000001"


def make_payload() -> dict[str, object]:
    return {
        "work_schedule_id": SCHEDULE_ID,
        "effective_from": "2026-09-01",
        "effective_until": None,
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
        "CreateEmployeeWorkScheduleResponse",
        (),
        {
            "id": "01K2TESTEWS000000000000001",
            "employee_id": EMPLOYEE_ID,
            "work_schedule_id": SCHEDULE_ID,
            "effective_from": date(2026, 9, 1),
            "effective_until": None,
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

    app.dependency_overrides[get_create_employee_work_schedule_use_case] = (
        lambda: use_case
    )

    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    app.dependency_overrides[get_authenticated_request_context] = (
        lambda: request_context
    )


def test_create_employee_work_schedule_returns_created_response() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.post(
            f"/api/v1/attendance/employees/{EMPLOYEE_ID}/work-schedules",
            json=make_payload(),
        )

        assert response.status_code == 201

        assert response.json() == {
            "id": "01K2TESTEWS000000000000001",
            "employee_id": EMPLOYEE_ID,
            "work_schedule_id": SCHEDULE_ID,
            "effective_from": "2026-09-01",
            "effective_until": None,
            "is_active": True,
            "created_at": "2026-09-01T04:00:00Z",
        }

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.tenant_id == TENANT_ID
        assert command.employee_id == EMPLOYEE_ID
        assert command.work_schedule_id == SCHEDULE_ID
        assert command.effective_from == date(2026, 9, 1)
        assert command.effective_until is None
        assert command.is_active is True

    finally:
        app.dependency_overrides.clear()


def test_create_employee_work_schedule_does_not_accept_client_tenant_id() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["tenant_id"] = "ATTACKER_TENANT"

        response = client.post(
            f"/api/v1/attendance/employees/{EMPLOYEE_ID}/work-schedules",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_work_schedule_accepts_effective_until() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["effective_until"] = "2026-12-31"

        response = client.post(
            f"/api/v1/attendance/employees/{EMPLOYEE_ID}/work-schedules",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.effective_until == date(2026, 12, 31)

    finally:
        app.dependency_overrides.clear()


def test_create_employee_work_schedule_defaults_to_active() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("is_active")

        response = client.post(
            f"/api/v1/attendance/employees/{EMPLOYEE_ID}/work-schedules",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.is_active is True

    finally:
        app.dependency_overrides.clear()


def test_create_employee_work_schedule_rejects_invalid_effective_from() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["effective_from"] = "not-a-date"

        response = client.post(
            f"/api/v1/attendance/employees/{EMPLOYEE_ID}/work-schedules",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_work_schedule_rejects_invalid_effective_until() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["effective_until"] = "not-a-date"

        response = client.post(
            f"/api/v1/attendance/employees/{EMPLOYEE_ID}/work-schedules",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_work_schedule_rejects_missing_work_schedule_id() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("work_schedule_id")

        response = client.post(
            f"/api/v1/attendance/employees/{EMPLOYEE_ID}/work-schedules",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_work_schedule_rejects_missing_effective_from() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("effective_from")

        response = client.post(
            f"/api/v1/attendance/employees/{EMPLOYEE_ID}/work-schedules",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()