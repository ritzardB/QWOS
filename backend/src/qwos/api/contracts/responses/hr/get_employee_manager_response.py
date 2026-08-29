"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

HR Module

File:
    get_employee_manager_response.py

Description:
    API response contract for retrieving an employee's manager.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class GetEmployeeManagerResponse:
    employee_id: str
    manager_employee_id: str | None
    manager_employee_number: str | None
    relationship_type: str | None
    effective_from: date | None
