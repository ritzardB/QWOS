"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    user_mapper.py

Description:
    Maps API contracts, commands, domain aggregates,
    and application responses for the User aggregate.

Responsibilities:
    - Request → Command
    - Domain → Response

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.requests.identity.create_user_request import (
    CreateUserRequest,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.identity.commands.create_user_command import (
    CreateUserCommand,
)
from qwos.application.identity.responses.create_user_response import (
    CreateUserResponse,
)
from qwos.domains.identity.models.user import User
from qwos.domains.identity.models.user_profile import UserProfile


class UserMapper:
    """
    Maps User-related objects between application layers.
    """

    # ------------------------------------------------------------------
    # Request -> Command
    # ------------------------------------------------------------------

    @staticmethod
    def to_create_command(
        request: CreateUserRequest,
        request_context: RequestContext,
    ) -> CreateUserCommand:
        """
        Convert API request into CreateUserCommand.
        """

        return CreateUserCommand(
        tenant_id=request_context.tenant_id,
        email=request.email,
        username=request.username,
        password=request.password,
        first_name=request.first_name,
        middle_name=request.middle_name,
        last_name=request.last_name,
        preferred_name=request.preferred_name,
        user_type=request.user_type,
    )

    # ------------------------------------------------------------------
    # Domain -> Response
    # ------------------------------------------------------------------

    @staticmethod
    def to_create_response(
        user: User,
        profile: UserProfile,
    ) -> CreateUserResponse:
        """
        Convert User aggregate into CreateUserResponse.
        """

        return CreateUserResponse(
            id=user.id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            email=user.email,
            username=user.username,
            user_type=user.user_type,
            account_status=user.account_status,
            created_at=user.created_at,
    )