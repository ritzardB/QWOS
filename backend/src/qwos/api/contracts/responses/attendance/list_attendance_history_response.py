"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Attendance Module

File:
    list_attendance_history_response.py

Description:
    API response returned when listing employee attendance history.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel


class AttendanceHistoryListItem(BaseModel):
    """
    API representation of an attendance history record.
    """

    attendance_record_id: str
    employee_id: str
    attendance_date: date
    status: str
    clock_in_at: datetime | None
    clock_out_at: datetime | None
    worked_minutes: int
    late_minutes: int
    undertime_minutes: int
    overtime_minutes: int
    notes: str | None


class ListAttendanceHistoryResponse(BaseModel):
    """
    API response returned when listing employee attendance history.
    """

    items: list[AttendanceHistoryListItem]
    total: int