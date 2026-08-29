"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_effective_work_schedule_resolution_service.py

Description:
    Unit tests for EffectiveWorkScheduleResolutionService.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date
from types import SimpleNamespace

from qwos.domains.attendance.services import (
    EffectiveWorkScheduleResolutionService,
)

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
EMPLOYEE_ID = "01KZYEMPLOYEE00000000000001"
SCHEDULE_ID = "01K2TESTSCHEDULE000000001"

EFFECTIVE_DATE = date(2026, 9, 15)


class FakeEmployeeWorkScheduleRepository:
    """
    Fake repository used by resolution-service tests.
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


def make_assignment() -> SimpleNamespace:
    return SimpleNamespace(
        id="01KEMPWORKSCHEDULE0000000001",
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        work_schedule_id=SCHEDULE_ID,
        effective_from=date(2026, 9, 1),
        effective_until=None,
        is_active=True,
    )


def make_service(
    *,
    result: object | None = None,
) -> tuple[
    EffectiveWorkScheduleResolutionService,
    FakeEmployeeWorkScheduleRepository,
]:
    repository = FakeEmployeeWorkScheduleRepository()
    repository.result = result

    service = EffectiveWorkScheduleResolutionService(
        employee_work_schedule_repository=repository,
    )

    return service, repository


def test_resolve_returns_effective_assignment() -> None:
    assignment = make_assignment()

    service, repository = make_service(
        result=assignment,
    )

    result = service.resolve(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        effective_date=EFFECTIVE_DATE,
    )

    assert result is assignment


def test_resolve_passes_tenant_id_to_repository() -> None:
    service, repository = make_service(
        result=make_assignment(),
    )

    service.resolve(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        effective_date=EFFECTIVE_DATE,
    )

    assert repository.received_tenant_id == TENANT_ID


def test_resolve_passes_employee_id_to_repository() -> None:
    service, repository = make_service(
        result=make_assignment(),
    )

    service.resolve(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        effective_date=EFFECTIVE_DATE,
    )

    assert repository.received_employee_id == EMPLOYEE_ID


def test_resolve_passes_effective_date_to_repository() -> None:
    service, repository = make_service(
        result=make_assignment(),
    )

    service.resolve(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        effective_date=EFFECTIVE_DATE,
    )

    assert repository.received_effective_date == EFFECTIVE_DATE


def test_resolve_returns_none_when_no_assignment_exists() -> None:
    service, _ = make_service(
        result=None,
    )

    result = service.resolve(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        effective_date=EFFECTIVE_DATE,
    )

    assert result is None

    