from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CreateLeavePolicyCommand:
    tenant_id: str
    leave_type_id: str
    policy_code: str
    policy_name: str
    description: str | None = None
    entitlement_days: Decimal = Decimal("0")
    accrual_method: str = "annual"
    accrual_frequency: str = "monthly"
    carry_forward_allowed: bool = False
    carry_forward_days: Decimal | None = None
    minimum_service_days: int = 0
    is_active: bool = True