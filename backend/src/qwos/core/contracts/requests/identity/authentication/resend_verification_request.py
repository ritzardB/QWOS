"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    resend_verification_request.py

Description:
    Request contract for resending an email verification.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import EmailStr

from qwos.core.contracts.requests.common.base_request import BaseRequest


class ResendVerificationRequest(BaseRequest):
    """
    Resend an email verification.
    """

    email: EmailStr
