"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_refresh_access_token_use_case.py

Description:
    Unit tests for RefreshAccessTokenUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import jwt
import pytest

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.account_locked_exception import (
    AccountLockedException,
)
from qwos.application.common.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from qwos.application.identity.commands.refresh_access_token_command import (
    RefreshAccessTokenCommand,
)
from qwos.application.identity.use_cases.refresh_access_token_use_case import (
    RefreshAccessTokenUseCase,
)
from qwos.domains.identity.enums.account_status import AccountStatus


class FakeUserRepository:
    def __init__(self, user: object | None) -> None:
        self.user = user

    def get_by_id(self, user_id: str) -> object | None:
        return self.user

    def save(self, user: object) -> None:
        pass


class FakeSessionRepository:
    def __init__(self, session: object | None) -> None:
        self.session = session
        self.saved_session: object | None = None

    def get_active_by_id(self, session_id: str) -> object | None:
        return self.session

    def save(self, session: object) -> None:
        self.saved_session = session


class FakeSessionTokenRepository:
    def __init__(self, token: object | None) -> None:
        self.token = token
        self.saved_tokens: list[object] = []

    def get_active_by_token_hash(
        self,
        token_hash: str,
    ) -> object | None:
        if self.token is None:
            return None

        if self.token.token_hash != token_hash:
            return None

        if self.token.is_revoked:
            return None

        return self.token

    def save(self, token: object) -> None:
        self.saved_tokens.append(token)


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
        return "new-access-token"

    async def create_refresh_token(
        self,
        *,
        subject: str,
        expires_in: timedelta,
    ) -> str:
        self.refresh_expires_in = expires_in
        return "new-refresh-token"

    async def validate_token(
        self,
        token: str,
    ) -> dict[str, object]:
        return {
            "sub": "01USER000000000000000000001",
            "type": "refresh",
        }


class InvalidTokenProvider(FakeTokenProvider):
    async def validate_token(
        self,
        token: str,
    ) -> dict[str, object]:
        raise jwt.InvalidTokenError("invalid token")


class AccessTokenProvider(FakeTokenProvider):
    async def validate_token(
        self,
        token: str,
    ) -> dict[str, object]:
        return {
            "sub": "01USER000000000000000000001",
            "type": "access",
        }


class FakeTokenHasher:
    def __init__(self) -> None:
        self.hashed_tokens: list[str] = []

    def hash(self, token: str) -> str:
        self.hashed_tokens.append(token)
        return f"hash:{token}"

    def verify(self, token: str, token_hash: str) -> bool:
        return self.hash(token) == token_hash


