"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    base_response.py

Description:
    Base class for all response contracts.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class BaseResponse(BaseModel):
    """
    Base class for all response contracts.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra="ignore",
    )
