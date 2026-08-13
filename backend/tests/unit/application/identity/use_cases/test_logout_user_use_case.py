"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_logout_user_use_case.py

Description:
    Unit tests for LogoutUserUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace

import jwt
import pytest

from qwos.application.common.context.request_context import RequestContext
from qwos.application.identity.commands.logout_user_command import (
    LogoutUserCommand,
)
from qwos.application.identity.use_cases.logout_user_use_case import (
    LogoutUserUseCase,
)


class FakeSessionTokenRepository:
    def __init__(self, token: object | None = None) -> None:
        self.token = token
        self.saved_token: object | None = None

    def get_active_by_token_hash(
        self,
        token_hash: str,
    ) -> object | None:
        return self.token

    def save(self, token: object) -> None:
        self.saved_token = token


class FakeSessionRepository:
    def __init__(self, session: object | None = None) -> None:
        self.session = session
        self.saved_session: object | None = None

    def get_by_id(self, session_id: str) -> object | None:
        return self.session

    def save(self, session: object) -> None:
        self.saved_session = session


class FakeTokenProvider:
    def __init__(
        self,
        claims: dict[str, object] | None = None,
        error: Exception | None = None,
    ) -> None:
        self.claims = claims or {
            "sub": "01USER000000000000000000001",
            "type": "refresh",
        }
        self.error = error

    async def validate_token(
        self,
        token: str,
    ) -> dict[str, object]:
        if self.error is not None:
            raise self.error

        return self.claims


class FakeTokenHasher:
    def __init__(self) -> None:
        self.hashed_token: str | None = None

    def hash(self, token: str) -> str:
        self.hashed_token = token
        return f"sha256:{token}"


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
    claims: dict[str, object] | None = None,
    token_provider_error: Exception | None = None,
):
    tenant_id = "01TENANT00000000000000000001"
    user_id = "01USER000000000000000000001"
    session_id = "01SESSION000000000000000001"

    if token is None:
        token = SimpleNamespace(
            tenant_id=tenant_id,
            session_id=session_id,
            expires_at=datetime(
                2026,
                8,
                18,
                12,
                0,
                0,
                tzinfo=timezone.utc,
            ),
            revoked_at=None,
            revoked_by=None,
            revocation_reason=None,
            is_revoked=False,
        )

        def revoke(
            *,
            revoked_at,
            revoked_by=None,
            reason=None,
        ) -> None:
            token.revoked_at = revoked_at
            token.revoked_by = revoked_by
            token.revocation_reason = reason
            token.is_revoked = True

        token.revoke = revoke

    if session is None:
        session = SimpleNamespace(
            tenant_id=tenant_id,
            user_id=user_id,
            is_active=True,
            signed_out_at=None,
            last_activity_at=None,
        )

    token_repository = FakeSessionTokenRepository(token)
    session_repository = FakeSessionRepository(session)
    token_provider = FakeTokenProvider(
        claims=claims,
        error=token_provider_error,
    )
    token_hasher = FakeTokenHasher()
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

    use_case = LogoutUserUseCase(
        session_repository=session_repository,
        session_token_repository=token_repository,
        token_provider=token_provider,
        token_hasher=token_hasher,
        clock=clock,
        unit_of_work=unit_of_work,
        request_context=request_context,
    )

    return (
        use_case,
        session,
        token,
        session_repository,
        token_repository,
        token_hasher,
        unit_of_work,
        clock,
    )


def test_logout_user_successfully_revokes_token_and_session() -> None:
    (
        use_case,
        session,
        token,
        session_repository,
        token_repository,
        token_hasher,
        unit_of_work,
        clock,
    ) = make_objects()

    command = LogoutUserCommand(
        tenant_id="01TENANT00000000000000000001",
        refresh_token="refresh-token",
    )

    response = asyncio.run(use_case.execute(command))

    assert response.success is True
    assert response.message == "User logged out successfully."

    assert token_hasher.hashed_token == "refresh-token"

    assert token.revoked_at == clock.now()
    assert token.revoked_by == "01USER000000000000000000001"
    assert token.revocation_reason == "User logout"
    assert token.is_revoked is True

    assert session.is_active is False
    assert session.signed_out_at == clock.now()
    assert session.last_activity_at == clock.now()

    assert token_repository.saved_token is token
    assert session_repository.saved_session is session

    assert unit_of_work.entered is True
    assert unit_of_work.flushed is True
    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


