"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    create_work_schedule_day_command.py

Description:
    Command representing the intention to create a work schedule day rule.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import time


@dataclass(frozen=True, slots=True)
class CreateWorkScheduleDayCommand:
    """
    Command for creating a work schedule day rule.
    """

    tenant_id: str
    work_schedule_id: str

    day_of_week: int
    day_type: str = "workday"

    start_time: time | None = None
    end_time: time | None = None

    break_minutes: int = 0
    is_overnight: bool = False
