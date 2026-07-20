"""
===============================================================================
Clock Interface
===============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime


class Clock(ABC):
    """
    Provides the current time.
    """

    @abstractmethod
    def utc_now(self) -> datetime:
        """
        Returns the current UTC datetime.
        """
        ...
