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

from qwos.api.contracts.requests.identity.authentication.change_password_request import (
    ChangePasswordRequest,
)
from qwos.api.contracts.requests.identity.authentication.forgot_password_request import (
    ForgotPasswordRequest,
)
from qwos.api.contracts.requests.identity.authentication.login_request import LoginRequest
from qwos.api.contracts.requests.identity.authentication.logout_request import (
    LogoutRequest,
)
from qwos.api.contracts.requests.identity.authentication.refresh_token_request import (
    RefreshTokenRequest,
)
from qwos.api.contracts.requests.identity.authentication.reset_password_request import (
    ResetPasswordRequest,
)
from qwos.api.contracts.requests.identity.create_user_request import (
    CreateUserRequest,
)
from qwos.api.contracts.responses.identity.authentication.authentication_response import (
    AuthenticationResponse,
)
from qwos.api.contracts.responses.identity.authentication.login_response import LoginResponse
from qwos.api.contracts.responses.identity.authentication.refresh_token_response import (
    RefreshTokenResponse,
)
from qwos.api.contracts.responses.identity.create_user_response import (
    CreateUserResponse as APICreateUserResponse,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies.identity import (
    get_authenticate_user_use_case,
    get_change_password_use_case,
    get_create_user_use_case,
    get_logout_user_use_case,
    get_refresh_access_token_use_case,
    get_request_context,
    get_request_password_reset_use_case,
    get_reset_password_use_case,
)
from qwos.application.identity.mappers.authentication_mapper import (
    AuthenticationMapper,
)
from qwos.application.identity.mappers.user_mapper import UserMapper
from qwos.application.identity.use_cases.authenticate_user_use_case import AuthenticateUserUseCase
from qwos.application.identity.use_cases.change_password_use_case import (
    ChangePasswordUseCase,
)
from qwos.application.identity.use_cases.create_user_use_case import (
    CreateUserUseCase,
)
from qwos.application.identity.use_cases.logout_user_use_case import (
    LogoutUserUseCase,
)
from qwos.application.identity.use_cases.refresh_access_token_use_case import (
    RefreshAccessTokenUseCase,
)
from qwos.application.identity.use_cases.request_password_reset_use_case import (
    RequestPasswordResetUseCase,
)
from qwos.application.identity.use_cases.reset_password_use_case import (
    ResetPasswordUseCase,
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

@router.post(
    "/authentication/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate User",
    description="Authenticate a user and issue access and refresh tokens.",
)
async def login(
    request: LoginRequest,
    request_context: RequestContext = Depends(
        get_request_context,
    ),
    use_case: AuthenticateUserUseCase = Depends(
        get_authenticate_user_use_case,
    ),
) -> LoginResponse:
    """
    Authenticate a user.
    """

    command = AuthenticationMapper.to_authenticate_user_command(
        request=request,
        request_context=request_context,
    )

    application_response = await use_case.execute(command)

    return LoginResponse(
        access_token=application_response.access_token,
        refresh_token=application_response.refresh_token,
        token_type=application_response.token_type,
        expires_at=application_response.expires_at,
    )

@router.post(
    "/authentication/refresh",
    response_model=RefreshTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh Access Token",
    description="Refresh the access and refresh tokens.",
)
async def refresh_access_token(
    request: RefreshTokenRequest,
    use_case: RefreshAccessTokenUseCase = Depends(
        get_refresh_access_token_use_case,
    ),
) -> RefreshTokenResponse:
    """
    Refresh the access and refresh tokens.
    """

    command = AuthenticationMapper.to_refresh_access_token_command(
        request,
    )

    application_response = await use_case.execute(command)

    return RefreshTokenResponse(
        access_token=application_response.access_token,
        refresh_token=application_response.refresh_token,
        expires_at=application_response.expires_at,
    )

@router.post(
    "/authentication/forgot-password",
    response_model=AuthenticationResponse,
    status_code=status.HTTP_200_OK,
    summary="Request Password Reset",
    description="Request a password reset.",
)
async def request_password_reset(
    request: ForgotPasswordRequest,
    use_case: RequestPasswordResetUseCase = Depends(
        get_request_password_reset_use_case,
    ),
) -> AuthenticationResponse:
    """
    Request a password reset.
    """

    command = AuthenticationMapper.to_request_password_reset_command(
        request,
    )

    application_response = await use_case.execute(command)

    return AuthenticationResponse(
        success=application_response.success,
        message=application_response.message,
    )

@router.post(
    "/authentication/reset-password",
    response_model=AuthenticationResponse,
    status_code=status.HTTP_200_OK,
    summary="Reset Password",
    description="Reset a user's password using a valid reset token.",
)
async def reset_password(
    request: ResetPasswordRequest,
    use_case: ResetPasswordUseCase = Depends(
        get_reset_password_use_case,
    ),
) -> AuthenticationResponse:
    """
    Reset a user's password.
    """

    command = AuthenticationMapper.to_reset_password_command(
        request,
    )

    application_response = await use_case.execute(command)

    return AuthenticationResponse(
        success=application_response.success,
        message=application_response.message,
    )

@router.post(
    "/authentication/change-password",
    response_model=AuthenticationResponse,
    status_code=status.HTTP_200_OK,
    summary="Change Password",
    description="Change the authenticated user's password.",
)
async def change_password(
    request: ChangePasswordRequest,
    use_case: ChangePasswordUseCase = Depends(
        get_change_password_use_case,
    ),
) -> AuthenticationResponse:
    """
    Change the authenticated user's password.
    """

    command = AuthenticationMapper.to_change_password_command(
        request,
    )

    application_response = await use_case.execute(command)

    return AuthenticationResponse(
        success=application_response.success,
        message=application_response.message,
    )

@router.post(
    "/authentication/logout",
    response_model=AuthenticationResponse,
    status_code=status.HTTP_200_OK,
    summary="Logout User",
    description="Terminate the authenticated user's session.",
)
async def logout(
    request: LogoutRequest,
    request_context: RequestContext = Depends(
        get_request_context,
    ),
    use_case: LogoutUserUseCase = Depends(
        get_logout_user_use_case,
    ),
) -> AuthenticationResponse:
    """
    Logout the authenticated user.
    """

    command = AuthenticationMapper.to_logout_user_command(
        request=request,
        request_context=request_context,
    )

    application_response = await use_case.execute(command)

    return AuthenticationResponse(
        success=application_response.success,
        message=application_response.message,
    )