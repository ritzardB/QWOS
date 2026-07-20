"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

File:
    base_use_case.py

Description:
    Defines the abstract base class for all application use cases.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

RequestType = TypeVar("RequestType")
ResponseType = TypeVar("ResponseType")


class BaseUseCase(
    ABC,
    Generic[RequestType, ResponseType],
):
    """
    Base class for every application use case.

    A use case represents one business capability.
    """

    @abstractmethod
    async def execute(
        self,
        request: RequestType,
    ) -> ResponseType:
        """
        Execute the business use case.
        """
        raise NotImplementedError
