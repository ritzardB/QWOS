"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    authenticate_user_command.py

Description:
    Command representing the intention to authenticate a user.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuthenticateUserCommand:
    """
    Command for authenticating a user.
    """

    tenant_id: str
    email: str
    password: str
    remember_me: bool = False