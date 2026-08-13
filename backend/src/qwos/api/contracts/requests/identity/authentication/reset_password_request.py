"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    reset_password_request.py

Description:
    Request contract for resetting a password.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import Field, SecretStr

from qwos.api.contracts.requests.common.base_request import BaseRequest


class ResetPasswordRequest(BaseRequest):
    """
    Reset a user's password.
    """

    token: str

    new_password: SecretStr = Field(
        min_length=8,
        max_length=128,
    )

    confirm_password: SecretStr = Field(
        min_length=8,
        max_length=128,
    )
