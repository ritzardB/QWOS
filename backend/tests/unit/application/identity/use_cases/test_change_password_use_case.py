"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_change_password_use_case.py

Description:
    Unit tests for ChangePasswordUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from qwos.application.common.context.request_context import RequestContext
from qwos.application.identity.commands.change_password_command import (
    ChangePasswordCommand,
)
from qwos.application.identity.use_cases.change_password_use_case import (
    ChangePasswordUseCase,
)


class FakeUserRepository:
    def __init__(self, user: object | None = None) -> None:
        self.user = user
        self.saved_user: object | None = None

    def get_by_id(self, user_id: str) -> object | None:
        if self.user is None:
            return None

        if getattr(self.user, "id", None) != user_id:
            return None

        return self.user

    def save(self, user: object) -> None:
        self.saved_user = user


class FakePasswordHasher:
    def __init__(self, current_password_valid: bool = True) -> None:
        self.current_password_valid = current_password_valid
        self.verified_password: str | None = None
        self.verified_hash: str | None = None
        self.hashed_password: str | None = None

    def verify(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        self.verified_password = plain_password
        self.verified_hash = hashed_password
        return self.current_password_valid

    def hash(
        self,
        plain_password: str,
    ) -> str:
        self.hashed_password = plain_password
        return f"bcrypt:{plain_password}"


class FakeClock:
    def __init__(self) -> None:
        self.current_time = datetime(
            2026,
            8,
            12,
            12,
            0,
            0,
            tzinfo=timezone.utc,
        )

    def now(self) -> datetime:
        return self.current_time


class FakeUnitOfWork:
    def __init__(self) -> None:
        self.entered = False
        self.committed = False
        self.rolled_back = False
        self.flushed = False

    def __enter__(self) -> "FakeUnitOfWork":
        self.entered = True
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc is None:
            self.commit()
        else:
            self.rollback()

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True

    def flush(self) -> None:
        self.flushed = True


def make_user(
    *,
    tenant_id: str = "01HTENANT000000000000000001",
) -> SimpleNamespace:
    return SimpleNamespace(
        id="01USER000000000000000000001",
        tenant_id=tenant_id,
        password_hash="old-password-hash",
        password_changed_at=None,
    )


def make_use_case(
    *,
    user: object | None = None,
    current_password_valid: bool = True,
    user_id: str | None = "01USER000000000000000000001",
    tenant_id: str = "01HTENANT000000000000000001",
):
    user_repository = FakeUserRepository(user)
    password_hasher = FakePasswordHasher(current_password_valid)
    clock = FakeClock()
    unit_of_work = FakeUnitOfWork()

    request_context = RequestContext(
        tenant_id=tenant_id,
        user_id=user_id,
        correlation_id="correlation-id",
        request_id="request-id",
        locale="en-US",
        timezone="UTC",
        ip_address="127.0.0.1",
        user_agent="pytest",
    )

    use_case = ChangePasswordUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        clock=clock,
        unit_of_work=unit_of_work,
        request_context=request_context,
    )

    return (
        use_case,
        user_repository,
        password_hasher,
        clock,
        unit_of_work,
    )


def test_change_password_successfully_updates_password() -> None:
    user = make_user()

    (
        use_case,
        user_repository,
        password_hasher,
        clock,
        unit_of_work,
    ) = make_use_case(user=user)

    command = ChangePasswordCommand(
        current_password="CurrentPassword123!",
        new_password="NewPassword456!",
    )

    response = asyncio.run(use_case.execute(command))

    assert response.success is True
    assert response.message == "Password changed successfully."

    assert password_hasher.verified_password == "CurrentPassword123!"
    assert password_hasher.verified_hash == "old-password-hash"

    assert password_hasher.hashed_password == "NewPassword456!"
    assert user.password_hash == "bcrypt:NewPassword456!"
    assert user.password_changed_at == clock.now()

    assert user_repository.saved_user is user

    assert unit_of_work.entered is True
    assert unit_of_work.flushed is True
    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


def test_change_password_requires_authentication() -> None:
    user = make_user()

    use_case, *_ = make_use_case(
        user=user,
        user_id=None,
    )

    command = ChangePasswordCommand(
        current_password="CurrentPassword123!",
        new_password="NewPassword456!",
    )

    with pytest.raises(ValueError, match="Authentication is required"):
        asyncio.run(use_case.execute(command))


def test_change_password_rejects_unknown_user() -> None:
    use_case, *_ = make_use_case(user=None)

    command = ChangePasswordCommand(
        current_password="CurrentPassword123!",
        new_password="NewPassword456!",
    )

    with pytest.raises(ValueError, match="User not found"):
        asyncio.run(use_case.execute(command))


def test_change_password_rejects_wrong_tenant() -> None:
    user = make_user(
        tenant_id="01OTHER000000000000000001",
    )

    use_case, *_ = make_use_case(user=user)

    command = ChangePasswordCommand(
        current_password="CurrentPassword123!",
        new_password="NewPassword456!",
    )

    with pytest.raises(ValueError, match="User not found"):
        asyncio.run(use_case.execute(command))


def test_change_password_rejects_user_without_password() -> None:
    user = make_user()
    user.password_hash = None

    use_case, *_ = make_use_case(user=user)

    command = ChangePasswordCommand(
        current_password="CurrentPassword123!",
        new_password="NewPassword456!",
    )

    with pytest.raises(ValueError, match="Password is not configured"):
        asyncio.run(use_case.execute(command))


def test_change_password_rejects_incorrect_current_password() -> None:
    user = make_user()

    (
        use_case,
        _user_repository,
        password_hasher,
        _clock,
        unit_of_work,
    ) = make_use_case(
        user=user,
        current_password_valid=False,
    )

    command = ChangePasswordCommand(
        current_password="WrongPassword123!",
        new_password="NewPassword456!",
    )

    with pytest.raises(ValueError, match="Current password is incorrect"):
        asyncio.run(use_case.execute(command))

    assert password_hasher.verified_password == "WrongPassword123!"
    assert password_hasher.hashed_password is None

    assert user.password_hash == "old-password-hash"
    assert user.password_changed_at is None

    assert unit_of_work.entered is False
    assert unit_of_work.flushed is False
    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is False