"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_request_password_reset_use_case.py

Description:
    Unit tests for RequestPasswordResetUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from qwos.application.common.context.request_context import RequestContext
from qwos.application.identity.commands.request_password_reset_command import (
    RequestPasswordResetCommand,
)
from qwos.application.identity.use_cases.request_password_reset_use_case import (
    RequestPasswordResetUseCase,
)
from qwos.domains.identity.enums.password_reset_status import PasswordResetStatus


class FakeUserRepository:
    def __init__(self, user: object | None) -> None:
        self.user = user
        self.requested_email: str | None = None

    def get_by_email(self, email: str) -> object | None:
        self.requested_email = email
        return self.user


class FakePasswordResetRepository:
    def __init__(self) -> None:
        self.saved_password_reset: object | None = None

    def save(self, password_reset: object) -> None:
        self.saved_password_reset = password_reset


class FakeIdGenerator:
    def __init__(self) -> None:
        self.generated_ids: list[str] = []

    def generate(self) -> str:
        value = f"01RESET{len(self.generated_ids) + 1:019d}"
        self.generated_ids.append(value)
        return value


class FakeSecureTokenGenerator:
    def __init__(
        self,
        token: str = "secure-reset-token",
    ) -> None:
        self.token = token
        self.called = False

    def generate(self) -> str:
        self.called = True
        return self.token


class FakeTokenHasher:
    def __init__(self) -> None:
        self.hashed_token: str | None = None

    def hash(self, token: str) -> str:
        self.hashed_token = token
        return "hashed-reset-token"

    def verify(
        self,
        token: str,
        token_hash: str,
    ) -> bool:
        return token_hash == "hashed-reset-token"


class FakeClock:
    def __init__(self) -> None:
        self.current_time = datetime(
            2026,
            8,
            12,
            10,
            0,
            tzinfo=timezone.utc,
        )

    def now(self) -> datetime:
        return self.current_time


class FakeUnitOfWork:
    def __init__(self) -> None:
        self.entered = False
        self.exited = False
        self.committed = False
        self.rolled_back = False
        self.flushed = False

    def __enter__(self) -> "FakeUnitOfWork":
        self.entered = True
        return self

    def __exit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> None:
        self.exited = True

        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True

    def flush(self) -> None:
        self.flushed = True


_NO_USER = object()


def make_objects(
    *,
    user: object = _NO_USER,
) -> tuple[
    RequestPasswordResetUseCase,
    FakeUserRepository,
    FakePasswordResetRepository,
    FakeIdGenerator,
    FakeSecureTokenGenerator,
    FakeTokenHasher,
    FakeClock,
    FakeUnitOfWork,
    RequestContext,
]:
    if user is _NO_USER:
        user = SimpleNamespace(
            id="01USER000000000000000000001",
            tenant_id="01TENANT00000000000000000001",
            email="richard@example.com",
        )

    user_repository = FakeUserRepository(user)
    password_reset_repository = FakePasswordResetRepository()
    id_generator = FakeIdGenerator()
    secure_token_generator = FakeSecureTokenGenerator()
    token_hasher = FakeTokenHasher()
    clock = FakeClock()
    unit_of_work = FakeUnitOfWork()

    request_context = RequestContext(
        tenant_id="01TENANT00000000000000000001",
        user_id=None,
        correlation_id="correlation-id",
        request_id="request-id",
        locale="en-US",
        timezone="UTC",
        ip_address="127.0.0.1",
        user_agent="pytest",
    )

    use_case = RequestPasswordResetUseCase(
        user_repository=user_repository,
        password_reset_repository=password_reset_repository,
        id_generator=id_generator,
        secure_token_generator=secure_token_generator,
        token_hasher=token_hasher,
        clock=clock,
        unit_of_work=unit_of_work,
        request_context=request_context,
    )

    return (
        use_case,
        user_repository,
        password_reset_repository,
        id_generator,
        secure_token_generator,
        token_hasher,
        clock,
        unit_of_work,
        request_context,
    )


