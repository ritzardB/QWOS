"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    get_work_schedule_response.py

Description:
    Response returned when retrieving a work schedule.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class GetWorkScheduleResponse:
    """
    Response returned when retrieving a work schedule.
    """

    id: str
    schedule_code: str
    schedule_name: str
    timezone: str
    is_active: bool
    created_at: datetime