class FakeIdGenerator:
    def __init__(self) -> None:
        self._ids = iter(
            (
                "01NEW_TOKEN00000000000000001",
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


def make_objects(
    *,
    token: object | None = None,
    session: object | None = None,
    user: object | None = None,
    token_provider: object | None = None,
):
    clock = FakeClock()

    user = user or SimpleNamespace(
        id="01USER000000000000000000001",
        tenant_id="01TENANT00000000000000000001",
        user_type="EMPLOYEE",
        account_status=AccountStatus.ACTIVE,
    )

    session = session or SimpleNamespace(
        id="01SESSION000000000000000001",
        tenant_id=user.tenant_id,
        user_id=user.id,
        expires_at=clock.now() + timedelta(days=7),
        last_activity_at=clock.now(),
    )

    token = token or SimpleNamespace(
        id="01TOKEN00000000000000000001",
        tenant_id=user.tenant_id,
        session_id=session.id,
        token_hash="hash:refresh-token",
        expires_at=clock.now() + timedelta(days=7),
        revoked_at=None,
        revoked_by=None,
        revocation_reason=None,
        last_used_at=None,
        is_revoked=False,
    )


    def revoke(
        *,
        revoked_at,
        revoked_by=None,
        reason=None,
    ):
        token.revoked_at = revoked_at
        token.revoked_by = revoked_by
        token.revocation_reason = reason

    def mark_used(*, used_at):
        token.last_used_at = used_at

    token.revoke = revoke
    token.mark_used = mark_used

    user_repository = FakeUserRepository(user)
    session_repository = FakeSessionRepository(session)
    token_repository = FakeSessionTokenRepository(token)
    token_provider = token_provider or FakeTokenProvider()
    token_hasher = FakeTokenHasher()
    id_generator = FakeIdGenerator()
    unit_of_work = FakeUnitOfWork()

    request_context = RequestContext(
        tenant_id=user.tenant_id,
        user_id=user.id,
        correlation_id="correlation-id",
        request_id="request-id",
        locale="en-US",
        timezone="UTC",
        ip_address="127.0.0.1",
        user_agent="pytest",
    )

    use_case = RefreshAccessTokenUseCase(
        user_repository=user_repository,
        session_repository=session_repository,
        session_token_repository=token_repository,
        token_provider=token_provider,
        token_hasher=token_hasher,
        id_generator=id_generator,
        clock=clock,
        unit_of_work=unit_of_work,
        request_context=request_context,
    )

    return (
        use_case,
        user,
        session,
        token,
        user_repository,
        session_repository,
        token_repository,
        token_provider,
        unit_of_work,
        clock,
    )


def test_refresh_token_successfully_rotates_tokens() -> None:
    (
        use_case,
        user,
        session,
        token,
        _user_repository,
        session_repository,
        token_repository,
        token_provider,
        unit_of_work,
        clock,
    ) = make_objects()

    command = RefreshAccessTokenCommand(
        refresh_token="refresh-token",
    )

    response = asyncio.run(use_case.execute(command))

    assert response.access_token == "new-access-token"
    assert response.refresh_token == "new-refresh-token"
    assert response.token_type == "Bearer"
    assert response.user_id == user.id
    assert response.session_id == session.id
    assert response.expires_at == clock.now() + timedelta(minutes=15)

    assert token.revoked_at == clock.now()
    assert token.revoked_by == user.id
    assert token.revocation_reason == "ROTATED"
    assert token.last_used_at == clock.now()

    assert len(token_repository.saved_tokens) == 2
    assert token_repository.saved_tokens[0] is token

    new_token = token_repository.saved_tokens[1]

    assert new_token.session_id == session.id
    assert new_token.tenant_id == user.tenant_id
    assert new_token.rotated_from_token_id == token.id
    assert new_token.token_hash == "hash:new-refresh-token"
    assert new_token.issued_at == clock.now()
    assert new_token.expires_at == session.expires_at

    assert session_repository.saved_session is session
    assert session.last_activity_at == clock.now()

    assert token_provider.access_expires_in == timedelta(minutes=15)
    assert token_provider.refresh_expires_in == timedelta(days=7)

    assert unit_of_work.entered is True
    assert unit_of_work.flushed is True
    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


def test_refresh_token_rejects_invalid_jwt() -> None:
    provider = InvalidTokenProvider()

    use_case, *_ = make_objects(token_provider=provider)

    command = RefreshAccessTokenCommand(
        refresh_token="invalid-token",
    )

    with pytest.raises(InvalidCredentialsException):
        asyncio.run(use_case.execute(command))


def test_refresh_token_rejects_access_token() -> None:
    provider = AccessTokenProvider()

    use_case, *_ = make_objects(token_provider=provider)

    command = RefreshAccessTokenCommand(
        refresh_token="access-token",
    )

    with pytest.raises(InvalidCredentialsException):
        asyncio.run(use_case.execute(command))


def test_refresh_token_rejects_missing_persisted_token() -> None:
    use_case, *_ = make_objects(token=None)

    # Force the repository lookup to return nothing.
    use_case._session_token_repository.token = None

    command = RefreshAccessTokenCommand(
        refresh_token="refresh-token",
    )

    with pytest.raises(InvalidCredentialsException):
        asyncio.run(use_case.execute(command))


def test_refresh_token_rejects_expired_token() -> None:
    clock = FakeClock()

    expired_token = SimpleNamespace(
        id="01TOKEN00000000000000000001",
        tenant_id="01TENANT00000000000000000001",
        session_id="01SESSION000000000000000001",
        token_hash="hash:refresh-token",
        expires_at=clock.now() - timedelta(seconds=1),
        revoked_at=None,
        revoked_by=None,
        revocation_reason=None,
        last_used_at=None,
        is_revoked=False,
    )

    use_case, *_ = make_objects(token=expired_token)

    command = RefreshAccessTokenCommand(
        refresh_token="refresh-token",
    )

    with pytest.raises(InvalidCredentialsException):
        asyncio.run(use_case.execute(command))


def test_refresh_token_rejects_locked_account() -> None:
    user = SimpleNamespace(
        id="01USER000000000000000000001",
        tenant_id="01TENANT00000000000000000001",
        user_type="EMPLOYEE",
        account_status=AccountStatus.LOCKED,
    )

    use_case, *_ = make_objects(user=user)

    command = RefreshAccessTokenCommand(
        refresh_token="refresh-token",
    )

    with pytest.raises(AccountLockedException):
        asyncio.run(use_case.execute(command))