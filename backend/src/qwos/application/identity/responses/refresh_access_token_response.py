"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    refresh_access_token_response.py

Description:
    Response returned after successfully refreshing authentication tokens.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class RefreshAccessTokenResponse:
    """
    Response returned after refreshing authentication tokens.
    """

    access_token: str
    refresh_token: str
    token_type: str
    expires_at: datetime
    user_id: str
    session_id: str