"""
===============================================================================
Notification Sender Interface
===============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class NotificationSender(ABC):
    """
    Sends in-app or push notifications.
    """

    @abstractmethod
    async def send(
        self,
        *,
        recipient_id: str,
        title: str,
        message: str,
    ) -> None: ...
