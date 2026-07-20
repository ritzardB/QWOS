"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

File:
    transaction_manager.py

Description:
    Coordinates transactional execution for application use cases.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Any

from .unit_of_work import UnitOfWork


# Fixes Line 25: Added ["TransactionManager"] generic type argument
class TransactionManager(AbstractAsyncContextManager["TransactionManager"]):
    """
    Manages transactional execution.
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._unit_of_work = unit_of_work

    # Fixes Line 36: Added explicit return type annotation
    async def __aenter__(self) -> TransactionManager:
        await self._unit_of_work.__aenter__()
        return self

    # Fixes Line 40: Added types for parameters and return annotation
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool | None:
        if exc is None:
            await self._unit_of_work.commit()
        else:
            await self._unit_of_work.rollback()

        await self._unit_of_work.__aexit__(
            exc_type,
            exc,
            tb,
        )
        return None