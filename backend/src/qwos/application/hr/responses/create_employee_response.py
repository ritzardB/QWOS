"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    create_employee_response.py

Description:
    Response returned after successfully creating an employee.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True, slots=True)
class CreateEmployeeResponse:
    """
    Response returned after creating an employee.
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