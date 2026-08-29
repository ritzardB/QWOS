"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

HR Module

File:
    get_employee_position_response.py

Description:
    API response contract for retrieving an employee's current position.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class GetEmployeePositionResponse(BaseModel):
    """
    Response containing an employee's current position.
    """

    id: str
    employee_id: str
    job_title: str
    organizational_level: str
    effective_from: date
    effective_to: date | None
