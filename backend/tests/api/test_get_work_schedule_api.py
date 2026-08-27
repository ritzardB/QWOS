"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_get_work_schedule_api.py

Description:
    API tests for the Get Work Schedule endpoint.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies.attendance import (
    get_work_schedule_use_case,
)
from qwos.application.common.dependencies.authentication import (
    get_authenticated_request_context,
)
from qwos.main import app

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
USER_ID = "01KZYTCWRF8S12V28R9NX6JXS5"
SCHEDULE_ID = "01K2TESTSCHEDULE000000001"


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
        "GetWorkScheduleResponse",
        (),
        {
            "id": SCHEDULE_ID,
            "schedule_code": "Standard-5-day-work",
            "schedule_name": "Standard 5-day work",
            "timezone": "UTC",
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

    app.dependency_overrides[get_work_schedule_use_case] = (
        lambda: use_case
    )

    app.dependency_overrides[get_authenticated_request_context] = (
        lambda: request_context
    )


def test_get_work_schedule_returns_schedule() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            f"/api/v1/attendance/work-schedules/{SCHEDULE_ID}",
        )

        assert response.status_code == 200

        assert response.json() == {
            "id": SCHEDULE_ID,
            "schedule_code": "Standard-5-day-work",
            "schedule_name": "Standard 5-day work",
            "timezone": "UTC",
            "is_active": True,
            "created_at": "2026-09-01T04:00:00Z",
        }

        use_case.execute.assert_awaited_once_with(
            SCHEDULE_ID,
        )

    finally:
        app.dependency_overrides.clear()


def test_get_work_schedule_passes_requested_schedule_id() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    requested_schedule_id = "01DIFFERENTSCHEDULE000000001"

    try:
        client = TestClient(app)

        response = client.get(
            f"/api/v1/attendance/work-schedules/{requested_schedule_id}",
        )

        assert response.status_code == 200

        use_case.execute.assert_awaited_once_with(
            requested_schedule_id,
        )

    finally:
        app.dependency_overrides.clear()


def test_get_work_schedule_returns_inactive_schedule() -> None:
    use_case = make_use_case()

    use_case.execute.return_value = type(
        "GetWorkScheduleResponse",
        (),
        {
            "id": SCHEDULE_ID,
            "schedule_code": "Archived-5-day-work",
            "schedule_name": "Archived 5-day work",
            "timezone": "UTC",
            "is_active": False,
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

    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            f"/api/v1/attendance/work-schedules/{SCHEDULE_ID}",
        )

        assert response.status_code == 200
        assert response.json()["is_active"] is False

    finally:
        app.dependency_overrides.clear()


def test_get_work_schedule_preserves_timezone() -> None:
    use_case = make_use_case()

    use_case.execute.return_value = type(
        "GetWorkScheduleResponse",
        (),
        {
            "id": SCHEDULE_ID,
            "schedule_code": "Standard-5-day-work",
            "schedule_name": "Standard 5-day work",
            "timezone": "Europe/London",
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

    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            f"/api/v1/attendance/work-schedules/{SCHEDULE_ID}",
        )

        assert response.status_code == 200
        assert response.json()["timezone"] == "Europe/London"

    finally:
        app.dependency_overrides.clear()


def test_get_work_schedule_requires_authentication() -> None:
    app.dependency_overrides.clear()

    try:
        client = TestClient(app)

        response = client.get(
            f"/api/v1/attendance/work-schedules/{SCHEDULE_ID}",
        )

        assert response.status_code == 401

    finally:
        app.dependency_overrides.clear()