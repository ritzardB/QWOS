"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Application

Command:
    Clock Out

Description:
    Application command for recording an employee clock-out event.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class ClockOutCommand:
    tenant_id: str
    employee_id: str
    clock_out_at: datetime | None = None
    event_source: str = "web"
    notes: str | None = None
