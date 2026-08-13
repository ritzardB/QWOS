"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    change_password_response.py

Description:
    Response returned after successfully changing a user's password.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ChangePasswordResponse:
    """
    Response returned after a successful password change.
    """

    success: bool
    message: str