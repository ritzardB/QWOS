"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

Identity Module

File:
    test_assign_role_use_case.py

Description:
    Unit tests for AssignRoleUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.duplicate_resource_exception import (
    DuplicateResourceException,
)
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.identity.commands.assign_role_command import (
    AssignRoleCommand,
)
from qwos.application.identity.use_cases.assign_role_use_case import (
    AssignRoleUseCase,
)

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
USER_ID = "01KZYTCWRF8S12V28R9NX6JXS5"
ROLE_ID = "01M0ARWRFEMQE2T0D9Y2N45GAY"

ASSIGNING_USER_ID = "01KZYTCWRF8S12V28R9NX6JXS5"

TEST_NOW = datetime(
    2026,
    8,
    18,
    16,
    0,
    tzinfo=UTC,
)

GENERATED_USER_ROLE_ID = "01M0AS075A6E3YEACZC720B2Q0"


def make_service() -> tuple[
    AssignRoleUseCase,
    MagicMock,
    MagicMock,
    MagicMock,
    MagicMock,
    MagicMock,
    MagicMock,
]:
    user_repository = MagicMock()
    role_repository = MagicMock()
    user_role_repository = MagicMock()
    id_generator = MagicMock()
    clock = MagicMock()
    unit_of_work = MagicMock()
    request_context = MagicMock(spec=RequestContext)

    request_context.tenant_id = TENANT_ID
    request_context.user_id = ASSIGNING_USER_ID

    clock.now.return_value = TEST_NOW
    id_generator.generate.return_value = GENERATED_USER_ROLE_ID

    service = AssignRoleUseCase(
        user_repository=user_repository,
        role_repository=role_repository,
        user_role_repository=user_role_repository,
        id_generator=id_generator,
        clock=clock,
        unit_of_work=unit_of_work,
        request_context=request_context,
    )

    return (
        service,
        user_repository,
        role_repository,
        user_role_repository,
        id_generator,
        clock,
        unit_of_work,
    )


def make_user(
    *,
    tenant_id: str = TENANT_ID,
) -> MagicMock:
    user = MagicMock()
    user.id = USER_ID
    user.tenant_id = tenant_id
    return user


def make_role(
    *,
    tenant_id: str = TENANT_ID,
    is_active: bool = True,
    deleted_at: datetime | None = None,
) -> MagicMock:
    role = MagicMock()
    role.id = ROLE_ID
    role.tenant_id = tenant_id
    role.is_active = is_active
    role.deleted_at = deleted_at
    return role


def test_assign_role_creates_and_persists_user_role() -> None:
    (
        use_case,
        user_repository,
        role_repository,
        user_role_repository,
        id_generator,
        clock,
        unit_of_work,
    ) = make_service()

    user_repository.get_by_id.return_value = make_user()
    role_repository.get_by_id.return_value = make_role()
    user_role_repository.exists_assignment.return_value = False

    command = AssignRoleCommand(
        user_id=USER_ID,
        role_id=ROLE_ID,
    )

    result = __import__(
        "asyncio",
    ).run(
        use_case.execute(command),
    )

    assert result.id == GENERATED_USER_ROLE_ID
    assert result.user_id == USER_ID
    assert result.role_id == ROLE_ID
    assert result.is_primary is False
    assert result.is_enabled is True
    assert result.assigned_at == TEST_NOW

    id_generator.generate.assert_called_once()
    clock.now.assert_called_once()

    user_role_repository.save.assert_called_once()

    saved_user_role = user_role_repository.save.call_args.args[0]

    assert saved_user_role.id == GENERATED_USER_ROLE_ID
    assert saved_user_role.tenant_id == TENANT_ID
    assert saved_user_role.user_id == USER_ID
    assert saved_user_role.role_id == ROLE_ID
    assert saved_user_role.assigned_at == TEST_NOW
    assert saved_user_role.assigned_by == ASSIGNING_USER_ID
    assert saved_user_role.is_primary is False
    assert saved_user_role.is_enabled is True

    unit_of_work.flush.assert_called_once()


