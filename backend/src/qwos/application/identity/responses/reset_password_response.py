"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    reset_password_response.py

Description:
    Response returned after successfully resetting a password.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResetPasswordResponse:
    """
    Response returned after a successful password reset.
    """

    success: bool
    message: str
