"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    refresh_access_token_command.py

Description:
    Command representing the intention to refresh an authenticated session.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RefreshAccessTokenCommand:
    """
    Command for refreshing an authenticated session.

    The raw refresh token is supplied by the client and must never be
    persisted by the application.
    """

    refresh_token: str