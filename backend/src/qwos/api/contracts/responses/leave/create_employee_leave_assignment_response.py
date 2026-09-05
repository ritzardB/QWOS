from __future__ import annotations

from datetime import date, datetime

from qwos.api.contracts.responses.common.base_response import BaseResponse


class CreateEmployeeLeaveAssignmentResponse(BaseResponse):
    id: str
    employee_id: str
    leave_policy_id: str
    effective_from: date
    effective_until: date | None
    is_active: bool
    created_at: datetime