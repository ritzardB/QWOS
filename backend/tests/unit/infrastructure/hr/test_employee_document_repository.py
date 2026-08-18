"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

HR Module

File:
    test_employee_document_repository.py

Description:
    Unit tests for SQLAlchemyEmployeeDocumentRepository.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from unittest.mock import MagicMock

from qwos.infrastructure.repositories.hr.sqlalchemy_employee_document_repository import (
    SQLAlchemyEmployeeDocumentRepository,
)

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
EMPLOYEE_ID = "01M03ZJQ8XMGC7424THFKH4HVD"
IMMIGRATION_ID = "01IMMIGRATION00000000000001"


def make_repository() -> tuple[
    SQLAlchemyEmployeeDocumentRepository,
    MagicMock,
]:
    session = MagicMock()

    repository = SQLAlchemyEmployeeDocumentRepository(
        session=session,
    )

    return repository, session


def test_get_next_version_returns_one_when_no_documents_exist() -> None:
    repository, session = make_repository()

    session.scalar.return_value = 1

    result = repository.get_next_version(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        document_category="residence visa",
        immigration_id=IMMIGRATION_ID,
    )

    assert result == 1
    session.scalar.assert_called_once()


def test_get_next_version_returns_next_value() -> None:
    repository, session = make_repository()

    session.scalar.return_value = 4

    result = repository.get_next_version(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        document_category="residence visa",
        immigration_id=IMMIGRATION_ID,
    )

    assert result == 4


def test_get_next_version_normalizes_document_category() -> None:
    repository, session = make_repository()

    session.scalar.return_value = 2

    result = repository.get_next_version(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        document_category="  Residence Visa  ",
        immigration_id=IMMIGRATION_ID,
    )

    assert result == 2

    statement = session.scalar.call_args.args[0]

    assert "employee_documents" in str(statement)


def test_get_next_version_supports_employee_level_documents() -> None:
    repository, session = make_repository()

    session.scalar.return_value = 3

    result = repository.get_next_version(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        document_category="passport",
        immigration_id=None,
    )

    assert result == 3


def test_get_next_version_defaults_to_one_when_scalar_returns_none() -> None:
    repository, session = make_repository()

    session.scalar.return_value = None

    result = repository.get_next_version(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        document_category="passport",
        immigration_id=None,
    )

    assert result == 1