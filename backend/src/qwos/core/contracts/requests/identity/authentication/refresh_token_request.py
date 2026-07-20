"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    refresh_token_request.py

Description:
    Request contract for refreshing an access token.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import SecretStr

from qwos.core.contracts.requests.common.base_request import BaseRequest


class RefreshTokenRequest(BaseRequest):
    """
    Refresh authentication token.
    """

    refresh_token: SecretStr
