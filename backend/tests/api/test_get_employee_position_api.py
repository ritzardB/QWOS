from __future__ import annotations

from datetime import date
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies import get_request_context
from qwos.application.common.dependencies.hr import (
    get_get_employee_position_use_case,
)
from qwos.application.hr.responses.get_employee_position_response import (
    GetEmployeePositionResponse,
)
from qwos.main import app

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
EMPLOYEE_ID = "01M03ZJQ8XMGC7424THFKH4HVD"


def make_use_case() -> AsyncMock:
    use_case = AsyncMock()

    use_case.execute.return_value = GetEmployeePositionResponse(
        id="01M08ED3QM623NWN4N0NBQ8VF6",
        employee_id=EMPLOYEE_ID,
        job_title="CEO / Owner & Shareholder",
        organizational_level="executive",
        effective_from=date(2026, 8, 16),
        effective_to=None,
    )

    return use_case


def install_overrides(
    use_case: AsyncMock,
) -> None:
    app.dependency_overrides[
        get_request_context
    ] = lambda: RequestContext(
        tenant_id=TENANT_ID,
        user_id="01KZYTCWRF8S12V28R9NX6JXS5",
        correlation_id="test-correlation-id",
        request_id="test-request-id",
    )

    app.dependency_overrides[
        get_get_employee_position_use_case
    ] = lambda: use_case


def clear_overrides() -> None:
    app.dependency_overrides.clear()


def test_get_employee_position_returns_created_position() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            f"/api/v1/hr/employees/{EMPLOYEE_ID}/position",
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == (
            "01M08ED3QM623NWN4N0NBQ8VF6"
        )
        assert data["employee_id"] == EMPLOYEE_ID
        assert data["job_title"] == (
            "CEO / Owner & Shareholder"
        )
        assert data["organizational_level"] == "executive"
        assert data["effective_from"] == "2026-08-16"
        assert data["effective_to"] is None

        use_case.execute.assert_awaited_once_with(
            tenant_id=TENANT_ID,
            employee_id=EMPLOYEE_ID,
        )
    finally:
        clear_overrides()


def test_get_employee_position_can_return_employee_level() -> None:
    use_case = AsyncMock()

    use_case.execute.return_value = GetEmployeePositionResponse(
        id="01M08ED3QM623NWN4N0NBQ8VF7",
        employee_id="01M041AZVQKK21B7RHTZ09HJXA",
        job_title="Employee",
        organizational_level="employee",
        effective_from=date(2026, 8, 16),
        effective_to=None,
    )

    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.get(
            "/api/v1/hr/employees/"
            "01M041AZVQKK21B7RHTZ09HJXA/position",
        )

        assert response.status_code == 200

        data = response.json()

        assert data["job_title"] == "Employee"
        assert data["organizational_level"] == "employee"
    finally:
        clear_overrides()