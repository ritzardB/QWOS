from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal


@dataclass(frozen=True)
class CreateEmployeeLeaveBalanceResponse:
    id: str
    employee_leave_assignment_id: str
    employee_id: str
    period_start: date
    period_end: date
    entitlement_days: Decimal
    carried_forward_days: Decimal
    accrued_days: Decimal
    used_days: Decimal
    adjustment_days: Decimal
    is_active: bool
    created_at: datetime