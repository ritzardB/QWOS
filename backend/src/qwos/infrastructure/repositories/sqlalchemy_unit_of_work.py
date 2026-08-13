"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

File:
    sqlalchemy_unit_of_work.py

Description:
    SQLAlchemy implementation of the Unit of Work pattern.

Responsibilities:
    - Coordinate transactional work.
    - Commit successful transactions.
    - Roll back failed transactions.
    - Flush pending changes.
    - Remain independent of business logic.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from types import TracebackType

from sqlalchemy.orm import Session

from qwos.application.common.persistence.unit_of_work import UnitOfWork


class SQLAlchemyUnitOfWork(UnitOfWork):
    """
    SQLAlchemy implementation of UnitOfWork.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def __enter__(self) -> "SQLAlchemyUnitOfWork":
        """
        Begin a transactional scope.
        """
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """
        Complete the transactional scope.
        """
        if exc is None:
            self.commit()
        else:
            self.rollback()

    def commit(self) -> None:
        """
        Commit the current transaction.
        """
        self._session.commit()

    def rollback(self) -> None:
        """
        Roll back the current transaction.
        """
        self._session.rollback()

    def flush(self) -> None:
        """
        Flush pending changes without committing.
        """
        self._session.flush()