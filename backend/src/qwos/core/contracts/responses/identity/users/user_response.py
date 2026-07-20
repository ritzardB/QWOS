"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    user_response.py

Description:
    Response contract representing a user.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime

from pydantic import EmailStr

from qwos.core.contracts.responses.common.base_response import (
    BaseResponse,
)
from qwos.domains.identity.enums.account_status import AccountStatus
from qwos.domains.identity.enums.authentication_provider import (
    AuthenticationProvider,
)
from qwos.domains.identity.enums.user_type import UserType


class UserResponse(BaseResponse):
    """
    User response.
    """

    id: str

    tenant_id: str

    email: EmailStr

    username: str

    user_type: UserType

    authentication_provider: AuthenticationProvider

    account_status: AccountStatus

    created_at: datetime

    updated_at: datetime | None
