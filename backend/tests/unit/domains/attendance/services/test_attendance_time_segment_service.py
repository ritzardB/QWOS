"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_attendance_time_segment_service.py

Description:
    Unit tests for AttendanceTimeSegmentService.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, time, timezone

import pytest

from qwos.domains.attendance.services import (
    AttendanceTimeSegmentService,
)


def make_datetime(
    *,
    day: int = 15,
    hour: int,
    minute: int = 0,
) -> datetime:
    return datetime(
        2026,
        9,
        day,
        hour,
        minute,
        tzinfo=timezone.utc,
    )


def test_segment_returns_single_segment_without_night_window() -> None:
    service = AttendanceTimeSegmentService()

    segments = service.segment(
        start_at=make_datetime(hour=9),
        end_at=make_datetime(hour=18),
    )

    assert len(segments) == 1

    segment = segments[0]

    assert segment.start_at == make_datetime(hour=9)
    assert segment.end_at == make_datetime(hour=18)
    assert segment.duration_minutes == 540
    assert segment.is_night_differential is False


def test_segment_splits_daytime_and_night_time() -> None:
    service = AttendanceTimeSegmentService()

    segments = service.segment(
        start_at=make_datetime(hour=21),
        end_at=datetime(
            2026,
            9,
            16,
            7,
            0,
            tzinfo=timezone.utc,
        ),
        night_start=time(22, 0),
        night_end=time(6, 0),
    )

    assert len(segments) == 3

    assert segments[0].start_at == make_datetime(hour=21)
    assert segments[0].end_at == make_datetime(hour=22)
    assert segments[0].is_night_differential is False

    assert segments[1].start_at == make_datetime(hour=22)
    assert segments[1].end_at == datetime(
        2026,
        9,
        16,
        6,
        0,
        tzinfo=timezone.utc,
    )
    assert segments[1].is_night_differential is True

    assert segments[2].start_at == datetime(
        2026,
        9,
        16,
        6,
        0,
        tzinfo=timezone.utc,
    )
    assert segments[2].end_at == datetime(
        2026,
        9,
        16,
        7,
        0,
        tzinfo=timezone.utc,
    )
    assert segments[2].is_night_differential is False


def test_segment_handles_overnight_night_window() -> None:
    service = AttendanceTimeSegmentService()

    segments = service.segment(
        start_at=make_datetime(hour=22),
        end_at=datetime(
            2026,
            9,
            16,
            6,
            0,
            tzinfo=timezone.utc,
        ),
        night_start=time(22, 0),
        night_end=time(6, 0),
    )

    assert len(segments) == 1

    segment = segments[0]

    assert segment.start_at == make_datetime(hour=22)
    assert segment.end_at == datetime(
        2026,
        9,
        16,
        6,
        0,
        tzinfo=timezone.utc,
    )
    assert segment.duration_minutes == 480
    assert segment.is_overnight is True
    assert segment.is_night_differential is True


def test_segment_exact_night_start_is_included() -> None:
    service = AttendanceTimeSegmentService()

    segments = service.segment(
        start_at=make_datetime(hour=22),
        end_at=datetime(
            2026,
            9,
            16,
            2,
            0,
            tzinfo=timezone.utc,
        ),
        night_start=time(22, 0),
        night_end=time(6, 0),
    )

    assert len(segments) == 1
    assert segments[0].is_night_differential is True


def test_segment_exact_night_end_is_excluded() -> None:
    service = AttendanceTimeSegmentService()

    segments = service.segment(
        start_at=make_datetime(hour=6),
        end_at=make_datetime(hour=7),
        night_start=time(22, 0),
        night_end=time(6, 0),
    )

    assert len(segments) == 1
    assert segments[0].is_night_differential is False


def test_segment_entirely_outside_night_window() -> None:
    service = AttendanceTimeSegmentService()

    segments = service.segment(
        start_at=make_datetime(hour=10),
        end_at=make_datetime(hour=18),
        night_start=time(22, 0),
        night_end=time(6, 0),
    )

    assert len(segments) == 1
    assert segments[0].duration_minutes == 480
    assert segments[0].is_night_differential is False


def test_segment_entirely_inside_night_window() -> None:
    service = AttendanceTimeSegmentService()

    segments = service.segment(
        start_at=make_datetime(hour=23),
        end_at=datetime(
            2026,
            9,
            16,
            2,
            0,
            tzinfo=timezone.utc,
        ),
        night_start=time(22, 0),
        night_end=time(6, 0),
    )

    assert len(segments) == 1
    assert segments[0].duration_minutes == 180
    assert segments[0].is_night_differential is True


def test_segment_applies_holiday_classification() -> None:
    service = AttendanceTimeSegmentService()

    segments = service.segment(
        start_at=make_datetime(hour=9),
        end_at=make_datetime(hour=18),
        is_holiday=True,
    )

    assert len(segments) == 1
    assert segments[0].is_holiday is True
    assert segments[0].has_premium_classification is True


def test_segment_applies_rest_day_classification() -> None:
    service = AttendanceTimeSegmentService()

    segments = service.segment(
        start_at=make_datetime(hour=9),
        end_at=make_datetime(hour=18),
        is_rest_day=True,
    )

    assert len(segments) == 1
    assert segments[0].is_rest_day is True
    assert segments[0].has_premium_classification is True


def test_segment_applies_overtime_classification() -> None:
    service = AttendanceTimeSegmentService()

    segments = service.segment(
        start_at=make_datetime(hour=18),
        end_at=make_datetime(hour=20),
        is_overtime=True,
    )

    assert len(segments) == 1
    assert segments[0].is_overtime is True
    assert segments[0].duration_minutes == 120
    assert segments[0].has_premium_classification is True


def test_segment_rejects_invalid_interval() -> None:
    service = AttendanceTimeSegmentService()

    with pytest.raises(
        ValueError,
        match="end_at must be later than start_at",
    ):
        service.segment(
            start_at=make_datetime(hour=18),
            end_at=make_datetime(hour=9),
        )