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

from qwos.infrastructure.repositories.attendance.sqlalchemy_employee_work_schedule_repository import (
    SQLAlchemyEmployeeWorkScheduleRepository,
)


class FakeSession:
    def __init__(self) -> None:
        self.scalar_result = None
        self.scalars_result: list[object] = []

    def scalar(self, _statement):
        return self.scalar_result

    def scalars(self, _statement):
        return SimpleNamespace(
            all=lambda: self.scalars_result,
        )


def make_repository():
    session = FakeSession()

    repository = SQLAlchemyEmployeeWorkScheduleRepository(
        session=session,
    )

    return repository, session


def test_get_by_id_for_tenant_returns_matching_assignment() -> None:
    repository, session = make_repository()

    expected = SimpleNamespace(
        id="01EWS000000000000000000001",
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
        work_schedule_id="01SCHEDULE00000000000000001",
    )

    session.scalar_result = expected

    result = repository.get_by_id_for_tenant(
        tenant_id="01TENANT00000000000000000001",
        assignment_id="01EWS000000000000000000001",
    )

    assert result is expected


def test_get_by_id_for_tenant_returns_none_when_not_found() -> None:
    repository, session = make_repository()

    session.scalar_result = None

    result = repository.get_by_id_for_tenant(
        tenant_id="01TENANT00000000000000000001",
        assignment_id="01EWS000000000000000000001",
    )

    assert result is None


def test_get_effective_for_employee_returns_assignment() -> None:
    repository, session = make_repository()

    expected = SimpleNamespace(
        id="01EWS000000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
        work_schedule_id="01SCHEDULE00000000000000001",
        effective_from=date(2026, 9, 1),
        effective_until=None,
    )

    session.scalar_result = expected

    result = repository.get_effective_for_employee(
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
        effective_date=date(2026, 9, 15),
    )

    assert result is expected


def test_get_effective_for_employee_returns_none_when_not_found() -> None:
    repository, session = make_repository()

    session.scalar_result = None

    result = repository.get_effective_for_employee(
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
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
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
    )

    assert result == expected


def test_list_by_employee_returns_empty_list_when_none_exist() -> None:
    repository, session = make_repository()

    session.scalars_result = []

    result = repository.list_by_employee(
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
    )

    assert result == []


def test_get_active_by_employee_returns_assignment() -> None:
    repository, session = make_repository()

    expected = SimpleNamespace(
        id="01EWS000000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
        is_active=True,
    )

    session.scalar_result = expected

    result = repository.get_active_by_employee(
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
    )

    assert result is expected


def test_get_active_by_employee_returns_none_when_not_found() -> None:
    repository, session = make_repository()

    session.scalar_result = None

    result = repository.get_active_by_employee(
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
    )

    assert result is None


def test_exists_by_employee_and_start_date_returns_true() -> None:
    repository, session = make_repository()

    session.scalar_result = SimpleNamespace(
        id="01EWS000000000000000000001",
    )

    result = repository.exists_by_employee_and_start_date(
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
        effective_from=date(2026, 9, 1),
    )

    assert result is True


def test_exists_by_employee_and_start_date_returns_false() -> None:
    repository, session = make_repository()

    session.scalar_result = None

    result = repository.exists_by_employee_and_start_date(
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
        effective_from=date(2026, 9, 1),
    )

    assert result is False