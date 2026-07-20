"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    create_user_profile_request.py

Description:
    Request contract for creating a user profile.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date

from pydantic import EmailStr, Field

from qwos.core.contracts.requests.common.base_request import BaseRequest


class CreateUserProfileRequest(BaseRequest):
    """
    Request for creating a user profile.
    """

    first_name: str = Field(
        min_length=1,
        max_length=100,
    )

    middle_name: str | None = Field(
        default=None,
        max_length=100,
    )

    last_name: str = Field(
        min_length=1,
        max_length=100,
    )

    preferred_name: str | None = Field(
        default=None,
        max_length=100,
    )

    mobile_number: str | None = Field(
        default=None,
        max_length=30,
    )

    alternate_email: EmailStr | None = None

    birth_date: date | None = None
