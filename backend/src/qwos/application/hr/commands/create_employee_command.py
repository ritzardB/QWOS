"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    create_employee_command.py

Description:
    Command representing the intention to create an employee.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class CreateEmployeeCommand:
    """
    Command for creating an employee record.
    """

    tenant_id: str

    user_id: str | None = None

    hire_date: date | None = None

    employment_status: str = "active"

    employment_type: str = "full_time"

    work_email: str | None = None

    work_phone: str | None = None