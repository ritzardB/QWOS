"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    create_employee_profile_command.py

Description:
    Command representing the intention to create an HR employee profile.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class CreateEmployeeProfileCommand:
    """
    Command for creating an employee profile.
    """

    tenant_id: str
    employee_id: str

    date_of_birth: date | None = None
    gender: str | None = None
    nationality: str | None = None
    marital_status: str | None = None

    personal_email: str | None = None
    personal_phone: str | None = None

    address_line_1: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    state_province: str | None = None
    postal_code: str | None = None
    country_code: str | None = None

    emergency_contact_name: str | None = None
    emergency_contact_relationship: str | None = None
    emergency_contact_phone: str | None = None