"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

Identity Domain

File:
    test_authorization_service.py

Description:
    Unit tests for AuthorizationService RBAC decisions.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest

from qwos.domains.identity.services.authorization_service import (
    AuthorizationService,
)

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
OTHER_TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGX"

USER_ID = "01KZYTCWRF8S12V28R9NX6JXS5"

ROLE_ID = "01M08RBACROLE00000000000001"
SECONDARY_ROLE_ID = "01M08RBACROLE00000000000002"

PERMISSION_ID = "01M08RBACPERM00000000000001"
SECONDARY_PERMISSION_ID = "01M08RBACPERM00000000000002"


def make_role(
    *,
    role_id: str = ROLE_ID,
    tenant_id: str = TENANT_ID,
    is_active: bool = True,
    deleted_at: datetime | None = None,
) -> MagicMock:
    role = MagicMock()

    role.id = role_id
    role.tenant_id = tenant_id
    role.code = "HR_OFFICER"
    role.name = "HR Officer"
    role.is_active = is_active
    role.deleted_at = deleted_at

    return role


def make_user_role(
    *,
    role_id: str = ROLE_ID,
    tenant_id: str = TENANT_ID,
    is_enabled: bool = True,
    effective_from: datetime | None = None,
    effective_until: datetime | None = None,
    deleted_at: datetime | None = None,
) -> MagicMock:
    user_role = MagicMock()

    user_role.user_id = USER_ID
    user_role.role_id = role_id
    user_role.tenant_id = tenant_id
    user_role.is_enabled = is_enabled
    user_role.is_primary = True
    user_role.effective_from = effective_from
    user_role.effective_until = effective_until
    user_role.deleted_at = deleted_at

    return user_role


def make_role_permission(
    *,
    role_id: str = ROLE_ID,
    permission_id: str = PERMISSION_ID,
    tenant_id: str = TENANT_ID,
    is_enabled: bool = True,
    effective_from: datetime | None = None,
    effective_until: datetime | None = None,
    deleted_at: datetime | None = None,
) -> MagicMock:
    role_permission = MagicMock()

    role_permission.role_id = role_id
    role_permission.permission_id = permission_id
    role_permission.tenant_id = tenant_id
    role_permission.is_enabled = is_enabled
    role_permission.effective_from = effective_from
    role_permission.effective_until = effective_until
    role_permission.deleted_at = deleted_at

    return role_permission


def make_permission(
    *,
    permission_id: str = PERMISSION_ID,
    code: str = "HR_EMPLOYEE_UPDATE",
    is_active: bool = True,
    deleted_at: datetime | None = None,
) -> MagicMock:
    permission = MagicMock()

    permission.id = permission_id
    permission.code = code
    permission.name = "HR Employee Update"
    permission.module = "hr"
    permission.is_active = is_active
    permission.deleted_at = deleted_at

    return permission

@pytest.fixture
def clock() -> MagicMock:
    clock = MagicMock()
    clock.now.return_value = datetime.now(timezone.utc)
    return clock

@pytest.fixture
def repositories() -> tuple[
    MagicMock,
    MagicMock,
    MagicMock,
    MagicMock,
    MagicMock,
]:
    users = MagicMock()
    roles = MagicMock()
    permissions = MagicMock()
    user_roles = MagicMock()
    role_permissions = MagicMock()

    return (
        users,
        roles,
        permissions,
        user_roles,
        role_permissions,
    )


@pytest.fixture
def service(
    repositories: tuple[
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
    ],
    clock: MagicMock,
) -> AuthorizationService:
    (
        users,
        roles,
        permissions,
        user_roles,
        role_permissions,
    ) = repositories

    return AuthorizationService(
        users=users,
        roles=roles,
        permissions=permissions,
        user_roles=user_roles,
        role_permissions=role_permissions,
        clock=clock,
    )


@pytest.mark.anyio
async def test_has_permission_returns_true_for_active_role_and_permission(
    service: AuthorizationService,
    repositories: tuple[
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
    ],
) -> None:
    (
        _users,
        roles,
        permissions,
        user_roles,
        role_permissions,
    ) = repositories

    user_role = make_user_role()
    role = make_role()
    role_permission = make_role_permission()
    permission = make_permission()

    user_roles.list_active_roles.return_value = [
        user_role,
    ]

    roles.get_by_id.return_value = role

    role_permissions.list_active_permissions.return_value = [
        role_permission,
    ]

    permissions.get_by_id.return_value = permission

    result = await service.has_permission(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        permission_code="HR_EMPLOYEE_UPDATE",
    )

    assert result is True


