"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Attendance Module

File:
    clock_in_response.py

Description:
    Response contract returned after successfully clocking in an employee.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel


class ClockInResponse(BaseModel):
    """
    API response returned after a successful clock-in.
    """

    attendance_record_id: str
    attendance_event_id: str
    employee_id: str
    attendance_date: date
    clock_in_at: datetime | None
    status: str
    event_type: str
    event_at: datetime
