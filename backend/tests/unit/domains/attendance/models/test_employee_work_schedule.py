"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_employee_work_schedule.py

Description:
    Unit tests for EmployeeWorkSchedule.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date

import pytest

from qwos.domains.attendance.models import EmployeeWorkSchedule

TENANT_ID = "01M0TEN00000000000000000001"
EMPLOYEE_ID = "01M0EMP00000000000000000001"
SCHEDULE_ID = "01M0WS00000000000000000001"


def make_assignment(
    *,
    assignment_id: str = "01M0EWS0000000000000000001",
    tenant_id: str = TENANT_ID,
    employee_id: str = EMPLOYEE_ID,
    work_schedule_id: str = SCHEDULE_ID,
    effective_from: date = date(2026, 9, 1),
    effective_until: date | None = None,
    is_active: bool = True,
) -> EmployeeWorkSchedule:
    return EmployeeWorkSchedule.create(
        id=assignment_id,
        tenant_id=tenant_id,
        employee_id=employee_id,
        work_schedule_id=work_schedule_id,
        effective_from=effective_from,
        effective_until=effective_until,
        is_active=is_active,
    )


def test_create_employee_work_schedule() -> None:
    assignment = make_assignment()

    assert assignment.id == "01M0EWS0000000000000000001"
    assert assignment.tenant_id == TENANT_ID
    assert assignment.employee_id == EMPLOYEE_ID
    assert assignment.work_schedule_id == SCHEDULE_ID
    assert assignment.effective_from == date(2026, 9, 1)
    assert assignment.effective_until is None
    assert assignment.is_active is True


def test_effective_until_can_be_defined() -> None:
    assignment = make_assignment(
        effective_until=date(2026, 12, 31),
    )

    assert assignment.effective_until == date(2026, 12, 31)


def test_effective_date_boundary_is_inclusive() -> None:
    assignment = make_assignment(
        effective_from=date(2026, 9, 1),
        effective_until=date(2026, 9, 30),
    )

    assert assignment.effective_from <= date(2026, 9, 1)
    assert assignment.effective_until >= date(2026, 9, 30)


def test_effective_date_range_is_valid() -> None:
    assignment = make_assignment(
        effective_from=date(2026, 9, 1),
        effective_until=date(2026, 9, 30),
    )

    assert assignment.effective_until >= assignment.effective_from


def test_effective_until_equal_to_effective_from_is_valid() -> None:
    effective_date = date(2026, 9, 1)

    assignment = make_assignment(
        effective_from=effective_date,
        effective_until=effective_date,
    )

    assert assignment.effective_from == assignment.effective_until


def test_effective_until_before_effective_from_raises_value_error() -> None:
    with pytest.raises(
        ValueError,
        match="effective_until cannot be earlier than effective_from",
    ):
        make_assignment(
            effective_from=date(2026, 9, 1),
            effective_until=date(2026, 8, 31),
        )


def test_inactive_assignment_can_be_created() -> None:
    assignment = make_assignment(
        is_active=False,
    )

    assert assignment.is_active is False


def test_assignment_is_tenant_scoped() -> None:
    tenant_id = "01M0TEN00000000000000000002"

    assignment = make_assignment(
        tenant_id=tenant_id,
    )

    assert assignment.tenant_id == tenant_id


def test_assignment_targets_employee() -> None:
    employee_id = "01M0EMP00000000000000000002"

    assignment = make_assignment(
        employee_id=employee_id,
    )

    assert assignment.employee_id == employee_id


def test_assignment_targets_work_schedule() -> None:
    schedule_id = "01M0WS00000000000000000002"

    assignment = make_assignment(
        work_schedule_id=schedule_id,
    )

    assert assignment.work_schedule_id == schedule_id