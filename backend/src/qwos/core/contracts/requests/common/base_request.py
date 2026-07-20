"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    base_request.py

Description:
    Base class for all request contracts.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class BaseRequest(BaseModel):
    """
    Base class for all request contracts.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
        frozen=False,
    )
