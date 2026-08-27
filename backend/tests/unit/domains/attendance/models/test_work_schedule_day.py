"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_work_schedule_day.py

Description:
    Unit tests for WorkScheduleDay.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import time

import pytest

from qwos.domains.attendance.models import (
    ScheduleDayType,
    WorkScheduleDay,
)

TENANT_ID = "01M0TEN00000000000000000001"
SCHEDULE_ID = "01M0WS00000000000000000001"


def make_day(
    *,
    day_id: str = "01M0WSD0000000000000000001",
    tenant_id: str = TENANT_ID,
    work_schedule_id: str = SCHEDULE_ID,
    day_of_week: int = 1,
    day_type: str = "workday",
    start_time: time | None = time(9, 0),
    end_time: time | None = time(18, 0),
    break_minutes: int = 60,
    is_overnight: bool = False,
) -> WorkScheduleDay:
    return WorkScheduleDay.create(
        id=day_id,
        tenant_id=tenant_id,
        work_schedule_id=work_schedule_id,
        day_of_week=day_of_week,
        day_type=day_type,
        start_time=start_time,
        end_time=end_time,
        break_minutes=break_minutes,
        is_overnight=is_overnight,
    )


def test_create_work_schedule_day() -> None:
    day = make_day()

    assert day.id == "01M0WSD0000000000000000001"
    assert day.tenant_id == TENANT_ID
    assert day.work_schedule_id == SCHEDULE_ID
    assert day.day_of_week == 1
    assert day.day_type == "workday"
    assert day.start_time == time(9, 0)
    assert day.end_time == time(18, 0)
    assert day.break_minutes == 60
    assert day.is_overnight is False


@pytest.mark.parametrize(
    "day_of_week",
    range(1, 8),
)
def test_valid_day_of_week(day_of_week: int) -> None:
    day = make_day(
        day_of_week=day_of_week,
    )

    assert day.day_of_week == day_of_week


@pytest.mark.parametrize(
    "day_of_week",
    [0, 8, -1, 99],
)
def test_invalid_day_of_week_raises_value_error(
    day_of_week: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="day_of_week must be between 1 and 7",
    ):
        make_day(
            day_of_week=day_of_week,
        )


def test_day_type_is_normalized() -> None:
    day = make_day(
        day_type=" WORKDAY ",
    )

    assert day.day_type == "workday"


def test_rest_day_can_be_created() -> None:
    day = make_day(
        day_type="rest_day",
        start_time=None,
        end_time=None,
        break_minutes=0,
        is_overnight=False,
    )

    assert day.day_type == ScheduleDayType.REST_DAY.value
    assert day.start_time is None
    assert day.end_time is None
    assert day.break_minutes == 0
    assert day.is_overnight is False


def test_workday_requires_start_time() -> None:
    with pytest.raises(
        ValueError,
        match="workday start_time is required",
    ):
        make_day(
            start_time=None,
        )


def test_workday_requires_end_time() -> None:
    with pytest.raises(
        ValueError,
        match="workday end_time is required",
    ):
        make_day(
            end_time=None,
        )


def test_rest_day_cannot_have_start_time() -> None:
    with pytest.raises(
        ValueError,
        match="rest_day cannot define start_time or end_time",
    ):
        make_day(
            day_type="rest_day",
            start_time=time(9, 0),
            end_time=None,
            break_minutes=0,
        )


def test_rest_day_cannot_have_end_time() -> None:
    with pytest.raises(
        ValueError,
        match="rest_day cannot define start_time or end_time",
    ):
        make_day(
            day_type="rest_day",
            start_time=None,
            end_time=time(18, 0),
            break_minutes=0,
        )


def test_rest_day_break_minutes_must_be_zero() -> None:
    with pytest.raises(
        ValueError,
        match="rest_day break_minutes must be zero",
    ):
        make_day(
            day_type="rest_day",
            start_time=None,
            end_time=None,
            break_minutes=30,
        )


def test_rest_day_cannot_be_overnight() -> None:
    with pytest.raises(
        ValueError,
        match="rest_day cannot be overnight",
    ):
        make_day(
            day_type="rest_day",
            start_time=None,
            end_time=None,
            break_minutes=0,
            is_overnight=True,
        )


def test_negative_break_minutes_raise_value_error() -> None:
    with pytest.raises(
        ValueError,
        match="break_minutes cannot be negative",
    ):
        make_day(
            break_minutes=-1,
        )


def test_invalid_day_type_raises_value_error() -> None:
    with pytest.raises(
        ValueError,
        match="day_type must be one of: workday, rest_day",
    ):
        make_day(
            day_type="holiday",
        )


def test_overnight_workday_is_supported() -> None:
    day = make_day(
        start_time=time(22, 0),
        end_time=time(6, 0),
        break_minutes=30,
        is_overnight=True,
    )

    assert day.start_time == time(22, 0)
    assert day.end_time == time(6, 0)
    assert day.is_overnight is True