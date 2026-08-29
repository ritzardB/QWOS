"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Identity Module

File:
    create_user_response.py

Description:
    Response contract returned after successfully creating a user.

Responsibilities:
    - Return user creation details
    - No business logic

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from qwos.domains.identity.enums.account_status import AccountStatus
from qwos.domains.identity.enums.user_type import UserType


class CreateUserResponse(BaseModel):
    """
    Response returned after creating a user.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: str

    email: str

    username: str

    user_type: UserType

    account_status: AccountStatus

    created_at: datetime
