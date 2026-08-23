"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

HR Domain

File:
    test_employee_immigration.py

Description:
    Unit tests for EmployeeImmigration domain model.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date

import pytest

from qwos.domains.hr.models.employee_immigration import (
    EmployeeImmigration,
)

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
EMPLOYEE_ID = "01M03ZJQ8XMGC7424THFKH4HVD"
USER_ID = "01M03USER000000000000000001"
IMMIGRATION_ID = "01M03IMMIGRATION00000000001"


def make_immigration() -> EmployeeImmigration:
    return EmployeeImmigration.create(
        id=IMMIGRATION_ID,
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        immigration_type="Residence Visa",
        status="Active",
        created_by=USER_ID,
    )


def test_create_normalizes_immigration_fields() -> None:
    immigration = EmployeeImmigration.create(
        id=IMMIGRATION_ID,
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        immigration_type="  Residence Visa  ",
        status="  Active  ",
        document_number="  ABC123  ",
        sponsor_name="  Example Sponsor  ",
        issuing_authority="  Government Authority  ",
        issue_date=date(2024, 1, 1),
        expiry_date=date(2028, 1, 1),
        notes="  Test record  ",
        created_by=USER_ID,
    )

    assert immigration.id == IMMIGRATION_ID
    assert immigration.tenant_id == TENANT_ID
    assert immigration.employee_id == EMPLOYEE_ID

    assert immigration.immigration_type == "residence visa"
    assert immigration.status == "active"
    assert immigration.document_number == "ABC123"
    assert immigration.sponsor_name == "Example Sponsor"
    assert immigration.issuing_authority == (
        "Government Authority"
    )
    assert immigration.issue_date == date(2024, 1, 1)
    assert immigration.expiry_date == date(2028, 1, 1)
    assert immigration.notes == "Test record"
    assert immigration.created_by == USER_ID
    assert immigration.updated_by == USER_ID


def test_create_allows_optional_fields_to_be_none() -> None:
    immigration = make_immigration()

    assert immigration.document_number is None
    assert immigration.sponsor_name is None
    assert immigration.issuing_authority is None
    assert immigration.issue_date is None
    assert immigration.expiry_date is None
    assert immigration.notes is None


def test_update_changes_supported_fields() -> None:
    immigration = make_immigration()

    immigration.update(
        immigration_type="  Work Permit  ",
        status="  Renewed  ",
        document_number="  ABC123  ",
        sponsor_name="  New Sponsor  ",
        issuing_authority="  New Authority  ",
        issue_date=date(2024, 1, 1),
        expiry_date=date(2028, 1, 1),
        notes="  Updated record  ",
        updated_by=USER_ID,
    )

    assert immigration.immigration_type == "work permit"
    assert immigration.status == "renewed"
    assert immigration.document_number == "ABC123"
    assert immigration.sponsor_name == "New Sponsor"
    assert immigration.issuing_authority == (
        "New Authority"
    )
    assert immigration.issue_date == date(2024, 1, 1)
    assert immigration.expiry_date == date(2028, 1, 1)
    assert immigration.notes == "Updated record"
    assert immigration.updated_by == USER_ID


def test_update_allows_partial_updates() -> None:
    immigration = EmployeeImmigration.create(
        id=IMMIGRATION_ID,
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        immigration_type="Residence Visa",
        status="Active",
        document_number="OLD123",
        sponsor_name="Original Sponsor",
        issuing_authority="Original Authority",
        issue_date=date(2024, 1, 1),
        expiry_date=date(2027, 1, 1),
        notes="Original notes",
        created_by=USER_ID,
    )

    immigration.update(
        document_number="NEW123",
        updated_by=USER_ID,
    )

    assert immigration.document_number == "NEW123"

    assert immigration.immigration_type == "residence visa"
    assert immigration.status == "active"
    assert immigration.sponsor_name == "Original Sponsor"
    assert immigration.issuing_authority == (
        "Original Authority"
    )
    assert immigration.issue_date == date(2024, 1, 1)
    assert immigration.expiry_date == date(2027, 1, 1)
    assert immigration.notes == "Original notes"


def test_update_rejects_expiry_before_issue_date() -> None:
    immigration = make_immigration()

    with pytest.raises(
        ValueError,
        match="expiry_date cannot be earlier than issue_date",
    ):
        immigration.update(
            issue_date=date(2028, 1, 1),
            expiry_date=date(2027, 1, 1),
        )


def test_update_allows_expiry_equal_to_issue_date() -> None:
    immigration = make_immigration()

    immigration.update(
        issue_date=date(2028, 1, 1),
        expiry_date=date(2028, 1, 1),
    )

    assert immigration.issue_date == date(2028, 1, 1)
    assert immigration.expiry_date == date(2028, 1, 1)


def test_update_allows_issue_date_without_expiry_date() -> None:
    immigration = make_immigration()

    immigration.update(
        issue_date=date(2024, 1, 1),
    )

    assert immigration.issue_date == date(2024, 1, 1)
    assert immigration.expiry_date is None


def test_update_allows_expiry_date_without_issue_date() -> None:
    immigration = make_immigration()

    immigration.update(
        expiry_date=date(2028, 1, 1),
    )

    assert immigration.issue_date is None
    assert immigration.expiry_date == date(2028, 1, 1)