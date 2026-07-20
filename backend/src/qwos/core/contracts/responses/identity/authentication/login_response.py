from __future__ import annotations

from datetime import datetime

from qwos.core.contracts.responses.common.base_response import BaseResponse


class LoginResponse(BaseResponse):
    """
    Successful authentication response.
    """

    access_token: str

    refresh_token: str

    token_type: str = "Bearer"

    expires_at: datetime
