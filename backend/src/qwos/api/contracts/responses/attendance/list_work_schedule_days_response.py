"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Attendance Module

File:
    list_work_schedule_days_response.py

Description:
    API response returned when listing work schedule day rules.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, time

from pydantic import BaseModel


class WorkScheduleDayListItem(BaseModel):
    """
    API representation of a work schedule day rule.
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


class ListWorkScheduleDaysResponse(BaseModel):
    """
    API response returned when listing work schedule day rules.
    """

    items: list[WorkScheduleDayListItem]
    total: int