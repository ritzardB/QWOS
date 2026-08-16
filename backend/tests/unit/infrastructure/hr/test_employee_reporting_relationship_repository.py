"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_employee_reporting_relationship_repository.py

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from types import SimpleNamespace

from qwos.infrastructure.repositories.hr.sqlalchemy_employee_reporting_relationship_repository import (
    SQLAlchemyEmployeeReportingRelationshipRepository,
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

    repository = SQLAlchemyEmployeeReportingRelationshipRepository(
        session=session,
    )

    return repository, session


def test_get_active_primary_manager_returns_relationship() -> None:
    repository, session = make_repository()

    expected = SimpleNamespace(
        id="01RELATIONSHIP00000000000001",
        employee_id="01EMPLOYEE00000000000000001",
        manager_employee_id="01EMPLOYEE00000000000000002",
    )

    session.scalar_result = expected

    result = repository.get_active_primary_manager(
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
    )

    assert result is expected


def test_get_active_primary_manager_returns_none_when_not_found() -> None:
    repository, session = make_repository()

    session.scalar_result = None

    result = repository.get_active_primary_manager(
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
    )

    assert result is None


def test_exists_active_primary_manager_returns_true() -> None:
    repository, session = make_repository()

    session.scalar_result = SimpleNamespace(
        id="01RELATIONSHIP00000000000001",
    )

    result = repository.exists_active_primary_manager(
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
    )

    assert result is True


def test_exists_active_primary_manager_returns_false() -> None:
    repository, session = make_repository()

    session.scalar_result = None

    result = repository.exists_active_primary_manager(
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
    )

    assert result is False


def test_get_active_reports_returns_relationships() -> None:
    repository, session = make_repository()

    expected = [
        SimpleNamespace(
            id="01RELATIONSHIP00000000000001",
            employee_id="01EMPLOYEE00000000000000001",
        ),
        SimpleNamespace(
            id="01RELATIONSHIP00000000000002",
            employee_id="01EMPLOYEE00000000000000003",
        ),
    ]

    session.scalars_result = expected

    result = repository.get_active_reports(
        tenant_id="01TENANT00000000000000000001",
        manager_employee_id="01EMPLOYEE00000000000000002",
    )

    assert result == expected