from __future__ import annotations

from datetime import datetime

from qwos.api.contracts.responses.common.base_response import BaseResponse


class CreateWorkScheduleResponse(BaseResponse):
    """
    API response for a newly created work schedule.
    """

    id: str
    schedule_code: str
    schedule_name: str
    timezone: str
    is_active: bool
    created_at: datetime