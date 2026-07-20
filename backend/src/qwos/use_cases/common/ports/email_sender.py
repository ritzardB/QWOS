"""
===============================================================================
Email Sender Interface
===============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class EmailSender(ABC):
    """
    Sends email messages.
    """

    @abstractmethod
    async def send(
        self,
        *,
        to: list[str],
        subject: str,
        body: str,
        html: str | None = None,
    ) -> None: ...
