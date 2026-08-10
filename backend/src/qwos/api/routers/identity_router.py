"""
===============================================================================
Quantum Workforce OS (QWOS)

API Layer

Identity Router

Description:
    REST API endpoints for Identity Management.

Responsibilities:
    - Receive HTTP requests
    - Delegate to Application Use Cases
    - Return HTTP responses
    - No business logic

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, status

from qwos.api.contracts.requests.identity.create_user_request import (
    CreateUserRequest,
)
from qwos.api.contracts.responses.identity.create_user_response import (
    CreateUserResponse as APICreateUserResponse,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies.identity import (
    get_create_user_use_case,
    get_request_context,
)
from qwos.application.identity.mappers.user_mapper import UserMapper
from qwos.application.identity.use_cases.create_user_use_case import (
    CreateUserUseCase,
)

router = APIRouter(
    prefix="/identity",
    tags=["Identity"],
)


@router.post(
    "/users",
    response_model=APICreateUserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create User",
    description="Create a new user.",
)
async def create_user(
    request: CreateUserRequest,
    request_context: RequestContext = Depends(
        get_request_context,
    ),
    use_case: CreateUserUseCase = Depends(
        get_create_user_use_case,
    ),
) -> APICreateUserResponse:
    """
    Create a new user.
    """

    command = UserMapper.to_create_command(
        request=request,
        request_context=request_context,
    )

    application_response = await use_case.execute(command)

    return APICreateUserResponse(
        id=application_response.id,
        username=application_response.username,
        email=application_response.email,
        user_type=application_response.user_type,
        account_status=application_response.account_status,
        created_at=application_response.created_at,
    )