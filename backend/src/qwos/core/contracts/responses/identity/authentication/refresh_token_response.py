from __future__ import annotations

from datetime import datetime

from qwos.core.contracts.responses.common.base_response import BaseResponse


class RefreshTokenResponse(BaseResponse):
    """
    Refresh token response.
    """

    access_token: str

    refresh_token: str

    expires_at: datetime
