from __future__ import annotations

from datetime import date

from pydantic import Field

from qwos.api.contracts.requests.common.base_request import BaseRequest


class CreateEmployeeLeaveAssignmentRequest(BaseRequest):
    employee_id: str = Field(..., min_length=1, max_length=26)
    leave_policy_id: str = Field(..., min_length=1, max_length=26)
    effective_from: date
    effective_until: date | None = None
    is_active: bool = True