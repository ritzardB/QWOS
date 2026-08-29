"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Port

File:
    clock.py

Description:
    Contract for obtaining the current UTC time.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Protocol


class Clock(Protocol):
    """
    Time provider.
    """

    def now(self) -> datetime:
        """
        Return the current UTC time.
        """
        ...
