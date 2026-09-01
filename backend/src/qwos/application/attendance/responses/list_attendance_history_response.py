"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    list_attendance_history_response.py

Description:
    Application response returned when listing employee attendance history.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class AttendanceHistoryListItem:
    """
    Application representation of an attendance history record.
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


@dataclass(frozen=True)
class ListAttendanceHistoryResponse:
    """
    Application response returned when listing employee attendance history.
    """

    items: list[AttendanceHistoryListItem]
    total: int