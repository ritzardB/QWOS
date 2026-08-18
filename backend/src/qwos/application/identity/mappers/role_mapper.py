"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Identity Module

File:
    role_mapper.py

Description:
    Maps application role-assignment responses to API contracts.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.responses.identity.roles.assign_role_response import (
    AssignRoleResponse as AssignRoleApiResponse,
)
from qwos.application.identity.responses.assign_role_response import (
    AssignRoleResponse,
)


class RoleMapper:
    """
    Maps role application responses to API responses.
    """

    @staticmethod
    def to_assign_response(
        response: AssignRoleResponse,
    ) -> AssignRoleApiResponse:
        return AssignRoleApiResponse(
            id=response.id,
            user_id=response.user_id,
            role_id=response.role_id,
            is_primary=response.is_primary,
            is_enabled=response.is_enabled,
            assigned_at=response.assigned_at,
        )