"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_attendance_schedule_resolution_service.py

Description:
    Unit tests for AttendanceScheduleResolutionService.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, time
from types import SimpleNamespace

from qwos.domains.attendance.services import (
    AttendanceScheduleResolutionService,
)

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
OTHER_TENANT_ID = "01OTHER00000000000000000001"

EMPLOYEE_ID = "01KZYEMPLOYEE00000000000001"
OTHER_EMPLOYEE_ID = "01OTHEREMPLOYEE00000000000001"

SCHEDULE_ID = "01K2TESTSCHEDULE000000001"
OTHER_SCHEDULE_ID = "01K2OTHERSCHEDULE000000001"

ASSIGNMENT_ID = "01K2ASSIGNMENT00000000000001"
DAY_ID = "01K2SCHEDULEDAY000000000001"


class FakeEmployeeWorkScheduleRepository:
    """
    Fake repository for employee work schedule assignments.
    """

    def __init__(self) -> None:
        self.result: object | None = None

        self.received_tenant_id: str | None = None
        self.received_employee_id: str | None = None
        self.received_effective_date: date | None = None

    def get_effective_for_employee(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        effective_date: date,
    ) -> object | None:
        self.received_tenant_id = tenant_id
        self.received_employee_id = employee_id
        self.received_effective_date = effective_date

        return self.result


class FakeWorkScheduleRepository:
    """
    Fake repository for work schedules.
    """

    def __init__(self) -> None:
        self.result: object | None = None

        self.received_tenant_id: str | None = None
        self.received_schedule_id: str | None = None

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        schedule_id: str,
    ) -> object | None:
        self.received_tenant_id = tenant_id
        self.received_schedule_id = schedule_id

        return self.result


class FakeWorkScheduleDayRepository:
    """
    Fake repository for work schedule day rules.
    """

    def __init__(self) -> None:
        self.result: object | None = None

        self.received_tenant_id: str | None = None
        self.received_work_schedule_id: str | None = None
        self.received_day_of_week: int | None = None

    def get_by_schedule_and_day(
        self,
        *,
        tenant_id: str,
        work_schedule_id: str,
        day_of_week: int,
    ) -> object | None:
        self.received_tenant_id = tenant_id
        self.received_work_schedule_id = work_schedule_id
        self.received_day_of_week = day_of_week

        return self.result


def make_assignment(
    *,
    tenant_id: str = TENANT_ID,
    employee_id: str = EMPLOYEE_ID,
    work_schedule_id: str = SCHEDULE_ID,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=ASSIGNMENT_ID,
        tenant_id=tenant_id,
        employee_id=employee_id,
        work_schedule_id=work_schedule_id,
        effective_from=date(2026, 9, 1),
        effective_until=None,
        is_active=True,
    )


def make_schedule() -> SimpleNamespace:
    return SimpleNamespace(
        id=SCHEDULE_ID,
        tenant_id=TENANT_ID,
        schedule_code="Standard-5-day-work",
        schedule_name="Standard 5-day work",
        timezone="UTC",
        is_active=True,
    )


def make_schedule_day(
    *,
    day_of_week: int = 1,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=DAY_ID,
        work_schedule_id=SCHEDULE_ID,
        day_of_week=day_of_week,
        day_type="workday",
        start_time=time(9, 0),
        end_time=time(18, 0),
        break_minutes=60,
        is_overnight=False,
    )


def make_service() -> tuple[
    AttendanceScheduleResolutionService,
    FakeEmployeeWorkScheduleRepository,
    FakeWorkScheduleRepository,
    FakeWorkScheduleDayRepository,
]:
    employee_work_schedule_repository = (
        FakeEmployeeWorkScheduleRepository()
    )
    work_schedule_repository = FakeWorkScheduleRepository()
    work_schedule_day_repository = FakeWorkScheduleDayRepository()

    service = AttendanceScheduleResolutionService(
        employee_work_schedule_repository=(
            employee_work_schedule_repository
        ),
        work_schedule_repository=work_schedule_repository,
        work_schedule_day_repository=work_schedule_day_repository,
    )

    return (
        service,
        employee_work_schedule_repository,
        work_schedule_repository,
        work_schedule_day_repository,
    )


def test_resolve_for_employee_returns_resolution() -> None:
    (
        service,
        employee_repository,
        schedule_repository,
        day_repository,
    ) = make_service()

    assignment = make_assignment()
    schedule = make_schedule()
    schedule_day = make_schedule_day()

    employee_repository.result = assignment
    schedule_repository.result = schedule
    day_repository.result = schedule_day

    result = service.resolve_for_employee(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        attendance_date=date(2026, 9, 7),
    )

    assert result is not None
    assert result.assignment is assignment
    assert result.work_schedule is schedule
    assert result.schedule_day is schedule_day


