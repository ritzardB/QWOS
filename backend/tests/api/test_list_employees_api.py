"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_list_employees_api.py

Description:
    API tests for the List Employees endpoint.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.dependencies.hr import (
    get_list_employees_use_case,
)
from qwos.main import app

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"


def make_list_employees_use_case() -> AsyncMock:
    use_case = AsyncMock()

    created_at_1 = datetime(
        2026,
        8,
        16,
        4,
        29,
        37,
        946774,
        tzinfo=timezone.utc,
    )

    created_at_2 = datetime(
        2026,
        8,
        16,
        5,
        0,
        21,
        749104,
        tzinfo=timezone.utc,
    )

    use_case.execute.return_value = type(
        "ListEmployeesResponse",
        (),
        {
            "employees": [
                type(
                    "EmployeeSummaryResponse",
                    (),
                    {
                        "id": "01M03ZJQ8XMGC7424THFKH4HVD",
                        "employee_number": "QW-00001",
                        "user_id": (
                            "01KZYTCWRF8S12V28R9NX6JXS5"
                        ),
                        "hire_date": date(2026, 8, 16),
                        "employment_status": "active",
                        "employment_type": "full_time",
                        "work_email": "richard@qwos.dev",
                        "work_phone": "+971 50 123 4567",
                        "created_at": created_at_1,
                    },
                )(),
                type(
                    "EmployeeSummaryResponse",
                    (),
                    {
                        "id": "01M041AZVQKK21B7RHTZ09HJXA",
                        "employee_number": "QW-00002",
                        "user_id": (
                            "01M057PDBEVKH1TG4HE6ACMAQF"
                        ),
                        "hire_date": date(2026, 8, 16),
                        "employment_status": "active",
                        "employment_type": "full_time",
                        "work_email": "aevan@qwos.dev",
                        "work_phone": None,
                        "created_at": created_at_2,
                    },
                )(),
            ]
        },
    )()

    return use_case


def install_list_employees_overrides(
    use_case: AsyncMock,
) -> None:
    app.dependency_overrides[
        get_list_employees_use_case
    ] = lambda: use_case


def test_list_employees_returns_employee_collection() -> None:
    use_case = make_list_employees_use_case()
    install_list_employees_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            "/api/v1/hr/employees",
        )

        assert response.status_code == 200

        assert response.json() == {
            "employees": [
                {
                    "id": "01M03ZJQ8XMGC7424THFKH4HVD",
                    "employee_number": "QW-00001",
                    "user_id": "01KZYTCWRF8S12V28R9NX6JXS5",
                    "hire_date": "2026-08-16",
                    "employment_status": "active",
                    "employment_type": "full_time",
                    "work_email": "richard@qwos.dev",
                    "work_phone": "+971 50 123 4567",
                    "created_at": (
                        "2026-08-16T04:29:37.946774Z"
                    ),
                },
                {
                    "id": "01M041AZVQKK21B7RHTZ09HJXA",
                    "employee_number": "QW-00002",
                    "user_id": "01M057PDBEVKH1TG4HE6ACMAQF",
                    "hire_date": "2026-08-16",
                    "employment_status": "active",
                    "employment_type": "full_time",
                    "work_email": "aevan@qwos.dev",
                    "work_phone": None,
                    "created_at": (
                        "2026-08-16T05:00:21.749104Z"
                    ),
                },
            ]
        }

        use_case.execute.assert_awaited_once_with()

    finally:
        app.dependency_overrides.clear()


def test_list_employees_returns_empty_collection() -> None:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "ListEmployeesResponse",
        (),
        {
            "employees": [],
        },
    )()

    install_list_employees_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            "/api/v1/hr/employees",
        )

        assert response.status_code == 200
        assert response.json() == {
            "employees": [],
        }

        use_case.execute.assert_awaited_once_with()

    finally:
        app.dependency_overrides.clear()