"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_authenticate_user_use_case.py

Description:
    Unit tests for AuthenticateUserUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.account_locked_exception import (
    AccountLockedException,
)
from qwos.application.common.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from qwos.application.identity.commands.authenticate_user_command import (
    AuthenticateUserCommand,
)
from qwos.application.identity.use_cases.authenticate_user_use_case import (
    AuthenticateUserUseCase,
)
from qwos.domains.identity.enums.account_status import AccountStatus


class FakeUserRepository:
    def __init__(self, user: object | None = None) -> None:
        self.user = user
        self.saved_user: object | None = None

    def get_by_email(self, email: str) -> object | None:
        return self.user

    def save(self, user: object) -> None:
        self.saved_user = user


class FakeSessionRepository:
    def __init__(self) -> None:
        self.saved_session: object | None = None

    def save(self, session: object) -> None:
        self.saved_session = session


class FakeSessionTokenRepository:
    def __init__(self) -> None:
        self.saved_token: object | None = None

    def save(self, token: object) -> None:
        self.saved_token = token


class FakePasswordHasher:
    def __init__(self, valid: bool = True) -> None:
        self.valid = valid
        self.verified_password: str | None = None
        self.verified_hash: str | None = None

    def verify(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        self.verified_password = plain_password
        self.verified_hash = hashed_password
        return self.valid


class FakeTokenHasher:
    def __init__(self) -> None:
        self.hashed_token: str | None = None

    def hash(self, token: str) -> str:
        self.hashed_token = token
        return f"sha256:{token}"

    def verify(
        self,
        token: str,
        token_hash: str,
    ) -> bool:
        return self.hash(token) == token_hash


class FakeTokenProvider:
    def __init__(self) -> None:
        self.access_expires_in: timedelta | None = None
        self.refresh_expires_in: timedelta | None = None

    async def create_access_token(
        self,
        *,
        subject: str,
        claims: dict[str, object],
        expires_in: timedelta,
    ) -> str:
        self.access_expires_in = expires_in
        return "access-token"

    async def create_refresh_token(
        self,
        *,
        subject: str,
        expires_in: timedelta,
    ) -> str:
        self.refresh_expires_in = expires_in
        return "refresh-token"

    async def validate_token(
        self,
        token: str,
    ) -> dict[str, object]:
        return {"sub": "test-user"}


class FakeIdGenerator:
    def __init__(self) -> None:
        self._ids = iter(
            (
                "01SESSION000000000000000001",
                "01TOKEN000000000000000001",
            )
        )

    def generate(self) -> str:
        return next(self._ids)


class FakeClock:
    def __init__(self) -> None:
        self.current_time = datetime(
            2026,
            8,
            11,
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

    def __exit__(
        self,
        exc_type,
        exc,
        tb,
    ) -> None:
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
    account_status: AccountStatus = AccountStatus.ACTIVE,
) -> SimpleNamespace:
    return SimpleNamespace(
        id="01USER000000000000000000001",
        tenant_id=tenant_id,
        email="john.doe@example.com",
        password_hash="$2b$12$test-hash",
        account_status=account_status,
        user_type="EMPLOYEE",
        last_login_at=None,
        failed_login_attempts=3,
    )


def make_use_case(
    *,
    user: object | None = None,
    password_valid: bool = True,
):
    user_repository = FakeUserRepository(user)
    session_repository = FakeSessionRepository()
    session_token_repository = FakeSessionTokenRepository()
    password_hasher = FakePasswordHasher(password_valid)
    token_provider = FakeTokenProvider()
    token_hasher = FakeTokenHasher()
    id_generator = FakeIdGenerator()
    clock = FakeClock()
    unit_of_work = FakeUnitOfWork()

    request_context = RequestContext(
        tenant_id="01HTENANT000000000000000001",
        user_id=None,
        correlation_id="correlation-id",
        request_id="request-id",
        locale="en-US",
        timezone="UTC",
        ip_address="127.0.0.1",
        user_agent="pytest",
    )

    use_case = AuthenticateUserUseCase(
        user_repository=user_repository,
        session_repository=session_repository,
        session_token_repository=session_token_repository,
        password_hasher=password_hasher,
        token_provider=token_provider,
        token_hasher=token_hasher,
        id_generator=id_generator,
        clock=clock,
        unit_of_work=unit_of_work,
        request_context=request_context,
    )

    return (
        use_case,
        user_repository,
        session_repository,
        session_token_repository,
        password_hasher,
        token_provider,
        token_hasher,
        unit_of_work,
        clock,
    )


def test_authenticate_user_successfully_creates_session_and_tokens() -> None:
    user = make_user()

    (
        use_case,
        user_repository,
        session_repository,
        session_token_repository,
        password_hasher,
        token_provider,
        token_hasher,
        unit_of_work,
        clock,
    ) = make_use_case(user=user)

    command = AuthenticateUserCommand(
        tenant_id=user.tenant_id,
        email=user.email,
        password="CorrectPassword123!",
        remember_me=False,
    )

    response = asyncio.run(use_case.execute(command))

    assert response.access_token == "access-token"
    assert response.refresh_token == "refresh-token"
    assert response.token_type == "Bearer"
    assert response.user_id == user.id
    assert response.session_id == "01SESSION000000000000000001"
    assert response.expires_at == (
        clock.now() + timedelta(minutes=15)
    )

    assert password_hasher.verified_password == "CorrectPassword123!"
    assert password_hasher.verified_hash == user.password_hash
    assert token_hasher.hashed_token == "refresh-token"

    assert token_provider.access_expires_in == timedelta(
        minutes=15
    )
    assert token_provider.refresh_expires_in == timedelta(
        days=7
    )

    assert session_repository.saved_session is not None
    assert session_token_repository.saved_token is not None

    assert user_repository.saved_user is user
    assert user.last_login_at == clock.now()
    assert user.failed_login_attempts == 0

    assert unit_of_work.entered is True
    assert unit_of_work.flushed is True
    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


def test_authenticate_user_with_remember_me_uses_long_refresh_lifetime() -> None:
    user = make_user()

    (
        use_case,
        _user_repository,
        _session_repository,
        _session_token_repository,
        _password_hasher,
        token_provider,
        _token_hasher,
        _unit_of_work,
        _clock,
    ) = make_use_case(user=user)

    command = AuthenticateUserCommand(
        tenant_id=user.tenant_id,
        email=user.email,
        password="CorrectPassword123!",
        remember_me=True,
    )

    asyncio.run(use_case.execute(command))

    assert token_provider.refresh_expires_in == timedelta(
        days=30
    )


def test_authenticate_user_rejects_unknown_user() -> None:
    use_case, *_ = make_use_case(user=None)

    command = AuthenticateUserCommand(
        tenant_id="01HTENANT000000000000000001",
        email="unknown@example.com",
        password="CorrectPassword123!",
    )

    with pytest.raises(InvalidCredentialsException):
        asyncio.run(use_case.execute(command))


def test_authenticate_user_rejects_wrong_tenant() -> None:
    user = make_user(
        tenant_id="01OTHER00000000000000000001"
    )

    use_case, *_ = make_use_case(user=user)

    command = AuthenticateUserCommand(
        tenant_id="01HTENANT000000000000000001",
        email=user.email,
        password="CorrectPassword123!",
    )

    with pytest.raises(InvalidCredentialsException):
        asyncio.run(use_case.execute(command))


def test_authenticate_user_rejects_inactive_account() -> None:
    user = make_user(
        account_status=AccountStatus.PENDING
    )

    (
        use_case,
        _user_repository,
        _session_repository,
        _session_token_repository,
        password_hasher,
        _token_provider,
        _token_hasher,
        _unit_of_work,
        _clock,
    ) = make_use_case(user=user)

    command = AuthenticateUserCommand(
        tenant_id=user.tenant_id,
        email=user.email,
        password="CorrectPassword123!",
    )

    with pytest.raises(
        ValueError,
        match="Account is not active",
    ):
        asyncio.run(use_case.execute(command))

    assert password_hasher.verified_password is None


def test_authenticate_user_rejects_locked_account() -> None:
    user = make_user(
        account_status=AccountStatus.LOCKED
    )

    (
        use_case,
        _user_repository,
        _session_repository,
        _session_token_repository,
        password_hasher,
        _token_provider,
        _token_hasher,
        _unit_of_work,
        _clock,
    ) = make_use_case(user=user)

    command = AuthenticateUserCommand(
        tenant_id=user.tenant_id,
        email=user.email,
        password="CorrectPassword123!",
    )

    with pytest.raises(AccountLockedException):
        asyncio.run(use_case.execute(command))

    assert password_hasher.verified_password is None


def test_authenticate_user_rejects_user_without_password() -> None:
    user = make_user()
    user.password_hash = None

    use_case, *_ = make_use_case(user=user)

    command = AuthenticateUserCommand(
        tenant_id=user.tenant_id,
        email=user.email,
        password="CorrectPassword123!",
    )

    with pytest.raises(InvalidCredentialsException):
        asyncio.run(use_case.execute(command))


def test_authenticate_user_rejects_invalid_password() -> None:
    user = make_user()

    (
        use_case,
        _user_repository,
        _session_repository,
        _session_token_repository,
        password_hasher,
        _token_provider,
        _token_hasher,
        _unit_of_work,
        _clock,
    ) = make_use_case(
        user=user,
        password_valid=False,
    )

    command = AuthenticateUserCommand(
        tenant_id=user.tenant_id,
        email=user.email,
        password="WrongPassword123!",
    )

    with pytest.raises(
        ValueError,
        match="Invalid email or password",
    ):
        asyncio.run(use_case.execute(command))

    assert password_hasher.verified_password == (
        "WrongPassword123!"
    )