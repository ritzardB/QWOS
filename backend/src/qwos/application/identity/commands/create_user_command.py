"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    create_user_command.py

Description:
    Command representing the intention to create a new user.

Responsibilities:
    - Carry user creation data
    - Remain immutable
    - Contain no business logic

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from qwos.domains.identity.enums.user_type import UserType


@dataclass(frozen=True, slots=True)
class CreateUserCommand:
    """
    Command for creating a new user.
    """

    tenant_id: str
    first_name: str
    last_name: str

    email: str
    username: str
    password: str

    middle_name: str | None = None
    preferred_name: str | None = None

    user_type: UserType = UserType.EMPLOYEE
