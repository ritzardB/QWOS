"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    create_user_use_case.py

Description:
    Creates a new user and corresponding user profile.

Responsibilities:
    - Validate the command
    - Enforce business rules
    - Create domain aggregates
    - Persist aggregates
    - Return application response

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.duplicate_resource_exception import (
    DuplicateResourceException,
)
from qwos.application.common.exceptions.validation_exception import (
    ValidationException,
)
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.clock import Clock
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.application.common.ports.password_hasher import PasswordHasher
from qwos.application.identity.commands.create_user_command import (
    CreateUserCommand,
)
from qwos.application.identity.mappers.user_mapper import UserMapper
from qwos.application.identity.responses.create_user_response import (
    CreateUserResponse,
)
from qwos.application.identity.validators.create_user_validator import (
    CreateUserValidator,
)
from qwos.domains.identity.models.user import User
from qwos.domains.identity.models.user_profile import UserProfile
from qwos.domains.identity.repositories.user_profile_repository import (
    UserProfileRepository,
)
from qwos.domains.identity.repositories.user_repository import (
    UserRepository,
)


class CreateUserUseCase:
    """
    Use case for creating a new user.
    """

    def __init__(
        self,
        *,
        user_repository: UserRepository,
        user_profile_repository: UserProfileRepository,
        password_hasher: PasswordHasher,
        id_generator: IdGenerator,
        clock: Clock,
        unit_of_work: UnitOfWork,
        validator: CreateUserValidator,
        request_context: RequestContext,
    ) -> None:
        self._user_repository = user_repository
        self._user_profile_repository = user_profile_repository
        self._password_hasher = password_hasher
        self._id_generator = id_generator
        self._clock = clock
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._request_context = request_context

    async def execute(
        self,
        command: CreateUserCommand,
    ) -> CreateUserResponse:
        """
        Execute the Create User use case.
        """

        # ------------------------------------------------------------------
        # Validate command
        # ------------------------------------------------------------------

        validation = self._validator.validate(command)

        if validation.errors:
            raise ValidationException(validation)

        # ------------------------------------------------------------------
        # Business Rules
        # ------------------------------------------------------------------

        if self._user_repository.exists_by_email(command.email):
            raise DuplicateResourceException(
                resource="User",
                field="email",
                value=command.email,
            )

        if self._user_repository.exists_by_username(command.username):
            raise DuplicateResourceException(
                resource="User",
                field="username",
                value=command.username,
            )

        # ------------------------------------------------------------------
        # Generate identifiers
        # ------------------------------------------------------------------

        user_id = self._id_generator.generate()
        profile_id = self._id_generator.generate()

        # ------------------------------------------------------------------
        # Security
        # ------------------------------------------------------------------

        password_hash = self._password_hasher.hash(
            command.password,
        )

        # ------------------------------------------------------------------
        # Create aggregates
        # ------------------------------------------------------------------

        user = User.create(
            id=user_id,
            tenant_id=command.tenant_id,
            email=command.email,
            username=command.username,
            password_hash=password_hash,
            user_type=command.user_type,
        )

        profile = UserProfile.create(
            id=profile_id,
            tenant_id=command.tenant_id,
            user_id=user.id,
            first_name=command.first_name,
            middle_name=command.middle_name,
            last_name=command.last_name,
            preferred_name=command.preferred_name,
        )

        # ------------------------------------------------------------------
        # Persist
        # ------------------------------------------------------------------

        with self._unit_of_work:
            self._user_repository.save(user)
            self._user_profile_repository.save(profile)
            self._unit_of_work.flush()

        # ------------------------------------------------------------------
        # Response
        # ------------------------------------------------------------------

        return UserMapper.to_create_response(
            user=user,
            profile=profile,
        )
