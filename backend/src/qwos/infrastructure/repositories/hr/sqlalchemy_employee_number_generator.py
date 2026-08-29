"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

HR Module

File:
    sqlalchemy_employee_number_generator.py

Description:
    Database-backed tenant employee-number generator.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.ports.employee_number_generator import (
    EmployeeNumberGenerator,
)
from qwos.domains.hr.repositories.employee_number_sequence_repository import (
    EmployeeNumberSequenceRepository,
)


class SQLAlchemyEmployeeNumberGenerator(
    EmployeeNumberGenerator,
):
    """
    Database-backed employee-number generator.

    The sequence repository acquires a row-level PostgreSQL lock so concurrent
    employee creation requests cannot receive the same employee number.
    """

    def __init__(
        self,
        *,
        repository: EmployeeNumberSequenceRepository,
    ) -> None:
        self._repository = repository

    def generate(
        self,
        *,
        tenant_id: str,
    ) -> str:
        """
        Generate and reserve the next employee number.

        The caller must execute this within an active Unit of Work.
        """

        sequence = self._repository.get_by_tenant_id_for_update(
            tenant_id,
        )

        if sequence is None:
            raise ValueError("Employee number sequence is not configured for tenant.")

        current_number = sequence.next_number

        employee_number = f"{sequence.prefix}{sequence.separator}{current_number:0{sequence.padding_length}d}"

        sequence.next_number = current_number + 1

        self._repository.save(sequence)

        return employee_number
