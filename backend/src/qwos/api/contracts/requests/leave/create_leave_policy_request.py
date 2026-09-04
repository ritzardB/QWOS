from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from qwos.api.contracts.requests.common.base_request import BaseRequest


class CreateLeavePolicyRequest(BaseRequest):
    leave_type_id: str = Field(..., min_length=1, max_length=26)
    policy_code: str = Field(..., min_length=1, max_length=50)
    policy_name: str = Field(..., min_length=1, max_length=150)
    description: str | None = None
    entitlement_days: Decimal = Field(default=Decimal("0"), ge=0)
    accrual_method: str = Field(default="annual", min_length=1, max_length=50)
    accrual_frequency: str = Field(
        default="monthly",
        min_length=1,
        max_length=50,
    )
    carry_forward_allowed: bool = False
    carry_forward_days: Decimal | None = Field(default=None, ge=0)
    minimum_service_days: int = Field(default=0, ge=0)
    is_active: bool = True