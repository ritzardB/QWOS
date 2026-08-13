"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    request_password_reset_command.py

Description:
    Command representing a request to initiate password recovery.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RequestPasswordResetCommand:
    """
    Command for requesting a password reset.
    """

    email: str
