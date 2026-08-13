"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    verify_email_request.py

Description:
    Request contract for verifying an email address.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.requests.common.base_request import BaseRequest


class VerifyEmailRequest(BaseRequest):
    """
    Verify a user's email address.
    """

    verification_token: str
