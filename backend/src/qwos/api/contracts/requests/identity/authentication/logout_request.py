"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    logout_request.py

Description:
    Request contract for terminating a user session.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import SecretStr

from qwos.api.contracts.requests.common.base_request import BaseRequest


class LogoutRequest(BaseRequest):
    """
    Logout request.
    """

    refresh_token: SecretStr
