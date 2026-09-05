from __future__ import annotations

from datetime import date
from decimal import Decimal

from qwos.api.contracts.requests.common.base_request import BaseRequest


class CreateEmployeeLeaveBalanceRequest(BaseRequest):
    employee_leave_assignment_id: str
    employee_id: str
    period_start: date
    period_end: date
    entitlement_days: Decimal = Decimal("0")
    carried_forward_days: Decimal = Decimal("0")
    accrued_days: Decimal = Decimal("0")
    used_days: Decimal = Decimal("0")
    adjustment_days: Decimal = Decimal("0")
    is_active: bool = True