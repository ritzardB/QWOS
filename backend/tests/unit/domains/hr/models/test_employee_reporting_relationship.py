"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_employee_reporting_relationship.py

Description:
    Unit tests for EmployeeReportingRelationship.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date

import pytest

from qwos.domains.hr.models.employee_reporting_relationship import (
    EmployeeReportingRelationship,
)


def test_create_primary_manager_relationship() -> None:
    relationship = EmployeeReportingRelationship.create(
        id="01RELATIONSHIP00000000000001",
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
        manager_employee_id="01EMPLOYEE00000000000000002",
        relationship_type=" PRIMARY_MANAGER ",
        effective_from=date(2026, 8, 16),
    )

    assert relationship.relationship_type == "primary_manager"
    assert relationship.employee_id == "01EMPLOYEE00000000000000001"
    assert relationship.manager_employee_id == (
        "01EMPLOYEE00000000000000002"
    )
    assert relationship.effective_from == date(2026, 8, 16)
    assert relationship.effective_to is None
    assert relationship.is_primary is True


def test_create_rejects_self_management() -> None:
    with pytest.raises(
        ValueError,
        match="An employee cannot report to themselves",
    ):
        EmployeeReportingRelationship.create(
            id="01RELATIONSHIP00000000000001",
            tenant_id="01TENANT00000000000000000001",
            employee_id="01EMPLOYEE00000000000000001",
            manager_employee_id="01EMPLOYEE00000000000000001",
            effective_from=date(2026, 8, 16),
        )


def test_create_allows_historical_end_date() -> None:
    relationship = EmployeeReportingRelationship.create(
        id="01RELATIONSHIP00000000000001",
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
        manager_employee_id="01EMPLOYEE00000000000000002",
        effective_from=date(2026, 8, 16),
        effective_to=date(2027, 8, 15),
    )

    assert relationship.effective_to == date(2027, 8, 15)


def test_create_normalizes_relationship_type() -> None:
    relationship = EmployeeReportingRelationship.create(
        id="01RELATIONSHIP00000000000001",
        tenant_id="01TENANT00000000000000000001",
        employee_id="01EMPLOYEE00000000000000001",
        manager_employee_id="01EMPLOYEE00000000000000002",
        relationship_type=" Matrix_Manager ",
        effective_from=date(2026, 8, 16),
        is_primary=False,
    )

    assert relationship.relationship_type == "matrix_manager"
    assert relationship.is_primary is False