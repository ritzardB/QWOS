"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Attendance Module

File:
    create_employee_work_arrangement_response.py

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel


class CreateEmployeeWorkArrangementResponse(BaseModel):
    """
    API response returned after creating an employee work arrangement.
    """

    id: str
    employee_id: str
    work_arrangement: str
    effective_from: date
    effective_until: date | None
    is_active: bool
    created_at: datetime
