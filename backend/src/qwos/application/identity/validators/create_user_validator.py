"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    create_user_validator.py

Description:
    Validates CreateUserCommand before execution.

Responsibilities:
    - Validate required fields
    - Validate field formats
    - Validate basic business-independent rules

Notes:
    This validator performs only structural validation.
    Business rules requiring repositories belong in the Use Case.
===============================================================================
"""

from __future__ import annotations

import re

from qwos.application.common.results.validation_error import ValidationError
from qwos.application.common.results.validation_result import ValidationResult
from qwos.application.identity.commands.create_user_command import (
    CreateUserCommand,
)


class CreateUserValidator:
    """
    Validator for CreateUserCommand.
    """

    EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9._-]{3,50}$")

    def validate(
        self,
        command: CreateUserCommand,
    ) -> ValidationResult:
        """
        Validate the command.
        """

        errors: list[ValidationError] = []

        # ---------------------------------------------------------
        # First Name
        # ---------------------------------------------------------

        if not command.first_name.strip():
            errors.append(
                ValidationError(
                    field="first_name",
                    message="First name is required.",
                )
            )

        elif len(command.first_name) > 100:
            errors.append(
                ValidationError(
                    field="first_name",
                    message="First name cannot exceed 100 characters.",
                )
            )

        # ---------------------------------------------------------
        # Last Name
        # ---------------------------------------------------------

        if not command.last_name.strip():
            errors.append(
                ValidationError(
                    field="last_name",
                    message="Last name is required.",
                )
            )

        elif len(command.last_name) > 100:
            errors.append(
                ValidationError(
                    field="last_name",
                    message="Last name cannot exceed 100 characters.",
                )
            )

        # ---------------------------------------------------------
        # Email
        # ---------------------------------------------------------

        if not command.email.strip():
            errors.append(
                ValidationError(
                    field="email",
                    message="Email is required.",
                )
            )

        elif not self.EMAIL_PATTERN.fullmatch(command.email):
            errors.append(
                ValidationError(
                    field="email",
                    message="Email format is invalid.",
                )
            )

        # ---------------------------------------------------------
        # Username
        # ---------------------------------------------------------

        if not command.username.strip():
            errors.append(
                ValidationError(
                    field="username",
                    message="Username is required.",
                )
            )

        elif not self.USERNAME_PATTERN.fullmatch(command.username):
            errors.append(
                ValidationError(
                    field="username",
                    message=("Username must contain 3–50 letters, numbers, '.', '_' or '-'."),
                )
            )

        # ---------------------------------------------------------
        # Password
        # ---------------------------------------------------------

        if len(command.password) < 8:
            errors.append(
                ValidationError(
                    field="password",
                    message="Password must contain at least 8 characters.",
                )
            )

        # ---------------------------------------------------------
        # User Type
        # ---------------------------------------------------------

        if not command.user_type.strip():
            errors.append(
                ValidationError(
                    field="user_type",
                    message="User type is required.",
                )
            )

        return ValidationResult(errors=errors)
