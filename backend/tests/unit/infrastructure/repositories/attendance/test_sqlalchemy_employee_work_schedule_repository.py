"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_sqlalchemy_employee_work_schedule_repository.py

Description:
    Unit tests for SQLAlchemyEmployeeWorkScheduleRepository.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date
from types import SimpleNamespace

from qwos.domains.attendance.models.employee_work_schedule import (
    EmployeeWorkSchedule,
)
from qwos.infrastructure.repositories.attendance.sqlalchemy_employee_work_schedule_repository import (
    SQLAlchemyEmployeeWorkScheduleRepository,
)

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
EMPLOYEE_ID = "01KZYEMPLOYEE00000000000001"


class FakeSession:
    """
    Minimal fake SQLAlchemy session for repository unit tests.
    """

    def __init__(self) -> None:
        self.scalar_result: object | None = None
        self.scalars_result: list[object] = []

    def scalar(
        self,
        _statement: object,
    ) -> object | None:
        return self.scalar_result

    def scalars(
        self,
        _statement: object,
    ) -> SimpleNamespace:
        return SimpleNamespace(
            all=lambda: self.scalars_result,
        )


def make_repository() -> tuple[
    SQLAlchemyEmployeeWorkScheduleRepository,
    FakeSession,
]:
    session = FakeSession()

    repository = SQLAlchemyEmployeeWorkScheduleRepository(
        session=session,
    )

    return repository, session


def make_assignment(
    *,
    assignment_id: str,
    tenant_id: str = TENANT_ID,
    employee_id: str = EMPLOYEE_ID,
    work_schedule_id: str = "01SCHEDULE000000000000000001",
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


def test_get_by_id_for_tenant_returns_matching_assignment() -> None:
    repository, session = make_repository()

    expected = SimpleNamespace(
        id="01EWS000000000000000000001",
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        work_schedule_id="01SCHEDULE000000000000000001",
    )

    session.scalar_result = expected

    result = repository.get_by_id_for_tenant(
        tenant_id=TENANT_ID,
        assignment_id=expected.id,
    )

    assert result is expected


def test_get_by_id_for_tenant_returns_none_when_not_found() -> None:
    repository, session = make_repository()

    session.scalar_result = None

    result = repository.get_by_id_for_tenant(
        tenant_id=TENANT_ID,
        assignment_id="01EWS000000000000000000001",
    )

    assert result is None


def test_get_effective_for_employee_returns_assignment() -> None:
    repository, session = make_repository()

    expected = SimpleNamespace(
        id="01EWS000000000000000000001",
        employee_id=EMPLOYEE_ID,
        work_schedule_id="01SCHEDULE000000000000000001",
        effective_from=date(2026, 9, 1),
        effective_until=None,
    )

    session.scalar_result = expected

    result = repository.get_effective_for_employee(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        effective_date=date(2026, 9, 15),
    )

    assert result is expected


def test_get_effective_for_employee_returns_none_when_not_found() -> None:
    repository, session = make_repository()

    session.scalar_result = None

    result = repository.get_effective_for_employee(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        effective_date=date(2026, 9, 15),
    )

    assert result is None


def test_list_by_employee_returns_assignments() -> None:
    repository, session = make_repository()

    expected = [
        SimpleNamespace(
            id="01EWS000000000000000000001",
            effective_from=date(2026, 9, 1),
        ),
        SimpleNamespace(
            id="01EWS000000000000000000002",
            effective_from=date(2026, 1, 1),
        ),
    ]

    session.scalars_result = expected

    result = repository.list_by_employee(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
    )

    assert result == expected


def test_list_by_employee_returns_empty_list_when_none_exist() -> None:
    repository, session = make_repository()

    session.scalars_result = []

    result = repository.list_by_employee(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
    )

    assert result == []


def test_get_active_by_employee_returns_assignment() -> None:
    repository, session = make_repository()

    expected = SimpleNamespace(
        id="01EWS000000000000000000001",
        employee_id=EMPLOYEE_ID,
        is_active=True,
    )

    session.scalar_result = expected

    result = repository.get_active_by_employee(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
    )

    assert result is expected


def test_get_active_by_employee_returns_none_when_not_found() -> None:
    repository, session = make_repository()

    session.scalar_result = None

    result = repository.get_active_by_employee(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
    )

    assert result is None


def test_exists_by_employee_and_start_date_returns_true() -> None:
    repository, session = make_repository()

    session.scalar_result = SimpleNamespace(
        id="01EWS000000000000000000001",
    )

    result = repository.exists_by_employee_and_start_date(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        effective_from=date(2026, 9, 1),
    )

    assert result is True


def test_exists_by_employee_and_start_date_returns_false() -> None:
    repository, session = make_repository()

    session.scalar_result = None

    result = repository.exists_by_employee_and_start_date(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        effective_from=date(2026, 9, 1),
    )

    assert result is False


def test_make_assignment_creates_effective_dated_assignment() -> None:
    assignment = make_assignment(
        assignment_id="01ASSIGNMENT0000000000000001",
        effective_from=date(2026, 9, 1),
        effective_until=date(2026, 9, 30),
    )

    assert assignment.id == "01ASSIGNMENT0000000000000001"
    assert assignment.tenant_id == TENANT_ID
    assert assignment.employee_id == EMPLOYEE_ID
    assert assignment.effective_from == date(2026, 9, 1)
    assert assignment.effective_until == date(2026, 9, 30)
    assert assignment.is_active is True