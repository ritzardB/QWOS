"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_create_employee_profile_api.py

Description:
    API tests for the Create Employee Profile endpoint.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies import get_request_context
from qwos.application.common.dependencies.hr import (
    get_create_employee_profile_use_case,
)
from qwos.main import app

EMPLOYEE_ID = "01M03ZJQ8XMGC7424THFKH4HVD"
TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"


def make_create_employee_profile_payload() -> dict[str, object]:
    return {
        "date_of_birth": "1971-01-15",
        "gender": "male",
        "nationality": "philippine",
        "marital_status": "married",
        "personal_email": "richard.personal@example.com",
        "personal_phone": "+971 50 987 6543",
        "address_line_1": "123 Main Street",
        "address_line_2": "Apartment 10",
        "city": "Abu Dhabi",
        "state_province": "Abu Dhabi",
        "postal_code": "00000",
        "country_code": "AE",
        "emergency_contact_name": "Maria Balabarcon",
        "emergency_contact_relationship": "spouse",
        "emergency_contact_phone": "+971 50 987 6543",
    }


def make_create_employee_profile_use_case() -> AsyncMock:
    use_case = AsyncMock()

    created_at = datetime(
        2026,
        8,
        16,
        11,
        0,
        tzinfo=timezone.utc,
    )

    use_case.execute.return_value = type(
        "CreateEmployeeProfileResponse",
        (),
        {
            "id": "01PROFILE000000000000000001",
            "employee_id": EMPLOYEE_ID,
            "date_of_birth": date(1971, 1, 15),
            "gender": "male",
            "nationality": "philippine",
            "marital_status": "married",
            "personal_email": "richard.personal@example.com",
            "personal_phone": "+971 50 987 6543",
            "address_line_1": "123 Main Street",
            "address_line_2": "Apartment 10",
            "city": "Abu Dhabi",
            "state_province": "Abu Dhabi",
            "postal_code": "00000",
            "country_code": "AE",
            "emergency_contact_name": "Maria Balabarcon",
            "emergency_contact_relationship": "spouse",
            "emergency_contact_phone": "+971 50 987 6543",
            "created_at": created_at,
        },
    )()

    return use_case


def install_create_employee_profile_overrides(
    use_case: AsyncMock,
) -> None:
    request_context = RequestContext(
        tenant_id=TENANT_ID,
        user_id="01KZYTCWRF8S12V28R9NX6JXS5",
        correlation_id="test-correlation-id",
        request_id="test-request-id",
        locale="en-US",
        timezone="UTC",
        ip_address=None,
        user_agent=None,
    )

    app.dependency_overrides[
        get_create_employee_profile_use_case
    ] = lambda: use_case

    app.dependency_overrides[
        get_request_context
    ] = lambda: request_context


def test_create_employee_profile_returns_created_response() -> None:
    use_case = make_create_employee_profile_use_case()
    install_create_employee_profile_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/profile",
            json=make_create_employee_profile_payload(),
        )

        assert response.status_code == 201

        assert response.json() == {
            "id": "01PROFILE000000000000000001",
            "employee_id": EMPLOYEE_ID,
            "date_of_birth": "1971-01-15",
            "gender": "male",
            "nationality": "philippine",
            "marital_status": "married",
            "personal_email": "richard.personal@example.com",
            "personal_phone": "+971 50 987 6543",
            "address_line_1": "123 Main Street",
            "address_line_2": "Apartment 10",
            "city": "Abu Dhabi",
            "state_province": "Abu Dhabi",
            "postal_code": "00000",
            "country_code": "AE",
            "emergency_contact_name": "Maria Balabarcon",
            "emergency_contact_relationship": "spouse",
            "emergency_contact_phone": "+971 50 987 6543",
            "created_at": "2026-08-16T11:00:00Z",
        }

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.tenant_id == TENANT_ID
        assert command.employee_id == EMPLOYEE_ID
        assert command.date_of_birth == date(1971, 1, 15)
        assert command.gender == "male"
        assert command.nationality == "philippine"
        assert command.marital_status == "married"
        assert command.personal_email == "richard.personal@example.com"
        assert command.personal_phone == "+971 50 987 6543"
        assert command.country_code == "AE"

    finally:
        app.dependency_overrides.clear()


def test_create_employee_profile_uses_employee_id_from_path() -> None:
    use_case = make_create_employee_profile_use_case()
    install_create_employee_profile_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/hr/employees/01OTHEREMPLOYEE00000000000001/profile",
            json=make_create_employee_profile_payload(),
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.employee_id == "01OTHEREMPLOYEE00000000000001"

    finally:
        app.dependency_overrides.clear()


def test_create_employee_profile_rejects_tenant_id_from_request() -> None:
    use_case = make_create_employee_profile_use_case()
    install_create_employee_profile_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_create_employee_profile_payload()
        payload["tenant_id"] = "ATTACKER_TENANT"

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/profile",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_profile_rejects_employee_id_from_request() -> None:
    use_case = make_create_employee_profile_use_case()
    install_create_employee_profile_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_create_employee_profile_payload()
        payload["employee_id"] = "ATTACKER_EMPLOYEE"

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/profile",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_profile_rejects_invalid_personal_email() -> None:
    use_case = make_create_employee_profile_use_case()
    install_create_employee_profile_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_create_employee_profile_payload()
        payload["personal_email"] = "not-an-email"

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/profile",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_profile_rejects_invalid_country_code() -> None:
    use_case = make_create_employee_profile_use_case()
    install_create_employee_profile_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_create_employee_profile_payload()
        payload["country_code"] = "UAE"

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/profile",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_profile_allows_minimal_profile() -> None:
    use_case = make_create_employee_profile_use_case()
    install_create_employee_profile_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/profile",
            json={},
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.tenant_id == TENANT_ID
        assert command.employee_id == EMPLOYEE_ID
        assert command.date_of_birth is None
        assert command.personal_email is None

    finally:
        app.dependency_overrides.clear()