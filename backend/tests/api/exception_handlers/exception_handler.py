"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Application Exception Handler

Description:
    Translates application-layer exceptions into standardized HTTP responses.

Responsibilities:
    - Convert ApplicationException into ErrorResponse
    - Preserve application-layer error information
    - Keep HTTP concerns outside the application layer
===============================================================================
"""

from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse

from qwos.api.contracts.common.error_detail import ErrorDetail
from qwos.api.contracts.common.error_response import ErrorResponse
from qwos.application.common.exceptions.application_exception import (
    ApplicationException,
)


def application_exception_handler(
    request: Request,
    exc: ApplicationException,
) -> JSONResponse:
    """
    Convert an ApplicationException into a standardized API response.
    """

    response = ErrorResponse(
        message=exc.message,
        errors=[
            ErrorDetail(
                code=exc.__class__.__name__,
                message=exc.message,
            ),
        ],
    )

    return JSONResponse(
        status_code=400,
        content=response.model_dump(mode="json"),
    )