def test_logout_user_rejects_invalid_refresh_token() -> None:
    use_case, *_ = make_objects(
        token_provider_error=jwt.InvalidTokenError("invalid"),
    )

    command = LogoutUserCommand(
        tenant_id="01TENANT00000000000000000001",
        refresh_token="bad-token",
    )

    with pytest.raises(ValueError, match="Invalid refresh token"):
        asyncio.run(use_case.execute(command))


def test_logout_user_rejects_access_token() -> None:
    use_case, *_ = make_objects(
        claims={
            "sub": "01USER000000000000000000001",
            "type": "access",
        },
    )

    command = LogoutUserCommand(
        tenant_id="01TENANT00000000000000000001",
        refresh_token="access-token",
    )

    with pytest.raises(ValueError, match="Invalid refresh token"):
        asyncio.run(use_case.execute(command))


def test_logout_user_rejects_missing_subject() -> None:
    use_case, *_ = make_objects(
        claims={
            "type": "refresh",
        },
    )

    command = LogoutUserCommand(
        tenant_id="01TENANT00000000000000000001",
        refresh_token="refresh-token",
    )

    with pytest.raises(ValueError, match="Invalid refresh token"):
        asyncio.run(use_case.execute(command))


def test_logout_user_rejects_unknown_token() -> None:
    (
        use_case,
        _session,
        _token,
        _session_repository,
        token_repository,
        _token_hasher,
        _unit_of_work,
        _clock,
    ) = make_objects(token=None)

    token_repository.token = None

    command = LogoutUserCommand(
        tenant_id="01TENANT00000000000000000001",
        refresh_token="unknown-token",
    )

    with pytest.raises(
        ValueError,
        match="Refresh token has been revoked or is invalid",
    ):
        asyncio.run(use_case.execute(command))


def test_logout_user_rejects_expired_token() -> None:
    expired_token = SimpleNamespace(
        tenant_id="01TENANT00000000000000000001",
        session_id="01SESSION000000000000000001",
        expires_at=datetime(
            2026,
            8,
            10,
            12,
            0,
            0,
            tzinfo=timezone.utc,
        ),
        revoked_at=None,
        revoked_by=None,
        revocation_reason=None,
        is_revoked=False,
    )

    use_case, *_ = make_objects(token=expired_token)

    command = LogoutUserCommand(
        tenant_id="01TENANT00000000000000000001",
        refresh_token="refresh-token",
    )

    with pytest.raises(ValueError, match="Refresh token has expired"):
        asyncio.run(use_case.execute(command))


def test_logout_user_rejects_tenant_mismatch() -> None:
    token = SimpleNamespace(
        tenant_id="01OTHER000000000000000000001",
        session_id="01SESSION000000000000000001",
        expires_at=datetime(
            2026,
            8,
            18,
            12,
            0,
            0,
            tzinfo=timezone.utc,
        ),
        revoked_at=None,
        revoked_by=None,
        revocation_reason=None,
        is_revoked=False,
    )

    use_case, *_ = make_objects(token=token)

    command = LogoutUserCommand(
        tenant_id="01TENANT00000000000000000001",
        refresh_token="refresh-token",
    )

    with pytest.raises(ValueError, match="Invalid refresh token"):
        asyncio.run(use_case.execute(command))


def test_logout_user_rejects_session_user_mismatch() -> None:
    session = SimpleNamespace(
        tenant_id="01TENANT00000000000000000001",
        user_id="01OTHERUSER00000000000000001",
        is_active=True,
        signed_out_at=None,
        last_activity_at=None,
    )

    use_case, *_ = make_objects(session=session)

    command = LogoutUserCommand(
        tenant_id="01TENANT00000000000000000001",
        refresh_token="refresh-token",
    )

    with pytest.raises(ValueError, match="Invalid session"):
        asyncio.run(use_case.execute(command))


def test_logout_user_never_persists_raw_refresh_token() -> None:
    (
        use_case,
        _session,
        _token,
        _session_repository,
        token_repository,
        _token_hasher,
        _unit_of_work,
        _clock,
    ) = make_objects()

    command = LogoutUserCommand(
        tenant_id="01TENANT00000000000000000001",
        refresh_token="super-secret-refresh-token",
    )

    asyncio.run(use_case.execute(command))

    assert token_repository.saved_token is not None
    assert (
        getattr(token_repository.saved_token, "token_hash", None)
        != "super-secret-refresh-token"
    )