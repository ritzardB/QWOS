"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Attendance Module

File:
    create_employee_work_schedule_response.py

Description:
    API response returned after creating an employee work schedule assignment.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel


class CreateEmployeeWorkScheduleResponse(BaseModel):
    """
    API response returned after creating an employee work schedule assignment.
    """

    id: str
    employee_id: str
    work_schedule_id: str
    effective_from: date
    effective_until: date | None
    is_active: bool
    created_at: datetime