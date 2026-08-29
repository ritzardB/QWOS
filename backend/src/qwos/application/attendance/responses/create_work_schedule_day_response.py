"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    create_work_schedule_day_response.py

Description:
    Response returned after creating a work schedule day.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time


@dataclass(frozen=True, slots=True)
class CreateWorkScheduleDayResponse:
    """
    Response returned after creating a work schedule day.
    """

    id: str
    work_schedule_id: str
    day_of_week: int
    day_type: str
    start_time: time | None
    end_time: time | None
    break_minutes: int
    is_overnight: bool
    created_at: datetime