def test_assign_role_rejects_unknown_user() -> None:
    (
        use_case,
        user_repository,
        role_repository,
        user_role_repository,
        _id_generator,
        _clock,
        unit_of_work,
    ) = make_service()

    user_repository.get_by_id.return_value = None

    command = AssignRoleCommand(
        user_id=USER_ID,
        role_id=ROLE_ID,
    )

    with pytest.raises(ResourceNotFoundException):
        __import__("asyncio").run(
            use_case.execute(command),
        )

    role_repository.get_by_id.assert_not_called()
    user_role_repository.save.assert_not_called()
    unit_of_work.flush.assert_not_called()


def test_assign_role_rejects_user_from_another_tenant() -> None:
    (
        use_case,
        user_repository,
        role_repository,
        user_role_repository,
        _id_generator,
        _clock,
        unit_of_work,
    ) = make_service()

    user_repository.get_by_id.return_value = make_user(
        tenant_id="01KZYRPZANTQJBZYE7KS4DCRGX",
    )

    command = AssignRoleCommand(
        user_id=USER_ID,
        role_id=ROLE_ID,
    )

    with pytest.raises(ResourceNotFoundException):
        __import__("asyncio").run(
            use_case.execute(command),
        )

    role_repository.get_by_id.assert_not_called()
    user_role_repository.save.assert_not_called()
    unit_of_work.flush.assert_not_called()


def test_assign_role_rejects_unknown_role() -> None:
    (
        use_case,
        user_repository,
        role_repository,
        user_role_repository,
        _id_generator,
        _clock,
        unit_of_work,
    ) = make_service()

    user_repository.get_by_id.return_value = make_user()
    role_repository.get_by_id.return_value = None

    command = AssignRoleCommand(
        user_id=USER_ID,
        role_id=ROLE_ID,
    )

    with pytest.raises(ResourceNotFoundException):
        __import__("asyncio").run(
            use_case.execute(command),
        )

    user_role_repository.save.assert_not_called()
    unit_of_work.flush.assert_not_called()


def test_assign_role_rejects_role_from_another_tenant() -> None:
    (
        use_case,
        user_repository,
        role_repository,
        user_role_repository,
        _id_generator,
        _clock,
        unit_of_work,
    ) = make_service()

    user_repository.get_by_id.return_value = make_user()
    role_repository.get_by_id.return_value = make_role(
        tenant_id="01KZYRPZANTQJBZYE7KS4DCRGX",
    )

    command = AssignRoleCommand(
        user_id=USER_ID,
        role_id=ROLE_ID,
    )

    with pytest.raises(ResourceNotFoundException):
        __import__("asyncio").run(
            use_case.execute(command),
        )

    user_role_repository.save.assert_not_called()
    unit_of_work.flush.assert_not_called()


def test_assign_role_rejects_inactive_role() -> None:
    (
        use_case,
        user_repository,
        role_repository,
        user_role_repository,
        _id_generator,
        _clock,
        unit_of_work,
    ) = make_service()

    user_repository.get_by_id.return_value = make_user()
    role_repository.get_by_id.return_value = make_role(
        is_active=False,
    )

    command = AssignRoleCommand(
        user_id=USER_ID,
        role_id=ROLE_ID,
    )

    with pytest.raises(ResourceNotFoundException):
        __import__("asyncio").run(
            use_case.execute(command),
        )

    user_role_repository.save.assert_not_called()
    unit_of_work.flush.assert_not_called()


def test_assign_role_rejects_duplicate_assignment() -> None:
    (
        use_case,
        user_repository,
        role_repository,
        user_role_repository,
        id_generator,
        clock,
        unit_of_work,
    ) = make_service()

    user_repository.get_by_id.return_value = make_user()
    role_repository.get_by_id.return_value = make_role()
    user_role_repository.exists_assignment.return_value = True

    command = AssignRoleCommand(
        user_id=USER_ID,
        role_id=ROLE_ID,
    )

    with pytest.raises(DuplicateResourceException):
        __import__("asyncio").run(
            use_case.execute(command),
        )

    id_generator.generate.assert_not_called()
    clock.now.assert_not_called()
    user_role_repository.save.assert_not_called()
    unit_of_work.flush.assert_not_called()