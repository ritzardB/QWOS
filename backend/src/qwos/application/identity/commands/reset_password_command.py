"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    reset_password_command.py

Description:
    Command representing the intention to reset a password using a valid
    password-reset token.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResetPasswordCommand:
    """
    Command for resetting a user's password.
    """

    token: str
    new_password: str
    confirm_password: str
