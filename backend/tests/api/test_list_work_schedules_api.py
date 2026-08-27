"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_list_work_schedules_api.py

Description:
    API tests for the List Work Schedules endpoint.

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
    get_list_work_schedules_use_case,
)
from qwos.application.common.dependencies.authentication import (
    get_authenticated_request_context,
)
from qwos.main import app

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
USER_ID = "01KZYTCWRF8S12V28R9NX6JXS5"


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
        "ListWorkSchedulesResponse",
        (),
        {
            "items": [
                type(
                    "WorkScheduleListItem",
                    (),
                    {
                        "id": "01K2TESTSCHEDULE000000001",
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
                )(),
                type(
                    "WorkScheduleListItem",
                    (),
                    {
                        "id": "01K2TESTSCHEDULE000000002",
                        "schedule_code": "Night-shift",
                        "schedule_name": "Night Shift",
                        "timezone": "UTC",
                        "is_active": False,
                        "created_at": datetime(
                            2026,
                            9,
                            2,
                            4,
                            0,
                            tzinfo=timezone.utc,
                        ),
                    },
                )(),
            ],
            "total": 2,
        },
    )()

    return use_case


def install_overrides(
    use_case: AsyncMock,
) -> None:
    request_context = make_request_context()

    app.dependency_overrides[get_list_work_schedules_use_case] = (
        lambda: use_case
    )

    app.dependency_overrides[get_authenticated_request_context] = (
        lambda: request_context
    )


def test_list_work_schedules_returns_created_schedules() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            "/api/v1/attendance/work-schedules",
        )

        assert response.status_code == 200

        assert response.json() == {
            "items": [
                {
                    "id": "01K2TESTSCHEDULE000000001",
                    "schedule_code": "Standard-5-day-work",
                    "schedule_name": "Standard 5-day work",
                    "timezone": "UTC",
                    "is_active": True,
                    "created_at": "2026-09-01T04:00:00Z",
                },
                {
                    "id": "01K2TESTSCHEDULE000000002",
                    "schedule_code": "Night-shift",
                    "schedule_name": "Night Shift",
                    "timezone": "UTC",
                    "is_active": False,
                    "created_at": "2026-09-02T04:00:00Z",
                },
            ],
            "total": 2,
        }

        use_case.execute.assert_awaited_once()

    finally:
        app.dependency_overrides.clear()


def test_list_work_schedules_uses_authenticated_context() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            "/api/v1/attendance/work-schedules",
        )

        assert response.status_code == 200
        use_case.execute.assert_awaited_once()

    finally:
        app.dependency_overrides.clear()


def test_list_work_schedules_supports_empty_result() -> None:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "ListWorkSchedulesResponse",
        (),
        {
            "items": [],
            "total": 0,
        },
    )()

    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            "/api/v1/attendance/work-schedules",
        )

        assert response.status_code == 200

        assert response.json() == {
            "items": [],
            "total": 0,
        }

        use_case.execute.assert_awaited_once()

    finally:
        app.dependency_overrides.clear()


def test_list_work_schedules_exposes_inactive_schedules() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            "/api/v1/attendance/work-schedules",
        )

        assert response.status_code == 200

        schedules = response.json()["items"]

        assert schedules[1]["schedule_code"] == "Night-shift"
        assert schedules[1]["is_active"] is False

    finally:
        app.dependency_overrides.clear()


def test_list_work_schedules_requires_authentication() -> None:
    app.dependency_overrides.clear()

    try:
        client = TestClient(app)

        response = client.get(
            "/api/v1/attendance/work-schedules",
        )

        assert response.status_code == 401

    finally:
        app.dependency_overrides.clear()