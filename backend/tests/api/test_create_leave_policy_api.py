"""
===============================================================================
Quantum Workforce OS (QWOS)

API Tests

File:
    test_create_leave_policy_api.py

Description:
    API tests for the Create Leave Policy endpoint.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies import get_request_context
from qwos.application.common.dependencies.authentication import (
    get_authenticated_request_context,
)
from qwos.application.common.dependencies.leave import (
    get_create_leave_policy_use_case,
)
from qwos.main import app

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
USER_ID = "01KZYTCWRF8S12V28R9NX6JXS5"
LEAVE_TYPE_ID = "01K2TESTLEAVETYPE00000001"


def make_payload() -> dict[str, object]:
    return {
        "leave_type_id": LEAVE_TYPE_ID,
        "policy_code": "annual-standard",
        "policy_name": "Annual Standard",
        "description": "Standard annual leave policy.",
        "entitlement_days": "30.00",
        "accrual_method": "annual",
        "accrual_frequency": "monthly",
        "carry_forward_allowed": False,
        "carry_forward_days": None,
        "minimum_service_days": 0,
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
        "CreateLeavePolicyResponse",
        (),
        {
            "id": "01K2TESTLEAVEPOLICY0000001",
            "leave_type_id": LEAVE_TYPE_ID,
            "policy_code": "annual-standard",
            "policy_name": "Annual Standard",
            "description": "Standard annual leave policy.",
            "entitlement_days": Decimal("30.00"),
            "accrual_method": "annual",
            "accrual_frequency": "monthly",
            "carry_forward_allowed": False,
            "carry_forward_days": None,
            "minimum_service_days": 0,
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

    app.dependency_overrides[get_create_leave_policy_use_case] = (
        lambda: use_case
    )

    app.dependency_overrides[get_request_context] = (
        lambda: request_context
    )

    app.dependency_overrides[get_authenticated_request_context] = (
        lambda: request_context
    )


def test_create_leave_policy_returns_created_response() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/leave/policies",
            json=make_payload(),
        )

        assert response.status_code == 201

        assert response.json() == {
            "id": "01K2TESTLEAVEPOLICY0000001",
            "leave_type_id": LEAVE_TYPE_ID,
            "policy_code": "annual-standard",
            "policy_name": "Annual Standard",
            "description": "Standard annual leave policy.",
            "entitlement_days": "30.00",
            "accrual_method": "annual",
            "accrual_frequency": "monthly",
            "carry_forward_allowed": False,
            "carry_forward_days": None,
            "minimum_service_days": 0,
            "is_active": True,
            "created_at": "2026-09-01T04:00:00Z",
        }

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.tenant_id == TENANT_ID
        assert command.leave_type_id == LEAVE_TYPE_ID
        assert command.policy_code == "annual-standard"
        assert command.policy_name == "Annual Standard"
        assert command.description == "Standard annual leave policy."
        assert command.entitlement_days == Decimal("30.00")
        assert command.accrual_method == "annual"
        assert command.accrual_frequency == "monthly"
        assert command.carry_forward_allowed is False
        assert command.carry_forward_days is None
        assert command.minimum_service_days == 0
        assert command.is_active is True

    finally:
        app.dependency_overrides.clear()


def test_create_leave_policy_does_not_accept_client_tenant_id() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["tenant_id"] = "ATTACKER_TENANT"

        response = client.post(
            "/api/v1/leave/policies",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_leave_policy_defaults_to_zero_entitlement() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("entitlement_days")

        response = client.post(
            "/api/v1/leave/policies",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.entitlement_days == Decimal("0")

    finally:
        app.dependency_overrides.clear()


def test_create_leave_policy_defaults_to_annual_accrual() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("accrual_method")

        response = client.post(
            "/api/v1/leave/policies",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.accrual_method == "annual"

    finally:
        app.dependency_overrides.clear()


def test_create_leave_policy_defaults_to_monthly_accrual() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("accrual_frequency")

        response = client.post(
            "/api/v1/leave/policies",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.accrual_frequency == "monthly"

    finally:
        app.dependency_overrides.clear()


def test_create_leave_policy_defaults_to_no_carry_forward() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("carry_forward_allowed")

        response = client.post(
            "/api/v1/leave/policies",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.carry_forward_allowed is False

    finally:
        app.dependency_overrides.clear()


def test_create_leave_policy_defaults_to_zero_service_days() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("minimum_service_days")

        response = client.post(
            "/api/v1/leave/policies",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.minimum_service_days == 0

    finally:
        app.dependency_overrides.clear()


def test_create_leave_policy_defaults_to_active() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("is_active")

        response = client.post(
            "/api/v1/leave/policies",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.is_active is True

    finally:
        app.dependency_overrides.clear()


def test_create_leave_policy_accepts_carry_forward_days() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["carry_forward_allowed"] = True
        payload["carry_forward_days"] = "10.00"

        response = client.post(
            "/api/v1/leave/policies",
            json=payload,
        )

        assert response.status_code == 201

        use_case.execute.assert_awaited_once()

        command = use_case.execute.await_args.args[0]

        assert command.carry_forward_allowed is True
        assert command.carry_forward_days == Decimal("10.00")

    finally:
        app.dependency_overrides.clear()


def test_create_leave_policy_rejects_missing_leave_type_id() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("leave_type_id")

        response = client.post(
            "/api/v1/leave/policies",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_leave_policy_rejects_missing_policy_code() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("policy_code")

        response = client.post(
            "/api/v1/leave/policies",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_leave_policy_rejects_missing_policy_name() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload.pop("policy_name")

        response = client.post(
            "/api/v1/leave/policies",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_leave_policy_rejects_negative_entitlement() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["entitlement_days"] = "-1.00"

        response = client.post(
            "/api/v1/leave/policies",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_leave_policy_rejects_negative_carry_forward_days() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["carry_forward_days"] = "-1.00"

        response = client.post(
            "/api/v1/leave/policies",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()


def test_create_leave_policy_rejects_negative_service_days() -> None:
    use_case = make_use_case()
    install_overrides(use_case)

    try:
        client = TestClient(app)

        payload = make_payload()
        payload["minimum_service_days"] = -1

        response = client.post(
            "/api/v1/leave/policies",
            json=payload,
        )

        assert response.status_code == 422
        use_case.execute.assert_not_awaited()

    finally:
        app.dependency_overrides.clear()