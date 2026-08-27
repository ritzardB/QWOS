"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_sqlalchemy_work_schedule_repository.py

Description:
    Unit tests for SQLAlchemyWorkScheduleRepository.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from types import SimpleNamespace

from qwos.infrastructure.repositories.attendance.sqlalchemy_work_schedule_repository import (
    SQLAlchemyWorkScheduleRepository,
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

    repository = SQLAlchemyWorkScheduleRepository(
        session=session,
    )

    return repository, session


def test_get_by_id_for_tenant_returns_matching_schedule() -> None:
    repository, session = make_repository()

    expected = SimpleNamespace(
        id="01SCHEDULE00000000000000001",
        tenant_id="01TENANT00000000000000000001",
        schedule_code="standard-5-day-work",
    )

    session.scalar_result = expected

    result = repository.get_by_id_for_tenant(
        tenant_id="01TENANT00000000000000000001",
        schedule_id="01SCHEDULE00000000000000001",
    )

    assert result is expected


def test_get_by_id_for_tenant_returns_none_when_not_found() -> None:
    repository, session = make_repository()

    session.scalar_result = None

    result = repository.get_by_id_for_tenant(
        tenant_id="01TENANT00000000000000000001",
        schedule_id="01SCHEDULE00000000000000001",
    )

    assert result is None


def test_list_by_tenant_returns_schedules() -> None:
    repository, session = make_repository()

    expected = [
        SimpleNamespace(
            id="01SCHEDULE00000000000000001",
            schedule_code="standard-5-day-work",
        ),
        SimpleNamespace(
            id="01SCHEDULE00000000000000002",
            schedule_code="standard-6-day-work",
        ),
    ]

    session.scalars_result = expected

    result = repository.list_by_tenant(
        tenant_id="01TENANT00000000000000000001",
    )

    assert result == expected


def test_list_by_tenant_returns_empty_list_when_no_schedules() -> None:
    repository, session = make_repository()

    session.scalars_result = []

    result = repository.list_by_tenant(
        tenant_id="01TENANT00000000000000000001",
    )

    assert result == []


def test_get_active_by_code_returns_matching_schedule() -> None:
    repository, session = make_repository()

    expected = SimpleNamespace(
        id="01SCHEDULE00000000000000001",
        tenant_id="01TENANT00000000000000000001",
        schedule_code="standard-5-day-work",
        is_active=True,
    )

    session.scalar_result = expected

    result = repository.get_active_by_code(
        tenant_id="01TENANT00000000000000000001",
        schedule_code="standard-5-day-work",
    )

    assert result is expected


def test_get_active_by_code_normalizes_schedule_code() -> None:
    repository, session = make_repository()

    expected = SimpleNamespace(
        id="01SCHEDULE00000000000000001",
        schedule_code="standard-5-day-work",
    )

    session.scalar_result = expected

    result = repository.get_active_by_code(
        tenant_id="01TENANT00000000000000000001",
        schedule_code="  STANDARD-5-DAY-WORK  ",
    )

    assert result is expected


def test_get_active_by_code_returns_none_when_not_found() -> None:
    repository, session = make_repository()

    session.scalar_result = None

    result = repository.get_active_by_code(
        tenant_id="01TENANT00000000000000000001",
        schedule_code="standard-5-day-work",
    )

    assert result is None


def test_exists_by_code_returns_true_when_schedule_exists() -> None:
    repository, session = make_repository()

    session.scalar_result = SimpleNamespace(
        id="01SCHEDULE00000000000000001",
    )

    result = repository.exists_by_code(
        tenant_id="01TENANT00000000000000000001",
        schedule_code="standard-5-day-work",
    )

    assert result is True


def test_exists_by_code_returns_false_when_schedule_not_found() -> None:
    repository, session = make_repository()

    session.scalar_result = None

    result = repository.exists_by_code(
        tenant_id="01TENANT00000000000000000001",
        schedule_code="standard-5-day-work",
    )

    assert result is False


def test_exists_by_code_normalizes_schedule_code() -> None:
    repository, session = make_repository()

    session.scalar_result = SimpleNamespace(
        id="01SCHEDULE00000000000000001",
    )

    result = repository.exists_by_code(
        tenant_id="01TENANT00000000000000000001",
        schedule_code="  STANDARD-5-DAY-WORK  ",
    )

    assert result is True