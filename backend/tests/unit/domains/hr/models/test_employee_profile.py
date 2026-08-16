"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_employee_profile.py

Description:
    Unit tests for EmployeeProfile domain model.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date

from qwos.domains.hr.models.employee_profile import EmployeeProfile


def test_employee_profile_create_normalizes_values() -> None:
    profile = EmployeeProfile.create(
        id="01PROFILE000000000000000001",
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
        date_of_birth=date(1971, 1, 15),
        gender=" MALE ",
        nationality=" philippine ",
        marital_status=" married ",
        personal_email=" Richard.Personal@Example.com ",
        personal_phone=" +971 50 123 4567 ",
        address_line_1=" 123 Main Street ",
        address_line_2=" Apt 10 ",
        city=" Abu Dhabi ",
        state_province=" Abu Dhabi ",
        postal_code=" 00000 ",
        country_code=" ae ",
        emergency_contact_name=" Maria Balabarcon ",
        emergency_contact_relationship=" Spouse ",
        emergency_contact_phone=" +971 50 987 6543 ",
    )

    assert profile.employee_id == "01EMPLOYEE00000000000000001"
    assert profile.gender == "male"
    assert profile.nationality == "philippine"
    assert profile.marital_status == "married"
    assert profile.personal_email == "richard.personal@example.com"
    assert profile.personal_phone == "+971 50 123 4567"
    assert profile.address_line_1 == "123 Main Street"
    assert profile.address_line_2 == "Apt 10"
    assert profile.city == "Abu Dhabi"
    assert profile.state_province == "Abu Dhabi"
    assert profile.postal_code == "00000"
    assert profile.country_code == "AE"
    assert profile.emergency_contact_name == "Maria Balabarcon"
    assert profile.emergency_contact_relationship == "spouse"
    assert profile.emergency_contact_phone == "+971 50 987 6543"


def test_employee_profile_create_allows_optional_fields_to_be_none() -> None:
    profile = EmployeeProfile.create(
        id="01PROFILE000000000000000001",
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
    )

    assert profile.date_of_birth is None
    assert profile.gender is None
    assert profile.nationality is None
    assert profile.marital_status is None
    assert profile.personal_email is None
    assert profile.personal_phone is None
    assert profile.address_line_1 is None
    assert profile.address_line_2 is None
    assert profile.city is None
    assert profile.state_province is None
    assert profile.postal_code is None
    assert profile.country_code is None
    assert profile.emergency_contact_name is None
    assert profile.emergency_contact_relationship is None
    assert profile.emergency_contact_phone is None