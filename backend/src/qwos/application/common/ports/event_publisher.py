"""
===============================================================================
Event Publisher Interface
===============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class EventPublisher(ABC):
    """
    Publishes application/domain events.
    """

    @abstractmethod
    async def publish(
        self,
        event: object,
    ) -> None: ...
