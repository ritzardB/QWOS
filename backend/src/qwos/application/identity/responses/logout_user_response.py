"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    logout_user_response.py

Description:
    Response returned after successfully terminating an authenticated session.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LogoutUserResponse:
    """
    Response returned after successful logout.
    """

    success: bool
    message: str