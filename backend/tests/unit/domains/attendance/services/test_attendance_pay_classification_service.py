"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_attendance_pay_classification_service.py

Description:
    Unit tests for AttendancePayClassificationService.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from qwos.domains.attendance.models import (
    AttendancePayClassification,
    AttendanceTimeSegment,
)
from qwos.domains.attendance.services import (
    AttendancePayClassificationService,
)


def make_segment(
    *,
    is_night_differential: bool = False,
    is_holiday: bool = False,
    is_rest_day: bool = False,
    is_overtime: bool = False,
) -> AttendanceTimeSegment:
    start_at = datetime(
        2026,
        9,
        15,
        9,
        0,
        tzinfo=timezone.utc,
    )

    return AttendanceTimeSegment(
        start_at=start_at,
        end_at=start_at + timedelta(hours=1),
        is_night_differential=is_night_differential,
        is_holiday=is_holiday,
        is_rest_day=is_rest_day,
        is_overtime=is_overtime,
    )


def test_classify_regular_segment() -> None:
    service = AttendancePayClassificationService()

    result = service.classify(
        make_segment(),
    )

    assert isinstance(
        result,
        AttendancePayClassification,
    )
    assert result.is_regular is True
    assert result.is_night_differential is False
    assert result.is_holiday is False
    assert result.is_rest_day is False
    assert result.is_overtime is False


def test_classify_night_differential() -> None:
    service = AttendancePayClassificationService()

    result = service.classify(
        make_segment(
            is_night_differential=True,
        ),
    )

    assert result.is_regular is False
    assert result.is_night_differential is True
    assert result.is_holiday is False
    assert result.is_rest_day is False
    assert result.is_overtime is False
    assert result.has_premium is True
    assert result.is_combined_premium is False


def test_classify_holiday() -> None:
    service = AttendancePayClassificationService()

    result = service.classify(
        make_segment(
            is_holiday=True,
        ),
    )

    assert result.is_regular is False
    assert result.is_night_differential is False
    assert result.is_holiday is True
    assert result.is_rest_day is False
    assert result.is_overtime is False
    assert result.has_premium is True
    assert result.is_combined_premium is False


def test_classify_rest_day() -> None:
    service = AttendancePayClassificationService()

    result = service.classify(
        make_segment(
            is_rest_day=True,
        ),
    )

    assert result.is_regular is False
    assert result.is_night_differential is False
    assert result.is_holiday is False
    assert result.is_rest_day is True
    assert result.is_overtime is False
    assert result.has_premium is True
    assert result.is_combined_premium is False


def test_classify_overtime() -> None:
    service = AttendancePayClassificationService()

    result = service.classify(
        make_segment(
            is_overtime=True,
        ),
    )

    assert result.is_regular is False
    assert result.is_night_differential is False
    assert result.is_holiday is False
    assert result.is_rest_day is False
    assert result.is_overtime is True
    assert result.has_premium is True
    assert result.is_combined_premium is False


def test_classify_holiday_with_night_differential() -> None:
    service = AttendancePayClassificationService()

    result = service.classify(
        make_segment(
            is_holiday=True,
            is_night_differential=True,
        ),
    )

    assert result.is_regular is False
    assert result.is_holiday is True
    assert result.is_night_differential is True
    assert result.is_rest_day is False
    assert result.is_overtime is False
    assert result.has_premium is True
    assert result.is_combined_premium is True


def test_classify_holiday_with_rest_day() -> None:
    service = AttendancePayClassificationService()

    result = service.classify(
        make_segment(
            is_holiday=True,
            is_rest_day=True,
        ),
    )

    assert result.is_regular is False
    assert result.is_holiday is True
    assert result.is_rest_day is True
    assert result.is_night_differential is False
    assert result.is_overtime is False
    assert result.has_premium is True
    assert result.is_combined_premium is True


def test_classify_night_differential_with_overtime() -> None:
    service = AttendancePayClassificationService()

    result = service.classify(
        make_segment(
            is_night_differential=True,
            is_overtime=True,
        ),
    )

    assert result.is_regular is False
    assert result.is_night_differential is True
    assert result.is_overtime is True
    assert result.is_holiday is False
    assert result.is_rest_day is False
    assert result.has_premium is True
    assert result.is_combined_premium is True


def test_classify_all_premium_conditions() -> None:
    service = AttendancePayClassificationService()

    result = service.classify(
        make_segment(
            is_night_differential=True,
            is_holiday=True,
            is_rest_day=True,
            is_overtime=True,
        ),
    )

    assert result.is_regular is False
    assert result.is_night_differential is True
    assert result.is_holiday is True
    assert result.is_rest_day is True
    assert result.is_overtime is True
    assert result.has_premium is True
    assert result.is_combined_premium is True


def test_classify_preserves_only_segment_classifications() -> None:
    service = AttendancePayClassificationService()

    segment = make_segment(
        is_holiday=True,
        is_night_differential=True,
    )

    result = service.classify(segment)

    assert result == AttendancePayClassification(
        is_regular=False,
        is_night_differential=True,
        is_holiday=True,
        is_rest_day=False,
        is_overtime=False,
    )