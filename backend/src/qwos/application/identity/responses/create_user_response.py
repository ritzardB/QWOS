"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    create_user_response.py

Description:
    Response returned after successfully creating a user.

Responsibilities:
    - Represent the outcome of the CreateUserUseCase
    - Remain immutable
    - Contain no business logic

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from qwos.domains.identity.enums.account_status import AccountStatus
from qwos.domains.identity.enums.user_type import UserType


@dataclass(frozen=True, slots=True)
class CreateUserResponse:
    """
    Response returned after creating a user.
    """

    id: str
    first_name: str
    last_name: str
    email: str
    username: str
    user_type: UserType
    account_status: AccountStatus
    created_at: datetime