def test_request_password_reset_creates_pending_reset() -> None:
    (
        use_case,
        _user_repository,
        password_reset_repository,
        _id_generator,
        secure_token_generator,
        token_hasher,
        clock,
        unit_of_work,
        _request_context,
    ) = make_objects()

    command = RequestPasswordResetCommand(
        email="  RICHARD@EXAMPLE.COM  ",
    )

    response = asyncio.run(use_case.execute(command))

    reset = password_reset_repository.saved_password_reset

    assert response.success is True
    assert "If an account exists" in response.message

    assert reset is not None
    assert reset.user_id == "01USER000000000000000000001"
    assert reset.tenant_id == "01TENANT00000000000000000001"
    assert reset.reset_token_hash == "hashed-reset-token"
    assert reset.password_reset_status == PasswordResetStatus.PENDING
    assert reset.requested_at == clock.now()
    assert reset.expires_at == clock.now() + timedelta(minutes=30)

    assert secure_token_generator.called is True
    assert token_hasher.hashed_token == "secure-reset-token"

    assert unit_of_work.entered is True
    assert unit_of_work.flushed is True
    assert unit_of_work.exited is True
    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


def test_request_password_reset_normalizes_email() -> None:
    (
        use_case,
        user_repository,
        *_rest,
    ) = make_objects()

    command = RequestPasswordResetCommand(
        email="  RICHARD@EXAMPLE.COM  ",
    )

    asyncio.run(use_case.execute(command))

    assert user_repository.requested_email == "richard@example.com"


def test_request_password_reset_uses_id_generator_for_reset_id() -> None:
    (
        use_case,
        _user_repository,
        password_reset_repository,
        id_generator,
        *_rest,
    ) = make_objects()

    command = RequestPasswordResetCommand(
        email="richard@example.com",
    )

    asyncio.run(use_case.execute(command))

    reset = password_reset_repository.saved_password_reset

    assert reset is not None
    assert reset.id == "01RESET0000000000000000001"
    assert id_generator.generated_ids == [
        "01RESET0000000000000000001",
    ]


def test_request_password_reset_never_persists_raw_token() -> None:
    (
        use_case,
        _user_repository,
        password_reset_repository,
        _id_generator,
        secure_token_generator,
        *_rest,
    ) = make_objects()

    command = RequestPasswordResetCommand(
        email="richard@example.com",
    )

    asyncio.run(use_case.execute(command))

    reset = password_reset_repository.saved_password_reset

    assert reset is not None
    assert secure_token_generator.token not in reset.reset_token_hash
    assert reset.reset_token_hash == "hashed-reset-token"


def test_request_password_reset_captures_request_metadata() -> None:
    (
        use_case,
        _user_repository,
        password_reset_repository,
        *_rest,
        request_context,
    ) = make_objects()

    command = RequestPasswordResetCommand(
        email="richard@example.com",
    )

    asyncio.run(use_case.execute(command))

    reset = password_reset_repository.saved_password_reset

    assert reset is not None
    assert reset.request_ip_address == request_context.ip_address
    assert reset.request_user_agent == request_context.user_agent


def test_request_password_reset_does_not_reveal_unknown_email() -> None:
    (
        use_case,
        user_repository,
        password_reset_repository,
        id_generator,
        secure_token_generator,
        token_hasher,
        _clock,
        unit_of_work,
        _request_context,
    ) = make_objects(user=None)

    command = RequestPasswordResetCommand(
        email="unknown@example.com",
    )

    response = asyncio.run(use_case.execute(command))

    assert response.success is True
    assert "If an account exists" in response.message

    assert user_repository.requested_email == "unknown@example.com"
    assert password_reset_repository.saved_password_reset is None
    assert id_generator.generated_ids == []
    assert secure_token_generator.called is False
    assert token_hasher.hashed_token is None
    assert unit_of_work.entered is False
    assert unit_of_work.committed is False


def test_request_password_reset_does_not_create_reset_for_other_tenant() -> None:
    user = SimpleNamespace(
        id="01USER000000000000000000001",
        tenant_id="01OTHER00000000000000000001",
        email="richard@example.com",
    )

    (
        use_case,
        _user_repository,
        password_reset_repository,
        id_generator,
        secure_token_generator,
        token_hasher,
        _clock,
        unit_of_work,
        _request_context,
    ) = make_objects(user=user)

    command = RequestPasswordResetCommand(
        email="richard@example.com",
    )

    response = asyncio.run(use_case.execute(command))

    assert response.success is True
    assert "If an account exists" in response.message

    assert password_reset_repository.saved_password_reset is None
    assert id_generator.generated_ids == []
    assert secure_token_generator.called is False
    assert token_hasher.hashed_token is None
    assert unit_of_work.entered is False
    assert unit_of_work.committed is False