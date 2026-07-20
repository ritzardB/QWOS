"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    error_response.py

Description:
    Standard API error response.
===============================================================================
"""

from __future__ import annotations

from qwos.core.contracts.responses.common.base_response import BaseResponse

from .error_detail import ErrorDetail


class ErrorResponse(BaseResponse):
    """
    Standard API error.
    """

    success: bool = False

    message: str

    errors: list[ErrorDetail]
