"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    update_employee_profile_response.py

Description:
    Application response returned after updating an employee profile.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, datetime


class UpdateEmployeeProfileResponse:
    """
    Response returned after updating an employee profile.
    """

    def __init__(
        self,
        *,
        id: str,
        employee_id: str,
        date_of_birth: date | None,
        gender: str | None,
        nationality: str | None,
        marital_status: str | None,
        personal_email: str | None,
        personal_phone: str | None,
        address_line_1: str | None,
        address_line_2: str | None,
        city: str | None,
        state_province: str | None,
        postal_code: str | None,
        country_code: str | None,
        emergency_contact_name: str | None,
        emergency_contact_relationship: str | None,
        emergency_contact_phone: str | None,
        created_at: datetime,
    ) -> None:
        self.id = id
        self.employee_id = employee_id
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.nationality = nationality
        self.marital_status = marital_status
        self.personal_email = personal_email
        self.personal_phone = personal_phone
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.state_province = state_province
        self.postal_code = postal_code
        self.country_code = country_code
        self.emergency_contact_name = emergency_contact_name
        self.emergency_contact_relationship = (
            emergency_contact_relationship
        )
        self.emergency_contact_phone = emergency_contact_phone
        self.created_at = created_at