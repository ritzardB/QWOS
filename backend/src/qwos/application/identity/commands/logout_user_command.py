"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    logout_user_command.py

Description:
    Command representing the intention to terminate an authenticated session.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LogoutUserCommand:
    """
    Command for logging out an authenticated user.
    """

    tenant_id: str
    refresh_token: str
