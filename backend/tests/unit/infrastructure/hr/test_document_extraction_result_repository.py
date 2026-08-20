"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

HR Module

File:
    test_document_extraction_result_repository.py

Description:
    Unit tests for SQLAlchemyDocumentExtractionResultRepository.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from unittest.mock import MagicMock

from qwos.infrastructure.repositories.hr.sqlalchemy_document_extraction_result_repository import (
    SQLAlchemyDocumentExtractionResultRepository,
)

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
EMPLOYEE_DOCUMENT_ID = "01M0DOCUMENT000000000000001"
FIELD_ID = "01M0FIELD000000000000000001"
OTHER_FIELD_ID = "01M0FIELD000000000000000002"
RESULT_ID = "01M0RESULT000000000000000001"


def make_repository() -> tuple[
    SQLAlchemyDocumentExtractionResultRepository,
    MagicMock,
]:
    session = MagicMock()

    repository = SQLAlchemyDocumentExtractionResultRepository(
        session=session,
    )

    return repository, session


def test_get_by_id_returns_result() -> None:
    repository, session = make_repository()

    expected_result = MagicMock()
    session.scalar.return_value = expected_result

    result = repository.get_by_id(
        RESULT_ID,
    )

    assert result is expected_result
    session.scalar.assert_called_once()

    statement = session.scalar.call_args.args[0]

    assert "document_extraction_results" in str(
        statement,
    )


def test_get_by_id_returns_none_when_not_found() -> None:
    repository, session = make_repository()

    session.scalar.return_value = None

    result = repository.get_by_id(
        RESULT_ID,
    )

    assert result is None
    session.scalar.assert_called_once()


def test_save_adds_result_to_session() -> None:
    repository, session = make_repository()

    extraction_result = MagicMock()

    repository.save(
        extraction_result,
    )

    session.add.assert_called_once_with(
        extraction_result,
    )


def test_list_by_document_id_returns_results() -> None:
    repository, session = make_repository()

    first = MagicMock()
    second = MagicMock()

    session.scalars.return_value.all.return_value = [
        first,
        second,
    ]

    results = repository.list_by_document_id(
        tenant_id=TENANT_ID,
        employee_document_id=EMPLOYEE_DOCUMENT_ID,
    )

    assert results == [
        first,
        second,
    ]

    session.scalars.assert_called_once()

    statement = session.scalars.call_args.args[0]

    assert "document_extraction_results" in str(
        statement,
    )


def test_list_by_document_id_returns_empty_list() -> None:
    repository, session = make_repository()

    session.scalars.return_value.all.return_value = []

    results = repository.list_by_document_id(
        tenant_id=TENANT_ID,
        employee_document_id=EMPLOYEE_DOCUMENT_ID,
    )

    assert results == []


def test_list_by_document_id_includes_tenant_filter() -> None:
    repository, session = make_repository()

    session.scalars.return_value.all.return_value = []

    repository.list_by_document_id(
        tenant_id=TENANT_ID,
        employee_document_id=EMPLOYEE_DOCUMENT_ID,
    )

    statement = session.scalars.call_args.args[0]

    statement_text = str(statement)

    assert "tenant_id" in statement_text
    assert "employee_document_id" in statement_text


def test_list_by_document_id_includes_deleted_filter() -> None:
    repository, session = make_repository()

    session.scalars.return_value.all.return_value = []

    repository.list_by_document_id(
        tenant_id=TENANT_ID,
        employee_document_id=EMPLOYEE_DOCUMENT_ID,
    )

    statement = session.scalars.call_args.args[0]

    statement_text = str(statement)

    assert "deleted_at" in statement_text


def test_list_by_field_id_returns_results() -> None:
    repository, session = make_repository()

    first = MagicMock()
    second = MagicMock()

    session.scalars.return_value.all.return_value = [
        first,
        second,
    ]

    results = repository.list_by_field_id(
        tenant_id=TENANT_ID,
        document_definition_field_id=FIELD_ID,
    )

    assert results == [
        first,
        second,
    ]

    session.scalars.assert_called_once()

    statement = session.scalars.call_args.args[0]

    assert "document_extraction_results" in str(
        statement,
    )


def test_list_by_field_id_returns_empty_list() -> None:
    repository, session = make_repository()

    session.scalars.return_value.all.return_value = []

    results = repository.list_by_field_id(
        tenant_id=TENANT_ID,
        document_definition_field_id=FIELD_ID,
    )

    assert results == []


def test_list_by_field_id_includes_tenant_filter() -> None:
    repository, session = make_repository()

    session.scalars.return_value.all.return_value = []

    repository.list_by_field_id(
        tenant_id=TENANT_ID,
        document_definition_field_id=FIELD_ID,
    )

    statement = session.scalars.call_args.args[0]

    statement_text = str(statement)

    assert "tenant_id" in statement_text
    assert "document_definition_field_id" in statement_text


def test_list_by_field_id_includes_deleted_filter() -> None:
    repository, session = make_repository()

    session.scalars.return_value.all.return_value = []

    repository.list_by_field_id(
        tenant_id=TENANT_ID,
        document_definition_field_id=FIELD_ID,
    )

    statement = session.scalars.call_args.args[0]

    statement_text = str(statement)

    assert "deleted_at" in statement_text


def test_list_by_document_id_scopes_to_requested_document() -> None:
    repository, session = make_repository()

    session.scalars.return_value.all.return_value = []

    repository.list_by_document_id(
        tenant_id=TENANT_ID,
        employee_document_id=EMPLOYEE_DOCUMENT_ID,
    )

    statement = session.scalars.call_args.args[0]

    statement_text = str(statement)

    assert "employee_document_id" in statement_text

    compiled = statement.compile(
        compile_kwargs={
            "literal_binds": True,
        },
    )

    assert EMPLOYEE_DOCUMENT_ID in str(compiled)