"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_link_employee_to_user_api.py

Description:
    API tests for linking an employee to an existing QWOS user.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies import get_request_context
from qwos.application.common.dependencies.hr import (
    get_link_employee_to_user_use_case,
)
from qwos.main import app

EMPLOYEE_ID = "01M03ZJQ8XMGC7424THFKH4HVD"
TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
USER_ID = "01KZYTCWRF8S12V28R9NX6JXS5"


def make_link_employee_to_user_payload() -> dict[str, object]:
    return {
        "user_id": USER_ID,
        "first_name": "Richard",
        "middle_name": "Santisas",
        "last_name": "Balabarcon",
        "preferred_name": "Richard S. Balabarcon",
    }


def make_link_employee_to_user_use_case() -> AsyncMock:
    use_case = AsyncMock()

    updated_at = datetime(
        2026,
        8,
        16,
        12,
        0,
        tzinfo=timezone.utc,
    )

    use_case.execute.return_value = type(
        "LinkEmployeeToUserResponse",
        (),
        {
            "employee_id": EMPLOYEE_ID,
            "employee_number": "QW-00001",
            "user_id": USER_ID,
            "profile_id": "01PROFILE000000000000000001",
            "display_name": "Richard Balabarcon",
            "preferred_name": "Richard S. Balabarcon",
            "updated_at": updated_at,
        },
    )()

    return use_case


def install_link_employee_to_user_overrides(
    use_case: AsyncMock,
) -> None:
    request_context = RequestContext(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        correlation_id="test-correlation-id",
        request_id="test-request-id",
        locale="en-US",
        timezone="UTC",
        ip_address=None,
        user_agent=None,
    )

    app.dependency_overrides[
        get_link_employee_to_user_use_case
    ] = lambda: use_case

    app.dependency_overrides[
        get_request_context
    ] = lambda: request_context


def test_link_employee_to_user_returns_created_response() -> None:
    use_case = make_link_employee_to_user_use_case()
    install_link_employee_to_user_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/link-user",
            json=make_link_employee_to_user_payload(),
        )

        assert response.status_code == 200

        assert response.json() == {
            "employee_id": EMPLOYEE_ID,
            "employee_number": "QW-00001",
            "user_id": USER_ID,
            "profile_id": "01PROFILE000000000000000001",
            "display_name": "Richard Balabarcon",
            "preferred_name": "Richard S. Balabarcon",
            "updated_at": "2026-08-16T12:00:00Z",
        }

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.tenant_id == TENANT_ID
        assert command.employee_id == EMPLOYEE_ID
        assert command.user_id == USER_ID
        assert command.first_name == "Richard"
        assert command.middle_name == "Santisas"
        assert command.last_name == "Balabarcon"
        assert command.preferred_name == "Richard S. Balabarcon"

    finally:
        app.dependency_overrides.clear()


def test_link_employee_to_user_uses_employee_id_from_path() -> None:
    use_case = make_link_employee_to_user_use_case()
    install_link_employee_to_user_overrides(use_case)

    path_employee_id = "01OTHEREMPLOYEE00000000000001"

    try:
        client = TestClient(app)

        response = client.post(
            f"/api/v1/hr/employees/{path_employee_id}/link-user",
            json=make_link_employee_to_user_payload(),
        )

        assert response.status_code == 200

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.employee_id == path_employee_id

    finally:
        app.dependency_overrides.clear()


def test_link_employee_to_user_uses_tenant_from_request_context() -> None:
    use_case = make_link_employee_to_user_use_case()
    install_link_employee_to_user_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_link_employee_to_user_payload()
        payload["tenant_id"] = "ATTACKER_TENANT"

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/link-user",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_link_employee_to_user_rejects_employee_id_from_request() -> None:
    use_case = make_link_employee_to_user_use_case()
    install_link_employee_to_user_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_link_employee_to_user_payload()
        payload["employee_id"] = "ATTACKER_EMPLOYEE"

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/link-user",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_link_employee_to_user_rejects_missing_user_id() -> None:
    use_case = make_link_employee_to_user_use_case()
    install_link_employee_to_user_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_link_employee_to_user_payload()
        payload.pop("user_id")

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/link-user",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_link_employee_to_user_rejects_missing_first_name() -> None:
    use_case = make_link_employee_to_user_use_case()
    install_link_employee_to_user_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_link_employee_to_user_payload()
        payload.pop("first_name")

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/link-user",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_link_employee_to_user_rejects_missing_last_name() -> None:
    use_case = make_link_employee_to_user_use_case()
    install_link_employee_to_user_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_link_employee_to_user_payload()
        payload.pop("last_name")

        response = client.post(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/link-user",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()