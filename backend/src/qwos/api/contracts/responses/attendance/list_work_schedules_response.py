"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Attendance Module

File:
    list_work_schedules_response.py

Description:
    API response returned when listing work schedules.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class WorkScheduleListItem(BaseModel):
    """
    API representation of a work schedule summary.
    """

    id: str
    schedule_code: str
    schedule_name: str
    timezone: str
    is_active: bool
    created_at: datetime


class ListWorkSchedulesResponse(BaseModel):
    """
    API response returned when listing work schedules.
    """

    items: list[WorkScheduleListItem]
    total: int