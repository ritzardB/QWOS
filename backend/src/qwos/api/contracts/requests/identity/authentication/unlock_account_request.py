"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    unlock_account_request.py

Description:
    Request contract for unlocking a locked account.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import EmailStr

from qwos.api.contracts.requests.common.base_request import BaseRequest


class UnlockAccountRequest(BaseRequest):
    """
    Unlock a user account.
    """

    email: EmailStr
