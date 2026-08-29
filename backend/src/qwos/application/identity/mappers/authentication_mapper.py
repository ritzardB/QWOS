"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    authentication_mapper.py

Description:
    Maps authentication API contracts to application commands.

Responsibilities:
    - Forgot-password request -> RequestPasswordResetCommand
    - Reset-password request -> ResetPasswordCommand
    - Safely unwrap SecretStr values
    - No business logic

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.requests.identity.authentication.change_password_request import (
    ChangePasswordRequest,
)
from qwos.api.contracts.requests.identity.authentication.forgot_password_request import (
    ForgotPasswordRequest,
)
from qwos.api.contracts.requests.identity.authentication.login_request import (
    LoginRequest,
)
from qwos.api.contracts.requests.identity.authentication.logout_request import (
    LogoutRequest,
)
from qwos.api.contracts.requests.identity.authentication.refresh_token_request import (
    RefreshTokenRequest,
)
from qwos.api.contracts.requests.identity.authentication.reset_password_request import (
    ResetPasswordRequest,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.identity.commands.authenticate_user_command import (
    AuthenticateUserCommand,
)
from qwos.application.identity.commands.change_password_command import (
    ChangePasswordCommand,
)
from qwos.application.identity.commands.logout_user_command import (
    LogoutUserCommand,
)
from qwos.application.identity.commands.refresh_access_token_command import (
    RefreshAccessTokenCommand,
)
from qwos.application.identity.commands.request_password_reset_command import (
    RequestPasswordResetCommand,
)
from qwos.application.identity.commands.reset_password_command import (
    ResetPasswordCommand,
)


class AuthenticationMapper:
    """
    Maps authentication API contracts to application commands.
    """

    # ------------------------------------------------------------------
    # Forgot Password
    # ------------------------------------------------------------------

    @staticmethod
    def to_request_password_reset_command(
        request: ForgotPasswordRequest,
    ) -> RequestPasswordResetCommand:
        """
        Convert ForgotPasswordRequest into RequestPasswordResetCommand.
        """

        return RequestPasswordResetCommand(
            email=str(request.email),
        )

    @staticmethod
    def to_authenticate_user_command(
        request: LoginRequest,
        request_context: RequestContext,
    ) -> AuthenticateUserCommand:
        """
        Convert LoginRequest into AuthenticateUserCommand.

        SecretStr values are explicitly unwrapped only at the
        API-to-application boundary.
        """

        return AuthenticateUserCommand(
            tenant_id=request_context.tenant_id,
            email=str(request.email),
            password=request.password.get_secret_value(),
            remember_me=request.remember_me,
        )

    # ------------------------------------------------------------------
    # Logout
    # ------------------------------------------------------------------

    @staticmethod
    def to_logout_user_command(
        request: LogoutRequest,
        request_context: RequestContext,
    ) -> LogoutUserCommand:
        """
        Convert LogoutRequest into LogoutUserCommand.

        SecretStr values are explicitly unwrapped only at the
        API-to-application boundary.
        """

        return LogoutUserCommand(
            tenant_id=request_context.tenant_id,
            refresh_token=request.refresh_token.get_secret_value(),
        )

    # ------------------------------------------------------------------
    # Reset Password
    # ------------------------------------------------------------------

    @staticmethod
    def to_reset_password_command(
        request: ResetPasswordRequest,
    ) -> ResetPasswordCommand:
        """
        Convert ResetPasswordRequest into ResetPasswordCommand.

        SecretStr values are explicitly unwrapped only at the
        API-to-application boundary.
        """

        return ResetPasswordCommand(
            token=request.token,
            new_password=request.new_password.get_secret_value(),
            confirm_password=request.confirm_password.get_secret_value(),
        )

    # ------------------------------------------------------------------
    # Change Password
    # -----------

    @staticmethod
    def to_change_password_command(
        request: ChangePasswordRequest,
    ) -> ChangePasswordCommand:
        """
        Convert ChangePasswordRequest into ChangePasswordCommand.

        SecretStr values are explicitly unwrapped only at the
        API-to-application boundary.
        """

        return ChangePasswordCommand(
            current_password=request.current_password.get_secret_value(),
            new_password=request.new_password.get_secret_value(),
        )

    # ------------------------------------------------------------------
    # Refresh Access Token
    # ------------------------------------------------------------------

    @staticmethod
    def to_refresh_access_token_command(
        request: RefreshTokenRequest,
    ) -> RefreshAccessTokenCommand:
        """
        Convert RefreshTokenRequest into RefreshAccessTokenCommand.

        SecretStr values are explicitly unwrapped only at the
        API-to-application boundary.
        """

        return RefreshAccessTokenCommand(
            refresh_token=request.refresh_token.get_secret_value(),
        )
