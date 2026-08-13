"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    request_password_reset_response.py

Description:
    Response returned after requesting a password reset.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RequestPasswordResetResponse:
    """
    Response returned after a password reset request.
    """

    success: bool
    message: str
