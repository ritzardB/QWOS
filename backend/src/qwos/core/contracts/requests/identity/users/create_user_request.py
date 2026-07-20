"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    create_user_request.py

Description:
    Request contract for creating a new user.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import EmailStr, Field

from qwos.core.contracts.requests.common.base_request import BaseRequest
from qwos.domains.identity.enums.authentication_provider import (
    AuthenticationProvider,
)
from qwos.domains.identity.enums.user_type import UserType


class CreateUserRequest(BaseRequest):
    """
    Request for creating a user.
    """

    email: EmailStr

    username: str = Field(
        min_length=3,
        max_length=100,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    user_type: UserType

    authentication_provider: AuthenticationProvider
