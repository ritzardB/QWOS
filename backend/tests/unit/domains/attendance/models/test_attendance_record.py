"""
===============================================================================
Quantum Workforce OS (QWOS)

Test:
    AttendanceRecord domain model

Author:
    Richard Balabarcon
===============================================================================
"""

from datetime import date, datetime, timezone

import pytest

from qwos.domains.attendance.models.attendance_record import (
    AttendanceRecord,
)

TENANT_ID = "01M0TEN00000000000000000001"
EMPLOYEE_ID = "01M0EMP00000000000000000001"
RECORD_ID = "01M0ATR00000000000000000001"
PAY_PERIOD_ID = "01M0PER00000000000000000001"


def test_create_normalizes_status_and_notes() -> None:
    record = AttendanceRecord.create(
        id=RECORD_ID,
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        attendance_date=date(2026, 8, 24),
        status=" PRESENT ",
        notes="  Normal working day  ",
    )

    assert record.status == "present"
    assert record.notes == "Normal working day"


def test_create_defaults_calculated_minutes_to_zero() -> None:
    record = AttendanceRecord.create(
        id=RECORD_ID,
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        attendance_date=date(2026, 8, 24),
    )

    assert record.worked_minutes == 0
    assert record.late_minutes == 0
    assert record.undertime_minutes == 0
    assert record.overtime_minutes == 0


def test_create_allows_pay_period_and_clock_times() -> None:
    clock_in = datetime(
        2026,
        8,
        24,
        8,
        30,
        tzinfo=timezone.utc,
    )

    clock_out = datetime(
        2026,
        8,
        24,
        17,
        30,
        tzinfo=timezone.utc,
    )

    record = AttendanceRecord.create(
        id=RECORD_ID,
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        pay_period_id=PAY_PERIOD_ID,
        attendance_date=date(2026, 8, 24),
        clock_in_at=clock_in,
        clock_out_at=clock_out,
        worked_minutes=480,
        late_minutes=0,
        undertime_minutes=0,
        overtime_minutes=60,
    )

    assert record.pay_period_id == PAY_PERIOD_ID
    assert record.clock_in_at == clock_in
    assert record.clock_out_at == clock_out
    assert record.worked_minutes == 480
    assert record.overtime_minutes == 60


@pytest.mark.parametrize(
    "field_name",
    [
        "worked_minutes",
        "late_minutes",
        "undertime_minutes",
        "overtime_minutes",
    ],
)
def test_create_rejects_negative_minutes(
    field_name: str,
) -> None:
    values = {
        "worked_minutes": 0,
        "late_minutes": 0,
        "undertime_minutes": 0,
        "overtime_minutes": 0,
    }

    values[field_name] = -1

    with pytest.raises(
        ValueError,
        match=f"{field_name} cannot be negative",
    ):
        AttendanceRecord.create(
            id=RECORD_ID,
            tenant_id=TENANT_ID,
            employee_id=EMPLOYEE_ID,
            attendance_date=date(2026, 8, 24),
            **values,
        )


def test_create_rejects_clock_out_before_clock_in() -> None:
    clock_in = datetime(
        2026,
        8,
        24,
        17,
        30,
        tzinfo=timezone.utc,
    )

    clock_out = datetime(
        2026,
        8,
        24,
        8,
        30,
        tzinfo=timezone.utc,
    )

    with pytest.raises(
        ValueError,
        match="clock_out_at cannot be earlier",
    ):
        AttendanceRecord.create(
            id=RECORD_ID,
            tenant_id=TENANT_ID,
            employee_id=EMPLOYEE_ID,
            attendance_date=date(2026, 8, 24),
            clock_in_at=clock_in,
            clock_out_at=clock_out,
        )


def test_create_allows_open_clocking_state() -> None:
    clock_in = datetime(
        2026,
        8,
        24,
        8,
        30,
        tzinfo=timezone.utc,
    )

    record = AttendanceRecord.create(
        id=RECORD_ID,
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        attendance_date=date(2026, 8, 24),
        clock_in_at=clock_in,
        clock_out_at=None,
    )

    assert record.clock_in_at == clock_in
    assert record.clock_out_at is None