def test_resolve_for_employee_passes_tenant_to_all_repositories() -> None:
    (
        service,
        employee_repository,
        schedule_repository,
        day_repository,
    ) = make_service()

    employee_repository.result = make_assignment()
    schedule_repository.result = make_schedule()
    day_repository.result = make_schedule_day()

    service.resolve_for_employee(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        attendance_date=date(2026, 9, 7),
    )

    assert employee_repository.received_tenant_id == TENANT_ID
    assert schedule_repository.received_tenant_id == TENANT_ID
    assert day_repository.received_tenant_id == TENANT_ID


def test_resolve_for_employee_passes_employee_to_assignment_repository() -> None:
    (
        service,
        employee_repository,
        schedule_repository,
        day_repository,
    ) = make_service()

    employee_repository.result = make_assignment()
    schedule_repository.result = make_schedule()
    day_repository.result = make_schedule_day()

    service.resolve_for_employee(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        attendance_date=date(2026, 9, 7),
    )

    assert employee_repository.received_employee_id == EMPLOYEE_ID


def test_resolve_for_employee_passes_date_to_assignment_repository() -> None:
    (
        service,
        employee_repository,
        schedule_repository,
        day_repository,
    ) = make_service()

    attendance_date = date(2026, 9, 7)

    employee_repository.result = make_assignment()
    schedule_repository.result = make_schedule()
    day_repository.result = make_schedule_day()

    service.resolve_for_employee(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        attendance_date=attendance_date,
    )

    assert employee_repository.received_effective_date == attendance_date


def test_resolve_for_employee_uses_assignment_schedule_id() -> None:
    (
        service,
        employee_repository,
        schedule_repository,
        day_repository,
    ) = make_service()

    assignment = make_assignment(
        work_schedule_id=OTHER_SCHEDULE_ID,
    )

    employee_repository.result = assignment
    schedule_repository.result = SimpleNamespace(
        id=OTHER_SCHEDULE_ID,
        tenant_id=TENANT_ID,
        schedule_code="Night-shift",
        schedule_name="Night Shift",
        timezone="UTC",
        is_active=True,
    )
    day_repository.result = make_schedule_day()

    result = service.resolve_for_employee(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        attendance_date=date(2026, 9, 7),
    )

    assert result is not None
    assert schedule_repository.received_schedule_id == OTHER_SCHEDULE_ID
    assert day_repository.received_work_schedule_id == OTHER_SCHEDULE_ID


def test_resolve_for_employee_maps_monday_to_day_one() -> None:
    (
        service,
        employee_repository,
        schedule_repository,
        day_repository,
    ) = make_service()

    employee_repository.result = make_assignment()
    schedule_repository.result = make_schedule()
    day_repository.result = make_schedule_day(
        day_of_week=1,
    )

    service.resolve_for_employee(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        attendance_date=date(2026, 9, 7),
    )

    assert day_repository.received_day_of_week == 1


def test_resolve_for_employee_maps_sunday_to_day_seven() -> None:
    (
        service,
        employee_repository,
        schedule_repository,
        day_repository,
    ) = make_service()

    employee_repository.result = make_assignment()
    schedule_repository.result = make_schedule()
    day_repository.result = make_schedule_day(
        day_of_week=7,
    )

    service.resolve_for_employee(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        attendance_date=date(2026, 9, 13),
    )

    assert day_repository.received_day_of_week == 7


def test_resolve_for_employee_returns_none_without_assignment() -> None:
    (
        service,
        employee_repository,
        schedule_repository,
        day_repository,
    ) = make_service()

    employee_repository.result = None

    result = service.resolve_for_employee(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        attendance_date=date(2026, 9, 7),
    )

    assert result is None
    assert schedule_repository.received_schedule_id is None
    assert day_repository.received_work_schedule_id is None


def test_resolve_for_employee_returns_none_without_schedule() -> None:
    (
        service,
        employee_repository,
        schedule_repository,
        day_repository,
    ) = make_service()

    employee_repository.result = make_assignment()
    schedule_repository.result = None

    result = service.resolve_for_employee(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        attendance_date=date(2026, 9, 7),
    )

    assert result is None
    assert day_repository.received_work_schedule_id is None


def test_resolve_for_employee_returns_none_without_schedule_day() -> None:
    (
        service,
        employee_repository,
        schedule_repository,
        day_repository,
    ) = make_service()

    employee_repository.result = make_assignment()
    schedule_repository.result = make_schedule()
    day_repository.result = None

    result = service.resolve_for_employee(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        attendance_date=date(2026, 9, 7),
    )

    assert result is None