"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    list_work_schedules_response.py

Description:
    Response returned when listing work schedules.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class WorkScheduleListItem:
    """
    Work schedule summary returned in a list.
    """

    id: str
    schedule_code: str
    schedule_name: str
    timezone: str
    is_active: bool
    created_at: datetime


@dataclass(frozen=True, slots=True)
class ListWorkSchedulesResponse:
    """
    Response returned when listing work schedules.
    """

    items: list[WorkScheduleListItem]
    total: int
