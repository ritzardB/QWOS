"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_employee_number_generator.py

Description:
    Unit tests for the database-backed employee-number generator.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from qwos.infrastructure.repositories.hr.sqlalchemy_employee_number_generator import (
    SQLAlchemyEmployeeNumberGenerator,
)


class FakeEmployeeNumberSequenceRepository:
    """
    In-memory repository used to test the generator without PostgreSQL.
    """

    def __init__(
        self,
        sequence: object | None,
    ) -> None:
        self.sequence = sequence
        self.saved_sequence: object | None = None

    def get_by_tenant_id_for_update(
        self,
        tenant_id: str,
    ) -> object | None:
        if self.sequence is None:
            return None

        if self.sequence.tenant_id != tenant_id:
            return None

        if not self.sequence.is_active:
            return None

        return self.sequence

    def save(
        self,
        sequence: object,
    ) -> None:
        self.saved_sequence = sequence


def make_sequence(
    *,
    tenant_id: str = "01TENANT00000000000000000001",
    prefix: str = "QW",
    separator: str = "-",
    padding_length: int = 5,
    next_number: int = 1,
    is_active: bool = True,
) -> SimpleNamespace:
    return SimpleNamespace(
        id="01SEQUENCE00000000000000001",
        tenant_id=tenant_id,
        prefix=prefix,
        separator=separator,
        padding_length=padding_length,
        next_number=next_number,
        is_active=is_active,
    )


def test_generates_first_employee_number() -> None:
    sequence = make_sequence()

    repository = FakeEmployeeNumberSequenceRepository(sequence)

    generator = SQLAlchemyEmployeeNumberGenerator(
        repository=repository,
    )

    employee_number = generator.generate(
        tenant_id=sequence.tenant_id,
    )

    assert employee_number == "QW-00001"
    assert sequence.next_number == 2
    assert repository.saved_sequence is sequence


def test_generates_next_employee_number() -> None:
    sequence = make_sequence(
        next_number=42,
    )

    repository = FakeEmployeeNumberSequenceRepository(sequence)

    generator = SQLAlchemyEmployeeNumberGenerator(
        repository=repository,
    )

    employee_number = generator.generate(
        tenant_id=sequence.tenant_id,
    )

    assert employee_number == "QW-00042"
    assert sequence.next_number == 43
    assert repository.saved_sequence is sequence


def test_supports_custom_prefix_separator_and_padding() -> None:
    sequence = make_sequence(
        prefix="ABC",
        separator="/",
        padding_length=3,
        next_number=7,
    )

    repository = FakeEmployeeNumberSequenceRepository(sequence)

    generator = SQLAlchemyEmployeeNumberGenerator(
        repository=repository,
    )

    employee_number = generator.generate(
        tenant_id=sequence.tenant_id,
    )

    assert employee_number == "ABC/007"
    assert sequence.next_number == 8


def test_raises_when_tenant_sequence_does_not_exist() -> None:
    repository = FakeEmployeeNumberSequenceRepository(
        sequence=None,
    )

    generator = SQLAlchemyEmployeeNumberGenerator(
        repository=repository,
    )

    with pytest.raises(
        ValueError,
        match="Employee number sequence is not configured for tenant",
    ):
        generator.generate(
            tenant_id="01TENANT00000000000000000001",
        )


def test_raises_when_sequence_is_inactive() -> None:
    sequence = make_sequence(
        is_active=False,
    )

    repository = FakeEmployeeNumberSequenceRepository(sequence)

    generator = SQLAlchemyEmployeeNumberGenerator(
        repository=repository,
    )

    with pytest.raises(
        ValueError,
        match="Employee number sequence is not configured for tenant",
    ):
        generator.generate(
            tenant_id=sequence.tenant_id,
        )