@pytest.mark.anyio
async def test_has_permission_returns_true_when_secondary_role_grants_permission(
    service: AuthorizationService,
    repositories: tuple[
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
    ],
) -> None:
    (
        _users,
        roles,
        permissions,
        user_roles,
        role_permissions,
    ) = repositories

    primary_user_role = make_user_role(
        role_id=ROLE_ID,
    )

    secondary_user_role = make_user_role(
        role_id=SECONDARY_ROLE_ID,
    )

    primary_role = make_role(
        role_id=ROLE_ID,
    )

    secondary_role = make_role(
        role_id=SECONDARY_ROLE_ID,
        tenant_id=TENANT_ID,
    )

    secondary_role_permission = make_role_permission(
        role_id=SECONDARY_ROLE_ID,
        permission_id=SECONDARY_PERMISSION_ID,
    )

    permission = make_permission(
        permission_id=SECONDARY_PERMISSION_ID,
        code="HR_IMMIGRATION_UPDATE",
    )

    user_roles.list_active_roles.return_value = [
        primary_user_role,
        secondary_user_role,
    ]

    roles.get_by_id.side_effect = [
        primary_role,
        secondary_role,
    ]

    role_permissions.list_active_permissions.side_effect = [
        [],
        [secondary_role_permission],
    ]

    permissions.get_by_id.return_value = permission

    result = await service.has_permission(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        permission_code="HR_IMMIGRATION_UPDATE",
    )

    assert result is True


@pytest.mark.anyio
async def test_has_permission_returns_false_when_role_is_disabled(
    service: AuthorizationService,
    repositories: tuple[
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
    ],
) -> None:
    (
        _users,
        roles,
        _permissions,
        user_roles,
        _role_permissions,
    ) = repositories

    user_roles.list_active_roles.return_value = [
        make_user_role(
            is_enabled=False,
        ),
    ]

    result = await service.has_permission(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        permission_code="HR_EMPLOYEE_UPDATE",
    )

    assert result is False


@pytest.mark.anyio
async def test_has_permission_returns_false_for_future_role(
    service: AuthorizationService,
    repositories: tuple[
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
    ],
) -> None:
    (
        _users,
        roles,
        _permissions,
        user_roles,
        _role_permissions,
    ) = repositories

    future = datetime.now(timezone.utc) + timedelta(days=1)

    user_roles.list_active_roles.return_value = [
        make_user_role(
            effective_from=future,
        ),
    ]

    result = await service.has_permission(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        permission_code="HR_EMPLOYEE_UPDATE",
    )

    assert result is False


@pytest.mark.anyio
async def test_has_permission_returns_false_for_expired_role(
    service: AuthorizationService,
    repositories: tuple[
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
    ],
) -> None:
    (
        _users,
        roles,
        _permissions,
        user_roles,
        _role_permissions,
    ) = repositories

    expired = datetime.now(timezone.utc) - timedelta(days=1)

    user_roles.list_active_roles.return_value = [
        make_user_role(
            effective_until=expired,
        ),
    ]

    result = await service.has_permission(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        permission_code="HR_EMPLOYEE_UPDATE",
    )

    assert result is False


@pytest.mark.anyio
async def test_has_permission_returns_false_when_permission_is_disabled(
    service: AuthorizationService,
    repositories: tuple[
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
    ],
) -> None:
    (
        _users,
        roles,
        permissions,
        user_roles,
        role_permissions,
    ) = repositories

    user_roles.list_active_roles.return_value = [
        make_user_role(),
    ]

    roles.get_by_id.return_value = make_role()

    role_permissions.list_active_permissions.return_value = [
        make_role_permission(),
    ]

    permissions.get_by_id.return_value = make_permission(
        is_active=False,
    )

    result = await service.has_permission(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        permission_code="HR_EMPLOYEE_UPDATE",
    )

    assert result is False


