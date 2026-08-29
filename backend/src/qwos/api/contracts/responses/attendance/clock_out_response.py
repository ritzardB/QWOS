"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Attendance Module

File:
    clock_out_response.py

Description:
    Response contract returned after successfully clocking out an employee.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel


class ClockOutResponse(BaseModel):
    """
    API response returned after a successful clock-out.
    """

    attendance_record_id: str
    attendance_event_id: str
    employee_id: str
    attendance_date: date
    clock_in_at: datetime | None
    clock_out_at: datetime
    worked_minutes: int
    status: str
    event_type: str
    event_at: datetime
