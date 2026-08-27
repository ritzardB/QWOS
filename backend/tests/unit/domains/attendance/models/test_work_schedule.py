"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_work_schedule.py

Description:
    Unit tests for WorkSchedule.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import pytest

from qwos.domains.attendance.models import WorkSchedule


TENANT_ID = "01M0TEN00000000000000000001"


def make_schedule(
    *,
    schedule_id: str = "01M0WS00000000000000000001",
    tenant_id: str = TENANT_ID,
    schedule_code: str = "standard-5-day-work",
    schedule_name: str = "Standard 5-Day Work",
    timezone: str = "UTC",
    is_active: bool = True,
) -> WorkSchedule:
    return WorkSchedule.create(
        id=schedule_id,
        tenant_id=tenant_id,
        schedule_code=schedule_code,
        schedule_name=schedule_name,
        timezone=timezone,
        is_active=is_active,
    )


def test_create_work_schedule() -> None:
    schedule = make_schedule()

    assert schedule.id == "01M0WS00000000000000000001"
    assert schedule.tenant_id == TENANT_ID
    assert schedule.schedule_code == "standard-5-day-work"
    assert schedule.schedule_name == "Standard 5-Day Work"
    assert schedule.timezone == "UTC"
    assert schedule.is_active is True


def test_schedule_code_is_normalized() -> None:
    schedule = make_schedule(
        schedule_code="  STANDARD-5-DAY-WORK  ",
    )

    assert schedule.schedule_code == "standard-5-day-work"


def test_schedule_name_is_trimmed() -> None:
    schedule = make_schedule(
        schedule_name="  Standard 5-Day Work  ",
    )

    assert schedule.schedule_name == "Standard 5-Day Work"


def test_timezone_is_trimmed() -> None:
    schedule = make_schedule(
        timezone="  Asia/Manila  ",
    )

    assert schedule.timezone == "Asia/Manila"


def test_inactive_schedule_can_be_created() -> None:
    schedule = make_schedule(
        is_active=False,
    )

    assert schedule.is_active is False


@pytest.mark.parametrize(
    "schedule_code",
    [
        "",
        "   ",
    ],
)
def test_empty_schedule_code_raises_value_error(
    schedule_code: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="schedule_code is required",
    ):
        make_schedule(
            schedule_code=schedule_code,
        )


@pytest.mark.parametrize(
    "schedule_name",
    [
        "",
        "   ",
    ],
)
def test_empty_schedule_name_raises_value_error(
    schedule_name: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="schedule_name is required",
    ):
        make_schedule(
            schedule_name=schedule_name,
        )


@pytest.mark.parametrize(
    "timezone",
    [
        "",
        "   ",
    ],
)
def test_empty_timezone_raises_value_error(
    timezone: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="timezone is required",
    ):
        make_schedule(
            timezone=timezone,
        )


def test_schedule_is_tenant_scoped() -> None:
    tenant_id = "01M0TEN00000000000000000002"

    schedule = make_schedule(
        tenant_id=tenant_id,
    )

    assert schedule.tenant_id == tenant_id


def test_schedule_supports_different_timezones() -> None:
    schedule = make_schedule(
        timezone="Europe/London",
    )

    assert schedule.timezone == "Europe/London"