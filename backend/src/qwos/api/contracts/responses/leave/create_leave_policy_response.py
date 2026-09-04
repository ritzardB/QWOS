from datetime import datetime
from decimal import Decimal

from qwos.api.contracts.responses.common.base_response import BaseResponse


class CreateLeavePolicyResponse(BaseResponse):
    id: str
    leave_type_id: str
    policy_code: str
    policy_name: str
    description: str | None
    entitlement_days: Decimal
    accrual_method: str
    accrual_frequency: str
    carry_forward_allowed: bool
    carry_forward_days: Decimal | None
    minimum_service_days: int
    is_active: bool
    created_at: datetime