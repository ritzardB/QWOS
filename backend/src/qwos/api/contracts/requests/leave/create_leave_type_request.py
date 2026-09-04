from __future__ import annotations

from pydantic import Field

from qwos.api.contracts.requests.common.base_request import BaseRequest


class CreateLeaveTypeRequest(BaseRequest):
    """
    API request for creating a tenant leave type.
    """

    leave_code: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    leave_name: str = Field(
        ...,
        min_length=1,
        max_length=150,
    )

    description: str | None = None

    is_paid: bool = True

    is_active: bool = True