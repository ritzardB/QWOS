"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    error_detail.py

Description:
    Represents a single API error.
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.responses.common.base_response import BaseResponse


class ErrorDetail(BaseResponse):
    """
    Represents a single error.
    """

    code: str

    field: str | None = None

    message: str
