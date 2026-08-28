"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_attendance_time_segment.py

Description:
    Unit tests for AttendanceTimeSegment.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from qwos.domains.attendance.models import AttendanceTimeSegment


def make_datetime(
    *,
    hour: int,
    minute: int = 0,
) -> datetime:
    return datetime(
        2026,
        9,
        15,
        hour,
        minute,
        tzinfo=timezone.utc,
    )


def test_segment_returns_duration_minutes() -> None:
    segment = AttendanceTimeSegment(
        start_at=make_datetime(hour=9),
        end_at=make_datetime(hour=18),
    )

    assert segment.duration_minutes == 540


def test_segment_returns_duration_with_minutes() -> None:
    segment = AttendanceTimeSegment(
        start_at=make_datetime(hour=9, minute=15),
        end_at=make_datetime(hour=17, minute=45),
    )

    assert segment.duration_minutes == 510


def test_segment_accepts_overnight_classification() -> None:
    segment = AttendanceTimeSegment(
        start_at=make_datetime(hour=22),
        end_at=datetime(
            2026,
            9,
            16,
            6,
            0,
            tzinfo=timezone.utc,
        ),
        is_overnight=True,
    )

    assert segment.is_overnight is True
    assert segment.duration_minutes == 480


def test_segment_accepts_holiday_classification() -> None:
    segment = AttendanceTimeSegment(
        start_at=make_datetime(hour=9),
        end_at=make_datetime(hour=18),
        is_holiday=True,
    )

    assert segment.is_holiday is True
    assert segment.has_premium_classification is True


def test_segment_accepts_rest_day_classification() -> None:
    segment = AttendanceTimeSegment(
        start_at=make_datetime(hour=9),
        end_at=make_datetime(hour=18),
        is_rest_day=True,
    )

    assert segment.is_rest_day is True
    assert segment.has_premium_classification is True


def test_segment_accepts_night_differential_classification() -> None:
    segment = AttendanceTimeSegment(
        start_at=make_datetime(hour=22),
        end_at=datetime(
            2026,
            9,
            16,
            2,
            0,
            tzinfo=timezone.utc,
        ),
        is_overnight=True,
        is_night_differential=True,
    )

    assert segment.is_night_differential is True
    assert segment.has_premium_classification is True
    assert segment.duration_minutes == 240


def test_segment_accepts_overtime_classification() -> None:
    segment = AttendanceTimeSegment(
        start_at=make_datetime(hour=18),
        end_at=make_datetime(hour=20),
        is_overtime=True,
    )

    assert segment.is_overtime is True
    assert segment.has_premium_classification is True
    assert segment.duration_minutes == 120


def test_segment_allows_combined_classifications() -> None:
    segment = AttendanceTimeSegment(
        start_at=make_datetime(hour=22),
        end_at=datetime(
            2026,
            9,
            16,
            2,
            0,
            tzinfo=timezone.utc,
        ),
        is_overnight=True,
        is_holiday=True,
        is_rest_day=True,
        is_night_differential=True,
        is_overtime=True,
    )

    assert segment.is_holiday is True
    assert segment.is_rest_day is True
    assert segment.is_night_differential is True
    assert segment.is_overtime is True
    assert segment.has_premium_classification is True
    assert segment.duration_minutes == 240


def test_segment_rejects_equal_start_and_end() -> None:
    start_at = make_datetime(hour=9)

    with pytest.raises(ValueError, match="end_at must be later"):
        AttendanceTimeSegment(
            start_at=start_at,
            end_at=start_at,
        )


def test_segment_rejects_end_before_start() -> None:
    with pytest.raises(ValueError, match="end_at must be later"):
        AttendanceTimeSegment(
            start_at=make_datetime(hour=18),
            end_at=make_datetime(hour=9),
        )