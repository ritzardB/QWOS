"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

File:
    authorization_service.py

Description:
    Service responsible for role-based access control (RBAC).

    Coordinates users, roles, permissions, user-role assignments,
    and role-permission assignments.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.ports.clock import Clock
from qwos.core.services.base_service import BaseService
from qwos.domains.identity.models.role_permission import RolePermission
from qwos.domains.identity.models.user_role import UserRole
from qwos.domains.identity.repositories.permission_repository import (
    PermissionRepository,
)
from qwos.domains.identity.repositories.role_permission_repository import (
    RolePermissionRepository,
)
from qwos.domains.identity.repositories.role_repository import (
    RoleRepository,
)
from qwos.domains.identity.repositories.user_repository import (
    UserRepository,
)
from qwos.domains.identity.repositories.user_role_repository import (
    UserRoleRepository,
)


class AuthorizationService(BaseService):
    """
    Business service responsible for authorization.
    """

    def __init__(
        self,
        users: UserRepository,
        roles: RoleRepository,
        permissions: PermissionRepository,
        user_roles: UserRoleRepository,
        role_permissions: RolePermissionRepository,
        clock: Clock,
    ) -> None:
        super().__init__()

        self._users = users
        self._roles = roles
        self._permissions = permissions
        self._user_roles = user_roles
        self._role_permissions = role_permissions
        self._clock = clock

    # ------------------------------------------------------------------
    # User Role Management
    # ------------------------------------------------------------------

    async def assign_role(
        self,
        user_id: str,
        role_id: str,
    ) -> None:
        """
        Assign a role to a user.
        """
        raise NotImplementedError()

    async def remove_role(
        self,
        user_id: str,
        role_id: str,
    ) -> None:
        """
        Remove a role from a user.
        """
        raise NotImplementedError()

    async def get_roles(
        self,
        user_id: str,
    ) -> list[UserRole]:
        """
        Retrieve all effective roles for a user.
        """
        raise NotImplementedError()

    async def has_role(
        self,
        user_id: str,
        role_code: str,
    ) -> bool:
        """
        Determine whether a user has a role.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------
    # Role Permission Management
    # ------------------------------------------------------------------

    async def grant_permission(
        self,
        role_id: str,
        permission_id: str,
    ) -> None:
        """
        Grant a permission to a role.
        """
        raise NotImplementedError()

    async def revoke_permission(
        self,
        role_id: str,
        permission_id: str,
    ) -> None:
        """
        Revoke a permission from a role.
        """
        raise NotImplementedError()

    async def get_permissions(
        self,
        role_id: str,
    ) -> list[RolePermission]:
        """
        Retrieve all permissions assigned to a role.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------
    # Authorization
    # ------------------------------------------------------------------

    async def has_permission(
        self,
        *,
        tenant_id: str,
        user_id: str,
        permission_code: str,
    ) -> bool:
        """
        Determine whether a user has an effective permission
        within the current tenant.
        """

        normalized_code = permission_code.strip().upper()

        effective_permissions = await self.get_effective_permissions(
            tenant_id=tenant_id,
            user_id=user_id,
        )

        return normalized_code in effective_permissions

    async def get_effective_permissions(
        self,
        *,
        tenant_id: str,
        user_id: str,
    ) -> list[str]:
        """
        Retrieve effective permission codes for a user
        within the current tenant.
        """

        now = self._clock.now()

        role_assignments = self._user_roles.list_active_roles(
            user_id=user_id,
        )

        permission_codes: set[str] = set()

        for user_role in role_assignments:
            # -----------------------------------------------------------------
            # Tenant isolation
            # -----------------------------------------------------------------

            if user_role.tenant_id != tenant_id:
                continue

            # -----------------------------------------------------------------
            # User role lifecycle
            # -----------------------------------------------------------------

            if not user_role.is_enabled:
                continue

            if user_role.deleted_at is not None:
                continue

            if user_role.effective_from is not None and user_role.effective_from > now:
                continue

            if user_role.effective_until is not None and user_role.effective_until < now:
                continue

            # -----------------------------------------------------------------
            # Resolve role
            # -----------------------------------------------------------------

            role = self._roles.get_by_id(
                user_role.role_id,
            )

            if role is None:
                continue

            if role.tenant_id != tenant_id:
                continue

            if role.deleted_at is not None:
                continue

            if not role.is_active:
                continue

            # -----------------------------------------------------------------
            # Resolve role permissions
            # -----------------------------------------------------------------

            role_permissions = self._role_permissions.list_active_permissions(
                role_id=role.id,
            )

            for role_permission in role_permissions:
                # -------------------------------------------------------------
                # Tenant isolation
                # -------------------------------------------------------------

                if role_permission.tenant_id != tenant_id:
                    continue

                # -------------------------------------------------------------
                # Role permission lifecycle
                # -------------------------------------------------------------

                if not role_permission.is_enabled:
                    continue

                if role_permission.deleted_at is not None:
                    continue

                if role_permission.effective_from is not None and role_permission.effective_from > now:
                    continue

                if role_permission.effective_until is not None and role_permission.effective_until < now:
                    continue

                # -------------------------------------------------------------
                # Resolve permission
                # -------------------------------------------------------------

                permission = self._permissions.get_by_id(
                    role_permission.permission_id,
                )

                if permission is None:
                    continue

                if permission.deleted_at is not None:
                    continue

                if not permission.is_active:
                    continue

                normalized_permission_code = permission.code.strip().upper()

                permission_codes.add(
                    normalized_permission_code,
                )

        return sorted(permission_codes)
