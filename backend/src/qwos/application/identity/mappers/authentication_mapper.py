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

from qwos.api.contracts.requests.identity.authentication.forgot_password_request import (
    ForgotPasswordRequest,
)
from qwos.api.contracts.requests.identity.authentication.reset_password_request import (
    ResetPasswordRequest,
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