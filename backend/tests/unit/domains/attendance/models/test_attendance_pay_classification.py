"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_attendance_pay_classification.py

Description:
    Unit tests for AttendancePayClassification.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.domains.attendance.models import (
    AttendancePayClassification,
)


def test_default_classification_is_regular() -> None:
    classification = AttendancePayClassification()

    assert classification.is_regular is True
    assert classification.is_night_differential is False
    assert classification.is_holiday is False
    assert classification.is_rest_day is False
    assert classification.is_overtime is False
    assert classification.has_premium is False
    assert classification.is_combined_premium is False


def test_night_differential_is_premium() -> None:
    classification = AttendancePayClassification(
        is_night_differential=True,
    )

    assert classification.is_night_differential is True
    assert classification.has_premium is True
    assert classification.is_combined_premium is False


def test_holiday_is_premium() -> None:
    classification = AttendancePayClassification(
        is_holiday=True,
    )

    assert classification.is_holiday is True
    assert classification.has_premium is True
    assert classification.is_combined_premium is False


def test_rest_day_is_premium() -> None:
    classification = AttendancePayClassification(
        is_rest_day=True,
    )

    assert classification.is_rest_day is True
    assert classification.has_premium is True
    assert classification.is_combined_premium is False


def test_overtime_is_premium() -> None:
    classification = AttendancePayClassification(
        is_overtime=True,
    )

    assert classification.is_overtime is True
    assert classification.has_premium is True
    assert classification.is_combined_premium is False


def test_holiday_and_night_differential_is_combined_premium() -> None:
    classification = AttendancePayClassification(
        is_holiday=True,
        is_night_differential=True,
    )

    assert classification.has_premium is True
    assert classification.is_combined_premium is True


def test_rest_day_and_holiday_is_combined_premium() -> None:
    classification = AttendancePayClassification(
        is_rest_day=True,
        is_holiday=True,
    )

    assert classification.has_premium is True
    assert classification.is_combined_premium is True


def test_overtime_and_night_differential_is_combined_premium() -> None:
    classification = AttendancePayClassification(
        is_overtime=True,
        is_night_differential=True,
    )

    assert classification.has_premium is True
    assert classification.is_combined_premium is True


def test_all_premium_classifications_can_apply_together() -> None:
    classification = AttendancePayClassification(
        is_night_differential=True,
        is_holiday=True,
        is_rest_day=True,
        is_overtime=True,
    )

    assert classification.has_premium is True
    assert classification.is_combined_premium is True


def test_classification_is_immutable() -> None:
    classification = AttendancePayClassification()

    try:
        classification.is_holiday = True
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "AttendancePayClassification must be immutable.",
        )