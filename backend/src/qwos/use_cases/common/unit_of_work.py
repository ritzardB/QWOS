"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

File:
    unit_of_work.py

Description:
    Defines the Unit of Work abstraction.

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
    async def __aenter__(self) -> "UnitOfWork": ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None
    ) -> None: ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
