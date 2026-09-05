from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class CreateEmployeeLeaveAssignmentCommand:
    tenant_id: str
    employee_id: str
    leave_policy_id: str
    effective_from: date
    effective_until: date | None = None
    is_active: bool = True