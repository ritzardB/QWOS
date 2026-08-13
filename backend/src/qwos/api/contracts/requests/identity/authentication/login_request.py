"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    login_request.py

Description:
    Request contract for user authentication.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import EmailStr, Field, SecretStr

from qwos.api.contracts.requests.common.base_request import BaseRequest


class LoginRequest(BaseRequest):
    """
    Authenticate a user.
    """

    email: EmailStr

    password: SecretStr = Field(
        min_length=8,
        max_length=128,
    )

    remember_me: bool = False
