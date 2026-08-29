"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

HR Module

File:
    create_employee_response.py

Description:
    Response contract for a created employee.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel


class CreateEmployeeResponse(BaseModel):
    """
    API response returned after creating an employee.
    """

    id: str
    employee_number: str
    user_id: str | None
    hire_date: date | None
    employment_status: str
    employment_type: str
    work_email: str | None
    work_phone: str | None
    created_at: datetime
