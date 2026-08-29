"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Identity Module

File:
    create_user_request.py

Description:
    Request contract for creating a new user.

Responsibilities:
    - Accept user registration data
    - Perform basic transport-level validation
    - No business logic

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import EmailStr, Field

from qwos.api.contracts.requests.common.base_request import BaseRequest
from qwos.domains.identity.enums.user_type import UserType


class CreateUserRequest(BaseRequest):
    """
    Request for creating a new user.
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

    first_name: str = Field(
        min_length=1,
        max_length=100,
    )

    middle_name: str | None = Field(
        default=None,
        max_length=100,
    )

    last_name: str = Field(
        min_length=1,
        max_length=100,
    )

    preferred_name: str | None = Field(
        default=None,
        max_length=100,
    )

    user_type: UserType = UserType.EMPLOYEE
