"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

Tests:
    Attendance Calculation Service
===============================================================================
"""

from __future__ import annotations

import pytest

from qwos.domains.attendance.services.attendance_calculation_service import (
    AttendanceCalculationResult,
    AttendanceCalculationService,
)


def test_calculate_returns_attendance_calculation_result() -> None:
    service = AttendanceCalculationService()

    result = service.calculate(
        worked_minutes=480,
    )

    assert isinstance(result, AttendanceCalculationResult)


def test_calculate_returns_worked_minutes() -> None:
    service = AttendanceCalculationService()

    result = service.calculate(
        worked_minutes=480,
    )

    assert result.worked_minutes == 480


def test_calculate_returns_late_minutes() -> None:
    service = AttendanceCalculationService()

    result = service.calculate(
        worked_minutes=450,
        late_minutes=30,
    )

    assert result.late_minutes == 30


def test_calculate_returns_undertime_minutes() -> None:
    service = AttendanceCalculationService()

    result = service.calculate(
        worked_minutes=450,
        undertime_minutes=30,
    )

    assert result.undertime_minutes == 30


def test_calculate_returns_overtime_minutes() -> None:
    service = AttendanceCalculationService()

    result = service.calculate(
        worked_minutes=540,
        overtime_minutes=60,
    )

    assert result.overtime_minutes == 60


def test_calculate_defaults_optional_values_to_zero() -> None:
    service = AttendanceCalculationService()

    result = service.calculate(
        worked_minutes=480,
    )

    assert result.late_minutes == 0
    assert result.undertime_minutes == 0
    assert result.overtime_minutes == 0


def test_calculation_result_rejects_negative_worked_minutes() -> None:
    with pytest.raises(
        ValueError,
        match="worked_minutes cannot be negative",
    ):
        AttendanceCalculationResult(
            worked_minutes=-1,
        )


def test_calculation_result_rejects_negative_late_minutes() -> None:
    with pytest.raises(
        ValueError,
        match="late_minutes cannot be negative",
    ):
        AttendanceCalculationResult(
            late_minutes=-1,
        )


def test_calculation_result_rejects_negative_undertime_minutes() -> None:
    with pytest.raises(
        ValueError,
        match="undertime_minutes cannot be negative",
    ):
        AttendanceCalculationResult(
            undertime_minutes=-1,
        )


def test_calculation_result_rejects_negative_overtime_minutes() -> None:
    with pytest.raises(
        ValueError,
        match="overtime_minutes cannot be negative",
    ):
        AttendanceCalculationResult(
            overtime_minutes=-1,
        )


def test_calculate_preserves_all_attendance_values() -> None:
    service = AttendanceCalculationService()

    result = service.calculate(
        worked_minutes=510,
        late_minutes=15,
        undertime_minutes=10,
        overtime_minutes=45,
    )

    assert result.worked_minutes == 510
    assert result.late_minutes == 15
    assert result.undertime_minutes == 10
    assert result.overtime_minutes == 45