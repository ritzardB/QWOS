"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    forgot_password_request.py

Description:
    Request contract for initiating a password reset.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import EmailStr

from qwos.api.contracts.requests.common.base_request import BaseRequest


class ForgotPasswordRequest(BaseRequest):
    """
    Request a password reset.
    """

    email: EmailStr
