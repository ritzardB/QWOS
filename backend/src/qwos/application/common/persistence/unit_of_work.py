"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Unit of Work

Coordinates transactional work.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType


class UnitOfWork(ABC):
    """
    Coordinates transactional work.
    """

    @abstractmethod
    def __enter__(self) -> "UnitOfWork":
        ...

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        ...

    @abstractmethod
    def commit(self) -> None:
        """
        Commit the current transaction.
        """
        ...

    @abstractmethod
    def rollback(self) -> None:
        """
        Roll back the current transaction.
        """
        ...

    @abstractmethod
    def flush(self) -> None:
        """
        Flush pending changes without committing.
        """
        ...