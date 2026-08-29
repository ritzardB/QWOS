"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

HR Module

File:
    link_employee_to_user_response.py

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class LinkEmployeeToUserResponse(BaseModel):
    """
    API response returned after linking an employee to a QWOS user.
    """

    employee_id: str
    employee_number: str
    user_id: str
    profile_id: str
    display_name: str
    preferred_name: str | None
    updated_at: datetime
