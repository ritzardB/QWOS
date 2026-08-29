"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    get_employee_position_response.py

Description:
    Application response for retrieving an employee's current position.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class GetEmployeePositionResponse:
    """
    Response containing an employee's current organizational position.
    """

    id: str
    employee_id: str
    job_title: str
    organizational_level: str
    effective_from: date
    effective_to: date | None
