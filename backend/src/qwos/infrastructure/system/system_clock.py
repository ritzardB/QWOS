"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

System Clock

Description:
    Concrete implementation of the Clock application port.

Responsibilities:
    - Provide the current UTC date and time.
    - Serve as the application's time source.
    - Keep the application layer independent of datetime APIs.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import UTC, datetime

from qwos.application.common.ports.clock import Clock


class SystemClock(Clock):
    """
    System implementation of Clock.
    """

    def now(self) -> datetime:
        """
        Return the current UTC date and time.
        """
        return datetime.now(UTC)