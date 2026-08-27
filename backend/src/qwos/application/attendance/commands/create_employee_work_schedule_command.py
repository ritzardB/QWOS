"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    create_employee_work_schedule_command.py

Description:
    Command representing the intention to create an employee work schedule
    assignment.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class CreateEmployeeWorkScheduleCommand:
    """
    Command for creating an employee work schedule assignment.
    """

    tenant_id: str
    employee_id: str
    work_schedule_id: str

    effective_from: date | None = None
    effective_until: date | None = None

    is_active: bool = True