@pytest.mark.anyio
async def test_has_permission_returns_false_when_permission_is_future_dated(
    service: AuthorizationService,
    repositories: tuple[
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
    ],
) -> None:
    (
        _users,
        roles,
        permissions,
        user_roles,
        role_permissions,
    ) = repositories

    user_roles.list_active_roles.return_value = [
        make_user_role(),
    ]

    roles.get_by_id.return_value = make_role()

    future = datetime.now(timezone.utc) + timedelta(days=1)

    role_permissions.list_active_permissions.return_value = [
        make_role_permission(
            effective_from=future,
        ),
    ]

    permissions.get_by_id.return_value = make_permission()

    result = await service.has_permission(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        permission_code="HR_EMPLOYEE_UPDATE",
    )

    assert result is False


@pytest.mark.anyio
async def test_has_permission_returns_false_when_permission_is_expired(
    service: AuthorizationService,
    repositories: tuple[
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
    ],
) -> None:
    (
        _users,
        roles,
        permissions,
        user_roles,
        role_permissions,
    ) = repositories

    user_roles.list_active_roles.return_value = [
        make_user_role(),
    ]

    roles.get_by_id.return_value = make_role()

    expired = datetime.now(timezone.utc) - timedelta(days=1)

    role_permissions.list_active_permissions.return_value = [
        make_role_permission(
            effective_until=expired,
        ),
    ]

    permissions.get_by_id.return_value = make_permission()

    result = await service.has_permission(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        permission_code="HR_EMPLOYEE_UPDATE",
    )

    assert result is False


@pytest.mark.anyio
async def test_has_permission_returns_false_for_wrong_tenant(
    service: AuthorizationService,
    repositories: tuple[
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
    ],
) -> None:
    (
        _users,
        roles,
        _permissions,
        user_roles,
        _role_permissions,
    ) = repositories

    user_roles.list_active_roles.return_value = [
        make_user_role(
            tenant_id=OTHER_TENANT_ID,
        ),
    ]

    result = await service.has_permission(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        permission_code="HR_EMPLOYEE_UPDATE",
    )

    assert result is False


@pytest.mark.anyio
async def test_has_permission_normalizes_permission_code(
    service: AuthorizationService,
    repositories: tuple[
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
    ],
) -> None:
    (
        _users,
        roles,
        permissions,
        user_roles,
        role_permissions,
    ) = repositories

    user_roles.list_active_roles.return_value = [
        make_user_role(),
    ]

    roles.get_by_id.return_value = make_role()

    role_permissions.list_active_permissions.return_value = [
        make_role_permission(),
    ]

    permissions.get_by_id.return_value = make_permission(
        code="HR_EMPLOYEE_UPDATE",
    )

    result = await service.has_permission(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        permission_code=" hr_employee_update ",
    )

    assert result is True


@pytest.mark.anyio
async def test_get_effective_permissions_returns_unique_sorted_codes(
    service: AuthorizationService,
    repositories: tuple[
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
        MagicMock,
    ],
) -> None:
    (
        _users,
        roles,
        permissions,
        user_roles,
        role_permissions,
    ) = repositories

    user_roles.list_active_roles.return_value = [
        make_user_role(
            role_id=ROLE_ID,
        ),
        make_user_role(
            role_id=SECONDARY_ROLE_ID,
        ),
    ]

    roles.get_by_id.side_effect = [
        make_role(
            role_id=ROLE_ID,
        ),
        make_role(
            role_id=SECONDARY_ROLE_ID,
        ),
    ]

    role_permissions.list_active_permissions.side_effect = [
        [
            make_role_permission(
                role_id=ROLE_ID,
                permission_id=PERMISSION_ID,
            ),
        ],
        [
            make_role_permission(
                role_id=SECONDARY_ROLE_ID,
                permission_id=SECONDARY_PERMISSION_ID,
            ),
            make_role_permission(
                role_id=SECONDARY_ROLE_ID,
                permission_id=PERMISSION_ID,
            ),
        ],
    ]

    permissions.get_by_id.side_effect = [
        make_permission(
            permission_id=PERMISSION_ID,
            code="HR_EMPLOYEE_UPDATE",
        ),
        make_permission(
            permission_id=SECONDARY_PERMISSION_ID,
            code="HR_IMMIGRATION_UPDATE",
        ),
        make_permission(
            permission_id=PERMISSION_ID,
            code="HR_EMPLOYEE_UPDATE",
        ),
    ]

    result = await service.get_effective_permissions(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
    )

    assert result == [
        "HR_EMPLOYEE_UPDATE",
        "HR_IMMIGRATION_UPDATE",
    ]