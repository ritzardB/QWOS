"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    link_employee_to_user_response.py

Description:
    Response returned after linking an employee to a QWOS user.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class LinkEmployeeToUserResponse:
    """
    Response returned after linking an employee to a QWOS user.
    """

    employee_id: str
    employee_number: str
    user_id: str
    profile_id: str
    display_name: str
    preferred_name: str | None
    updated_at: datetime