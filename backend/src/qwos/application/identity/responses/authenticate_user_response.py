"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    authenticate_user_response.py

Description:
    Response returned after successful user authentication.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class AuthenticateUserResponse:
    """
    Response returned after successful authentication.
    """

    access_token: str
    refresh_token: str
    token_type: str
    expires_at: datetime
    user_id: str
    session_id: str
