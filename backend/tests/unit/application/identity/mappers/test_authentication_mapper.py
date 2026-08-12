"""
Tests for the AuthenticationMapper.
"""

from __future__ import annotations

from pydantic import SecretStr

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
from qwos.application.identity.mappers.authentication_mapper import (
    AuthenticationMapper,
)


def test_to_request_password_reset_command_maps_email() -> None:
    request = ForgotPasswordRequest(
        email="richard@example.com",
    )

    command = AuthenticationMapper.to_request_password_reset_command(
        request,
    )

    assert isinstance(command, RequestPasswordResetCommand)
    assert command.email == "richard@example.com"


def test_to_request_password_reset_command_uses_normalized_email() -> None:
    request = ForgotPasswordRequest(
        email="  richard@example.com  ",
    )

    command = AuthenticationMapper.to_request_password_reset_command(
        request,
    )

    assert command.email == "richard@example.com"


def test_to_reset_password_command_maps_token() -> None:
    request = ResetPasswordRequest(
        token="secure-reset-token",
        new_password="NewPassword123!",
        confirm_password="NewPassword123!",
    )

    command = AuthenticationMapper.to_reset_password_command(
        request,
    )

    assert isinstance(command, ResetPasswordCommand)
    assert command.token == "secure-reset-token"


def test_to_reset_password_command_unwraps_secret_passwords() -> None:
    request = ResetPasswordRequest(
        token="secure-reset-token",
        new_password=SecretStr("NewPassword123!"),
        confirm_password=SecretStr("NewPassword123!"),
    )

    command = AuthenticationMapper.to_reset_password_command(
        request,
    )

    assert command.new_password == "NewPassword123!"
    assert command.confirm_password == "NewPassword123!"


def test_to_reset_password_command_returns_plain_strings() -> None:
    request = ResetPasswordRequest(
        token="secure-reset-token",
        new_password=SecretStr("NewPassword123!"),
        confirm_password=SecretStr("NewPassword123!"),
    )

    command = AuthenticationMapper.to_reset_password_command(
        request,
    )

    assert isinstance(command.new_password, str)
    assert isinstance(command.confirm_password, str)
    assert not isinstance(command.new_password, SecretStr)
    assert not isinstance(command.confirm_password, SecretStr)