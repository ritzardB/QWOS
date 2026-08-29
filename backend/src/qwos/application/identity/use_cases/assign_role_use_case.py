"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    assign_role_use_case.py

Description:
    Assigns an existing role to an existing user.

Responsibilities:
    - Validate tenant ownership
    - Verify user existence
    - Verify role existence
    - Prevent duplicate assignments
    - Create UserRole
    - Persist the assignment

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.duplicate_resource_exception import (
    DuplicateResourceException,
)
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.clock import Clock
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.application.identity.commands.assign_role_command import (
    AssignRoleCommand,
)
from qwos.application.identity.responses.assign_role_response import (
    AssignRoleResponse,
)
from qwos.domains.identity.models.user_role import UserRole
from qwos.domains.identity.repositories.role_repository import (
    RoleRepository,
)
from qwos.domains.identity.repositories.user_repository import (
    UserRepository,
)
from qwos.domains.identity.repositories.user_role_repository import (
    UserRoleRepository,
)


class AssignRoleUseCase:
    """
    Use case for assigning a role to a user.
    """

    def __init__(
        self,
        *,
        user_repository: UserRepository,
        role_repository: RoleRepository,
        user_role_repository: UserRoleRepository,
        id_generator: IdGenerator,
        clock: Clock,
        unit_of_work: UnitOfWork,
        request_context: RequestContext,
    ) -> None:
        self._user_repository = user_repository
        self._role_repository = role_repository
        self._user_role_repository = user_role_repository
        self._id_generator = id_generator
        self._clock = clock
        self._unit_of_work = unit_of_work
        self._request_context = request_context

    async def execute(
        self,
        command: AssignRoleCommand,
    ) -> AssignRoleResponse:
        """
        Execute the Assign Role use case.
        """

        tenant_id = self._request_context.tenant_id

        # ------------------------------------------------------------------
        # User
        # ------------------------------------------------------------------

        user = self._user_repository.get_by_id(
            command.user_id,
        )

        if user is None:
            raise ResourceNotFoundException(
                resource="User",
                identifier=command.user_id,
            )

        if user.tenant_id != tenant_id:
            raise ResourceNotFoundException(
                resource="User",
                identifier=command.user_id,
            )

        # ------------------------------------------------------------------
        # Role
        # ------------------------------------------------------------------

        role = self._role_repository.get_by_id(
            command.role_id,
        )

        if role is None:
            raise ResourceNotFoundException(
                resource="Role",
                identifier=command.role_id,
            )

        if role.tenant_id != tenant_id:
            raise ResourceNotFoundException(
                resource="Role",
                identifier=command.role_id,
            )

        if role.deleted_at is not None:
            raise ResourceNotFoundException(
                resource="Role",
                identifier=command.role_id,
            )

        if not role.is_active:
            raise ResourceNotFoundException(
                resource="Role",
                identifier=command.role_id,
            )

        # ------------------------------------------------------------------
        # Duplicate Assignment
        # ------------------------------------------------------------------

        if self._user_role_repository.exists_assignment(
            user_id=command.user_id,
            role_id=command.role_id,
        ):
            raise DuplicateResourceException(
                resource="UserRole",
                field="user_id/role_id",
                value=(f"{command.user_id}/{command.role_id}"),
            )

        # ------------------------------------------------------------------
        # Create Assignment
        # ------------------------------------------------------------------

        now = self._clock.now()

        user_role = UserRole.create(
            id=self._id_generator.generate(),
            tenant_id=tenant_id,
            user_id=command.user_id,
            role_id=command.role_id,
            assigned_at=now,
            assigned_by=self._request_context.user_id,
        )

        # ------------------------------------------------------------------
        # Persist
        # ------------------------------------------------------------------

        with self._unit_of_work:
            self._user_role_repository.save(user_role)
            self._unit_of_work.flush()

        # ------------------------------------------------------------------
        # Response
        # ------------------------------------------------------------------

        return AssignRoleResponse(
            id=user_role.id,
            user_id=user_role.user_id,
            role_id=user_role.role_id,
            is_primary=user_role.is_primary,
            is_enabled=user_role.is_enabled,
            assigned_at=user_role.assigned_at,
        )
