"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_create_employee_leave_balance_api.py

Description:
    API tests for the Create Employee Leave Balance endpoint.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies import get_request_context
from qwos.application.common.dependencies.authentication import (
    get_authenticated_request_context,
)
from qwos.application.common.dependencies.leave import (
    get_create_employee_leave_balance_use_case,
)
from qwos.main import app

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
USER_ID = "01KZYTCWRF8S12V28R9NX6JXS5"
EMPLOYEE_ID = "01K2TESTEMPLOYEE00000001"
ASSIGNMENT_ID = "01K2TESTLEAVEASSIGNMENT01"


def make_payload() -> dict[str, object]:
    return {
        "employee_leave_assignment_id": ASSIGNMENT_ID,
        "employee_id": EMPLOYEE_ID,
        "period_start": "2026-01-01",
        "period_end": "2026-12-31",
        "entitlement_days": "24.00",
        "carried_forward_days": "2.00",
        "accrued_days": "10.50",
        "used_days": "5.50",
        "adjustment_days": "1.00",
        "is_active": True,
    }


def make_request_context() -> RequestContext:
    return RequestContext(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        correlation_id="test-correlation-id",
        request_id="test-request-id",
        locale="en-US",
        timezone="UTC",
        ip_address=None,
        user_agent=None,
    )


def make_use_case() -> AsyncMock:
    use_case = AsyncMock()

    use_case.execute.return_value = type(
        "CreateEmployeeLeaveBalanceResponse",
        (),
        {
            "id": "01K2TESTLEAVEBALANCE01",
            "employee_leave_assignment_id": ASSIGNMENT_ID,
            "employee_id": EMPLOYEE_ID,
            "period_start": date(2026, 1, 1),
            "period_end": date(2026, 12, 31),
            "entitlement_days": Decimal("24.00"),
            "carried_forward_days": Decimal("2.00"),
            "accrued_days": Decimal("10.50"),
            "used_days": Decimal("5.50"),
            "adjustment_days": Decimal("1.00"),
            "is_active": True,
            "created_at": datetime(
                2026,
                9,
                1,
                4,
                0,
                tzinfo=timezone.utc,
            ),
        },
    )()

    return use_case


def install_overrides(
    use_case: AsyncMock,
) -> None:
    request_context = make_request_context()

    app.dependency_overrides[get_create_employee_leave_balance_use_case] = (
        lambda: use_case
    )

    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    app.dependency_overrides[get_authenticated_request_context] = (
        lambda: request_context
    )


def test_create_employee_leave_balance_returns_created_response() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/leave/employee-balances",
            json=make_payload(),
        )

        assert response.status_code == 201

        assert response.json() == {
            "id": "01K2TESTLEAVEBALANCE01",
            "employee_leave_assignment_id": ASSIGNMENT_ID,
            "employee_id": EMPLOYEE_ID,
            "period_start": "2026-01-01",
            "period_end": "2026-12-31",
            "entitlement_days": "24.00",
            "carried_forward_days": "2.00",
            "accrued_days": "10.50",
            "used_days": "5.50",
            "adjustment_days": "1.00",
            "is_active": True,
            "created_at": "2026-09-01T04:00:00Z",
        }

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.tenant_id == TENANT_ID
        assert command.employee_leave_assignment_id == ASSIGNMENT_ID
        assert command.employee_id == EMPLOYEE_ID
        assert command.period_start == date(2026, 1, 1)
        assert command.period_end == date(2026, 12, 31)
        assert command.entitlement_days == Decimal("24.00")
        assert command.carried_forward_days == Decimal("2.00")
        assert command.accrued_days == Decimal("10.50")
        assert command.used_days == Decimal("5.50")
        assert command.adjustment_days == Decimal("1.00")
        assert command.is_active is True

    finally:
        app.dependency_overrides.clear()


def test_create_employee_leave_balance_does_not_accept_client_tenant_id() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["tenant_id"] = "ATTACKER_TENANT"

        response = client.post(
            "/api/v1/leave/employee-balances",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_leave_balance_allows_negative_adjustment() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["adjustment_days"] = "-3.50"

        response = client.post(
            "/api/v1/leave/employee-balances",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.adjustment_days == Decimal("-3.50")

    finally:
        app.dependency_overrides.clear()


def test_create_employee_leave_balance_defaults_to_zero_values() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("entitlement_days")
        payload.pop("carried_forward_days")
        payload.pop("accrued_days")
        payload.pop("used_days")
        payload.pop("adjustment_days")

        response = client.post(
            "/api/v1/leave/employee-balances",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.entitlement_days == Decimal("0")
        assert command.carried_forward_days == Decimal("0")
        assert command.accrued_days == Decimal("0")
        assert command.used_days == Decimal("0")
        assert command.adjustment_days == Decimal("0")

    finally:
        app.dependency_overrides.clear()


def test_create_employee_leave_balance_defaults_to_active() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("is_active")

        response = client.post(
            "/api/v1/leave/employee-balances",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.is_active is True

    finally:
        app.dependency_overrides.clear()


def test_create_employee_leave_balance_requires_assignment_id() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("employee_leave_assignment_id")

        response = client.post(
            "/api/v1/leave/employee-balances",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_leave_balance_requires_employee_id() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("employee_id")

        response = client.post(
            "/api/v1/leave/employee-balances",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_leave_balance_requires_period_start() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("period_start")

        response = client.post(
            "/api/v1/leave/employee-balances",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_employee_leave_balance_requires_period_end() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("period_end")

        response = client.post(
            "/api/v1/leave/employee-balances",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()