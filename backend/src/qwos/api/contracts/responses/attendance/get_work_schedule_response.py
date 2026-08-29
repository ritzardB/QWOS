"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Attendance Module

File:
    get_work_schedule_response.py

Description:
    API response returned when retrieving a work schedule.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class GetWorkScheduleResponse(BaseModel):
    """
    API response returned when retrieving a work schedule.
    """

    id: str
    schedule_code: str
    schedule_name: str
    timezone: str
    is_active: bool
    created_at: datetime
