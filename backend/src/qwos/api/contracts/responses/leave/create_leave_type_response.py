from __future__ import annotations

from datetime import datetime

from qwos.api.contracts.responses.common.base_response import BaseResponse


class CreateLeaveTypeResponse(BaseResponse):
    """
    API response for a newly created leave type.
    """

    id: str
    leave_code: str
    leave_name: str
    description: str | None
    is_paid: bool
    is_active: bool
    created_at: datetime