"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Attendance Module

File:
    create_employee_work_arrangement_response.py

Description:
    Response returned after creating an employee work arrangement.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True, slots=True)
class CreateEmployeeWorkArrangementResponse:
    """
    Response returned after creating an employee work arrangement.
    """

    id: str
    employee_id: str
    work_arrangement: str
    effective_from: date
    effective_until: date | None
    is_active: bool
    created_at: datetime
