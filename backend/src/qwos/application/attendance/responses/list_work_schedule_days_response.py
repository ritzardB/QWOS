"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    list_work_schedule_days_response.py

Description:
    Response returned when listing the weekly day rules
    for a work schedule.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time


@dataclass(frozen=True, slots=True)
class WorkScheduleDayListItem:
    """
    Work schedule day summary returned in a list.
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


@dataclass(frozen=True, slots=True)
class ListWorkScheduleDaysResponse:
    """
    Response returned when listing work schedule day rules.
    """

    items: list[WorkScheduleDayListItem]
    total: int
