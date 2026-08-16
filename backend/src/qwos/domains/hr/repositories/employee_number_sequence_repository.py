"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

Employee Number Sequence Repository Contract

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from qwos.domains.hr.models.employee_number_sequence import (
    EmployeeNumberSequence,
)


class EmployeeNumberSequenceRepository(Protocol):
    """
    Repository contract for employee-number sequences.
    """

    def get_by_tenant_id_for_update(
        self,
        tenant_id: str,
    ) -> EmployeeNumberSequence | None:
        """
        Retrieve the active employee-number sequence for update.

        The implementation must acquire a database row lock.
        """
        ...

    def save(
        self,
        sequence: EmployeeNumberSequence,
    ) -> None:
        """
        Persist the sequence within the current Unit of Work.
        """
        ...