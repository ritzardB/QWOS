"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    update_user_request.py

Description:
    Request contract for updating an existing user.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import EmailStr, Field

from qwos.core.contracts.requests.common.base_request import BaseRequest
from qwos.domains.identity.enums.user_type import UserType


class UpdateUserRequest(BaseRequest):
    """
    Request for updating a user.
    """

    email: EmailStr | None = None

    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
    )

    user_type: UserType | None = None
