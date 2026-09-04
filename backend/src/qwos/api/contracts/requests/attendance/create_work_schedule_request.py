from __future__ import annotations

from pydantic import Field

from qwos.api.contracts.requests.common.base_request import BaseRequest


class CreateWorkScheduleRequest(BaseRequest):
    """
    API request for creating a master work schedule.
    """

    schedule_code: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    schedule_name: str = Field(
        ...,
        min_length=1,
        max_length=150,
    )

    timezone: str = Field(
        default="UTC",
        min_length=1,
        max_length=100,
    )

    is_active: bool = True