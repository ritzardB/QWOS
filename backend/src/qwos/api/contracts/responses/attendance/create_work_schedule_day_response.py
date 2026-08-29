"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Attendance Module

File:
    create_work_schedule_day_response.py

Description:
    API response returned after creating a work schedule day rule.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, time

from pydantic import BaseModel


class CreateWorkScheduleDayResponse(BaseModel):
    """
    API response returned after creating a work schedule day rule.
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
