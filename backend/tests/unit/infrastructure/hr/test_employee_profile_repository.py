"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_employee_profile_repository.py

Description:
    Unit tests for SQLAlchemyEmployeeProfileRepository.

Author:
    Richard Balabarcon
===============================================================================
"""

from types import SimpleNamespace

from qwos.infrastructure.repositories.hr.sqlalchemy_employee_profile_repository import (
    SQLAlchemyEmployeeProfileRepository,
)


class FakeSession:
    def __init__(self) -> None:
        self.scalar_result = None

    def scalar(self, _statement):
        return self.scalar_result


def make_repository():
    session = FakeSession()

    repository = SQLAlchemyEmployeeProfileRepository(
        session=session,
    )

    return repository, session


def test_get_by_employee_id_returns_matching_profile() -> None:
    repository, session = make_repository()

    expected = SimpleNamespace(
        id="01PROFILE000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
    )

    session.scalar_result = expected

    result = repository.get_by_employee_id(
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
    )

    assert result is expected


def test_get_by_employee_id_returns_none_when_not_found() -> None:
    repository, session = make_repository()

    session.scalar_result = None

    result = repository.get_by_employee_id(
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
    )

    assert result is None


def test_exists_by_employee_id_returns_true_when_profile_exists() -> None:
    repository, session = make_repository()

    session.scalar_result = SimpleNamespace(
        id="01PROFILE000000000000000001",
    )

    result = repository.exists_by_employee_id(
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
    )

    assert result is True


def test_exists_by_employee_id_returns_false_when_profile_not_found() -> None:
    repository, session = make_repository()

    session.scalar_result = None

    result = repository.exists_by_employee_id(
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
    )

    assert result is False