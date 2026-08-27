"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_list_work_schedule_days_api.py

Description:
    API tests for the List Work Schedule Days endpoint.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, time, timezone
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies.attendance import (
    get_list_work_schedule_days_use_case,
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

    created_at = datetime(
        2026,
        9,
        1,
        4,
        0,
        tzinfo=timezone.utc,
    )

    use_case.execute.return_value = type(
        "ListWorkScheduleDaysResponse",
        (),
        {
            "items": [
                type(
                    "WorkScheduleDayListItem",
                    (),
                    {
                        "id": "01K2WSDAY000000000000000001",
                        "work_schedule_id": SCHEDULE_ID,
                        "day_of_week": 1,
                        "day_type": "workday",
                        "start_time": time(9, 0),
                        "end_time": time(18, 0),
                        "break_minutes": 60,
                        "is_overnight": False,
                        "created_at": created_at,
                    },
                )(),
                type(
                    "WorkScheduleDayListItem",
                    (),
                    {
                        "id": "01K2WSDAY000000000000000002",
                        "work_schedule_id": SCHEDULE_ID,
                        "day_of_week": 2,
                        "day_type": "workday",
                        "start_time": time(9, 0),
                        "end_time": time(18, 0),
                        "break_minutes": 60,
                        "is_overnight": False,
                        "created_at": created_at,
                    },
                )(),
                type(
                    "WorkScheduleDayListItem",
                    (),
                    {
                        "id": "01K2WSDAY000000000000000006",
                        "work_schedule_id": SCHEDULE_ID,
                        "day_of_week": 6,
                        "day_type": "rest_day",
                        "start_time": None,
                        "end_time": None,
                        "break_minutes": 0,
                        "is_overnight": False,
                        "created_at": created_at,
                    },
                )(),
            ],
            "total": 3,
        },
    )()

    return use_case


def install_overrides(
    use_case: AsyncMock,
) -> None:
    request_context = make_request_context()

    app.dependency_overrides[get_list_work_schedule_days_use_case] = (
        lambda: use_case
    )

    app.dependency_overrides[get_authenticated_request_context] = (
        lambda: request_context
    )


def test_list_work_schedule_days_returns_schedule_days() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            f"/api/v1/attendance/work-schedules/{SCHEDULE_ID}/days",
        )

        assert response.status_code == 200

        assert response.json() == {
            "items": [
                {
                    "id": "01K2WSDAY000000000000000001",
                    "work_schedule_id": SCHEDULE_ID,
                    "day_of_week": 1,
                    "day_type": "workday",
                    "start_time": "09:00:00",
                    "end_time": "18:00:00",
                    "break_minutes": 60,
                    "is_overnight": False,
                    "created_at": "2026-09-01T04:00:00Z",
                },
                {
                    "id": "01K2WSDAY000000000000000002",
                    "work_schedule_id": SCHEDULE_ID,
                    "day_of_week": 2,
                    "day_type": "workday",
                    "start_time": "09:00:00",
                    "end_time": "18:00:00",
                    "break_minutes": 60,
                    "is_overnight": False,
                    "created_at": "2026-09-01T04:00:00Z",
                },
                {
                    "id": "01K2WSDAY000000000000000006",
                    "work_schedule_id": SCHEDULE_ID,
                    "day_of_week": 6,
                    "day_type": "rest_day",
                    "start_time": None,
                    "end_time": None,
                    "break_minutes": 0,
                    "is_overnight": False,
                    "created_at": "2026-09-01T04:00:00Z",
                },
            ],
            "total": 3,
        }

        use_case.execute.assert_awaited_once_with(
            SCHEDULE_ID,
        )

    finally:
        app.dependency_overrides.clear()


def test_list_work_schedule_days_passes_requested_schedule_id() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    requested_schedule_id = "01DIFFERENTSCHEDULE000000001"

    try:
        client = TestClient(app)

        response = client.get(
            f"/api/v1/attendance/work-schedules/{requested_schedule_id}/days",
        )

        assert response.status_code == 200

        use_case.execute.assert_awaited_once_with(
            requested_schedule_id,
        )

    finally:
        app.dependency_overrides.clear()


def test_list_work_schedule_days_supports_empty_result() -> None:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "ListWorkScheduleDaysResponse",
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
            f"/api/v1/attendance/work-schedules/{SCHEDULE_ID}/days",
        )

        assert response.status_code == 200

        assert response.json() == {
            "items": [],
            "total": 0,
        }

        use_case.execute.assert_awaited_once_with(
            SCHEDULE_ID,
        )

    finally:
        app.dependency_overrides.clear()


def test_list_work_schedule_days_returns_rest_day() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            f"/api/v1/attendance/work-schedules/{SCHEDULE_ID}/days",
        )

        assert response.status_code == 200

        rest_day = response.json()["items"][2]

        assert rest_day["day_of_week"] == 6
        assert rest_day["day_type"] == "rest_day"
        assert rest_day["start_time"] is None
        assert rest_day["end_time"] is None
        assert rest_day["break_minutes"] == 0
        assert rest_day["is_overnight"] is False

    finally:
        app.dependency_overrides.clear()


def test_list_work_schedule_days_returns_overnight_day() -> None:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "ListWorkScheduleDaysResponse",
        (),
        {
            "items": [
                type(
                    "WorkScheduleDayListItem",
                    (),
                    {
                        "id": "01K2WSDAY000000000000000001",
                        "work_schedule_id": SCHEDULE_ID,
                        "day_of_week": 1,
                        "day_type": "workday",
                        "start_time": time(22, 0),
                        "end_time": time(6, 0),
                        "break_minutes": 30,
                        "is_overnight": True,
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
            ],
            "total": 1,
        },
    )()

    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            f"/api/v1/attendance/work-schedules/{SCHEDULE_ID}/days",
        )

        assert response.status_code == 200

        item = response.json()["items"][0]

        assert item["day_type"] == "workday"
        assert item["start_time"] == "22:00:00"
        assert item["end_time"] == "06:00:00"
        assert item["break_minutes"] == 30
        assert item["is_overnight"] is True

    finally:
        app.dependency_overrides.clear()


def test_list_work_schedule_days_requires_authentication() -> None:
    app.dependency_overrides.clear()

    try:
        client = TestClient(app)

        response = client.get(
            f"/api/v1/attendance/work-schedules/{SCHEDULE_ID}/days",
        )

        assert response.status_code == 401

    finally:
        app.dependency_overrides.clear()