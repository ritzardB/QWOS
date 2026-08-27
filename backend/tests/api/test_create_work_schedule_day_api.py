"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_create_work_schedule_day_api.py

Description:
    API tests for the Create Work Schedule Day endpoint.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, time, timezone
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies import get_request_context
from qwos.application.common.dependencies.attendance import (
    get_create_work_schedule_day_use_case,
)
from qwos.application.common.dependencies.authentication import (
    get_authenticated_request_context,
)
from qwos.main import app

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
USER_ID = "01KZYTCWRF8S12V28R9NX6JXS5"
SCHEDULE_ID = "01K2TESTSCHEDULE000000001"


def make_payload() -> dict[str, object]:
    return {
        "day_of_week": 1,
        "day_type": "workday",
        "start_time": "09:00:00",
        "end_time": "18:00:00",
        "break_minutes": 60,
        "is_overnight": False,
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
        "CreateWorkScheduleDayResponse",
        (),
        {
            "id": "01K2TESTWSD00000000000001",
            "work_schedule_id": SCHEDULE_ID,
            "day_of_week": 1,
            "day_type": "workday",
            "start_time": time(9, 0),
            "end_time": time(18, 0),
            "break_minutes": 60,
            "is_overnight": False,
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

    app.dependency_overrides[get_create_work_schedule_day_use_case] = (
        lambda: use_case
    )

    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    app.dependency_overrides[get_authenticated_request_context] = (
        lambda: request_context
    )


def test_create_work_schedule_day_returns_created_response() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.post(
            f"/api/v1/attendance/work-schedules/{SCHEDULE_ID}/days",
            json=make_payload(),
        )

        assert response.status_code == 201

        assert response.json() == {
            "id": "01K2TESTWSD00000000000001",
            "work_schedule_id": SCHEDULE_ID,
            "day_of_week": 1,
            "day_type": "workday",
            "start_time": "09:00:00",
            "end_time": "18:00:00",
            "break_minutes": 60,
            "is_overnight": False,
            "created_at": "2026-09-01T04:00:00Z",
        }

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.tenant_id == TENANT_ID
        assert command.work_schedule_id == SCHEDULE_ID
        assert command.day_of_week == 1
        assert command.day_type == "workday"
        assert command.start_time == time(9, 0)
        assert command.end_time == time(18, 0)
        assert command.break_minutes == 60
        assert command.is_overnight is False

    finally:
        app.dependency_overrides.clear()


def test_create_work_schedule_day_does_not_accept_client_tenant_id() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["tenant_id"] = "ATTACKER_TENANT"

        response = client.post(
            f"/api/v1/attendance/work-schedules/{SCHEDULE_ID}/days",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_work_schedule_day_accepts_rest_day() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["day_of_week"] = 6
        payload["day_type"] = "rest_day"
        payload["start_time"] = None
        payload["end_time"] = None
        payload["break_minutes"] = 0

        response = client.post(
            f"/api/v1/attendance/work-schedules/{SCHEDULE_ID}/days",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.day_of_week == 6
        assert command.day_type == "rest_day"
        assert command.start_time is None
        assert command.end_time is None
        assert command.break_minutes == 0

    finally:
        app.dependency_overrides.clear()


def test_create_work_schedule_day_accepts_overnight_workday() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["start_time"] = "22:00:00"
        payload["end_time"] = "06:00:00"
        payload["break_minutes"] = 30
        payload["is_overnight"] = True

        response = client.post(
            f"/api/v1/attendance/work-schedules/{SCHEDULE_ID}/days",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.start_time == time(22, 0)
        assert command.end_time == time(6, 0)
        assert command.break_minutes == 30
        assert command.is_overnight is True

    finally:
        app.dependency_overrides.clear()


def test_create_work_schedule_day_rejects_invalid_day_of_week() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["day_of_week"] = 8

        response = client.post(
            f"/api/v1/attendance/work-schedules/{SCHEDULE_ID}/days",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_work_schedule_day_rejects_negative_break_minutes() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["break_minutes"] = -1

        response = client.post(
            f"/api/v1/attendance/work-schedules/{SCHEDULE_ID}/days",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_work_schedule_day_allows_missing_start_time_at_api_boundary(
) -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["start_time"] = None

        response = client.post(
            f"/api/v1/attendance/work-schedules/{SCHEDULE_ID}/days",
            json=payload,
        )

        assert response.status_code == 201
        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.start_time is None

    finally:
        app.dependency_overrides.clear()


def test_create_work_schedule_day_allows_missing_end_time_at_api_boundary(
) -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["end_time"] = None

        response = client.post(
            f"/api/v1/attendance/work-schedules/{SCHEDULE_ID}/days",
            json=payload,
        )

        assert response.status_code == 201
        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.end_time is None

    finally:
        app.dependency_overrides.clear()