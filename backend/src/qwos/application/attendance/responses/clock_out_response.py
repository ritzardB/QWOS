"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Application

Response:
    Clock Out

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True, slots=True)
class ClockOutResponse:
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