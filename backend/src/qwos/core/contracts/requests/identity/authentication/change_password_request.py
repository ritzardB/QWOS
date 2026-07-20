"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    change_password_request.py

Description:
    Request contract for changing a user's password.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import Field, SecretStr

from qwos.core.contracts.requests.common.base_request import BaseRequest


class ChangePasswordRequest(BaseRequest):
    """
    Change the authenticated user's password.
    """

    current_password: SecretStr

    new_password: SecretStr = Field(
        min_length=8,
        max_length=128,
    )

    confirm_password: SecretStr = Field(
        min_length=8,
        max_length=128,
    )
