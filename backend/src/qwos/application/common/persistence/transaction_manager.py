"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

File:
    transaction_manager.py

Description:
    Coordinates transactional execution using the Unit of Work pattern.

Responsibilities:
    - Enter a transactional scope
    - Commit successful transactions
    - Roll back failed transactions

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from contextlib import AbstractContextManager
from types import TracebackType

from .unit_of_work import UnitOfWork


class TransactionManager(AbstractContextManager["TransactionManager"]):
    """
    Manages transactional execution.
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._unit_of_work = unit_of_work

    def __enter__(self) -> "TransactionManager":
        """
        Begin a transactional scope.
        """
        self._unit_of_work.__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool | None:
        """
        Complete the transactional scope.
        """
        self._unit_of_work.__exit__(
            exc_type,
            exc,
            tb,
        )
        return None

    def commit(self) -> None:
        """
        Commit the current transaction.
        """
        self._unit_of_work.commit()

    def rollback(self) -> None:
        """
        Roll back the current transaction.
        """
        self._unit_of_work.rollback()

    def flush(self) -> None:
        """
        Flush pending changes without committing.
        """
        self._unit_of_work.flush()
