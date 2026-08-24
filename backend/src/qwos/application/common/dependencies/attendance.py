"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Common Dependencies

Attendance Dependencies

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from fastapi import Depends

from qwos.application.attendance.use_cases.clock_in_use_case import (
    ClockInUseCase,
)


def get_clock_in_use_case() -> ClockInUseCase:
    """
    Provide the ClockInUseCase instance.
    """

    raise NotImplementedError(
        "ClockInUseCase dependency has not been configured yet.",
    )