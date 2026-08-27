"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Attendance Module

File:
    create_employee_work_schedule_request.py

Description:
    Request contract for creating an employee work schedule assignment.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date

from qwos.api.contracts.requests.common.base_request import BaseRequest


class CreateEmployeeWorkScheduleRequest(BaseRequest):
    """
    Request for creating an employee work schedule assignment.
    """

    work_schedule_id: str

    effective_from: date

    effective_until: date | None = None

    is_active: bool = True