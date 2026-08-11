"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    change_password_command.py

Description:
    Command representing the intention to change an authenticated user's
    password.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ChangePasswordCommand:
    """
    Command for changing an authenticated user's password.
    """

    current_password: str
    new_password: str