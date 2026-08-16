"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

HR Module

File:
    create_employee_profile_response.py

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel


class CreateEmployeeProfileResponse(BaseModel):
    """
    API response returned after creating an employee profile.
    """

    id: str
    employee_id: str

    date_of_birth: date | None
    gender: str | None
    nationality: str | None
    marital_status: str | None

    personal_email: str | None
    personal_phone: str | None

    address_line_1: str | None
    address_line_2: str | None
    city: str | None
    state_province: str | None
    postal_code: str | None
    country_code: str | None

    emergency_contact_name: str | None
    emergency_contact_relationship: str | None
    emergency_contact_phone: str | None

    created_at: datetime