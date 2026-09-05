from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class CreateEmployeeLeaveAssignmentResponse:
    id: str
    employee_id: str
    leave_policy_id: str
    effective_from: date
    effective_until: date | None
    is_active: bool
    created_at: datetime