"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Application Exception Handler

Description:
    Translates application-layer exceptions into standardized HTTP responses.

Responsibilities:
    - Convert application-layer exceptions into HTTP responses
    - Preserve application-layer error information
    - Keep HTTP concerns outside the application layer
===============================================================================
"""

from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse

from qwos.api.contracts.common.error_detail import ErrorDetail
from qwos.api.contracts.common.error_response import ErrorResponse
from qwos.application.common.exceptions.account_locked_exception import (
    AccountLockedException,
)
from qwos.application.common.exceptions.application_exception import (
    ApplicationException,
)
from qwos.application.common.exceptions.duplicate_resource_exception import (
    DuplicateResourceException,
)
from qwos.application.common.exceptions.forbidden_exception import (
    ForbiddenException,
)
from qwos.application.common.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.common.exceptions.validation_exception import (
    ValidationException,
)


def _get_status_code(
    exc: ApplicationException,
) -> int:
    """
    Return the HTTP status code associated with an application exception.
    """
    if isinstance(exc, ForbiddenException):
        return 403

    if isinstance(exc, ValidationException):
        return 400

    if isinstance(exc, InvalidCredentialsException):
        return 401

    if isinstance(exc, AccountLockedException):
        return 423

    if isinstance(exc, DuplicateResourceException):
        return 409

    if isinstance(exc, ResourceNotFoundException):
        return 404

    return 400


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
        status_code=_get_status_code(exc),
        content=response.model_dump(mode="json"),
    )


def _get_status_code(
    exc: ApplicationException,
) -> int:
    """
    Return the HTTP status code associated with an application exception.
    """

    if isinstance(exc, ValidationException):
        return 400

    if isinstance(exc, InvalidCredentialsException):
        return 401

    if isinstance(exc, AccountLockedException):
        return 423

    if isinstance(exc, DuplicateResourceException):
        return 409

    if isinstance(exc, ResourceNotFoundException):
        return 404

    if isinstance(exc, ForbiddenException):
        return 403

    return 400
