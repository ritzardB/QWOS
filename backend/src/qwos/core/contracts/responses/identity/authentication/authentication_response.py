from __future__ import annotations

from qwos.core.contracts.responses.common.base_response import BaseResponse


class AuthenticationResponse(BaseResponse):
    """
    Generic authentication operation response.
    """

    success: bool

    message: str
