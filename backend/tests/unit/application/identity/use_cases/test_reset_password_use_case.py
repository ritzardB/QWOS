"""
Tests for the ResetPasswordUseCase.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from qwos.application.common.context.request_context import RequestContext
from qwos.application.identity.commands.reset_password_command import (
    ResetPasswordCommand,
)
from qwos.application.identity.use_cases.reset_password_use_case import (
    ResetPasswordUseCase,
)
from qwos.domains.identity.enums.password_reset_status import PasswordResetStatus
from qwos.domains.identity.models.password_reset import PasswordReset


class FakeUserRepository:
    def __init__(self, user: object | None) -> None:
        self.user = user
        self.requested_user_id: str | None = None
        self.saved_user: object | None = None

    def get_by_id(self, user_id: str) -> object | None:
        self.requested_user_id = user_id
        return self.user

    def save(self, user: object) -> None:
        self.saved_user = user


class FakePasswordResetRepository:
    def __init__(self, password_reset: PasswordReset | None) -> None:
        self.password_reset = password_reset
        self.requested_token_hash: str | None = None
        self.saved_password_reset: PasswordReset | None = None

    def get_active_by_token_hash(
        self,
        token_hash: str,
    ) -> PasswordReset | None:
        self.requested_token_hash = token_hash
        return self.password_reset

    def save(self, password_reset: PasswordReset) -> None:
        self.saved_password_reset = password_reset


class FakePasswordHasher:
    def __init__(self) -> None:
        self.hashed_password: str | None = None

    def hash(self, password: str) -> str:
        self.hashed_password = password
        return "hashed-new-password"

    def verify(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        return False


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

    def flush(self) -> None:
        self.flushed = True


_NO_RESET = object()


def make_objects(
    *,
    password_reset: object = _NO_RESET,
    user: object | None = None,
) -> tuple[
    ResetPasswordUseCase,
    FakeUserRepository,
    FakePasswordResetRepository,
    FakePasswordHasher,
    FakeTokenHasher,
    FakeClock,
    FakeUnitOfWork,
    RequestContext,
]:
    clock = FakeClock()

    if password_reset is _NO_RESET:
        password_reset = PasswordReset.create(
            id="01RESET0000000000000000001",
            tenant_id="01TENANT00000000000000000001",
            user_id="01USER000000000000000000001",
            reset_token_hash="hashed-reset-token",
            requested_at=clock.now() - timedelta(minutes=5),
            expires_at=clock.now() + timedelta(minutes=25),
            request_ip_address="127.0.0.1",
            request_user_agent="pytest",
            created_by="01USER000000000000000000001",
        )

    if user is None:
        user = SimpleNamespace(
            id="01USER000000000000000000001",
            tenant_id="01TENANT00000000000000000001",
            email="richard@example.com",
            password_hash="old-password-hash",
            password_changed_at=None,
        )

    user_repository = FakeUserRepository(user)
    password_reset_repository = FakePasswordResetRepository(
        password_reset
        if isinstance(password_reset, PasswordReset)
        else None,
    )
    password_hasher = FakePasswordHasher()
    token_hasher = FakeTokenHasher()
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

    use_case = ResetPasswordUseCase(
        user_repository=user_repository,
        password_reset_repository=password_reset_repository,
        password_hasher=password_hasher,
        token_hasher=token_hasher,
        clock=clock,
        unit_of_work=unit_of_work,
        request_context=request_context,
    )

    return (
        use_case,
        user_repository,
        password_reset_repository,
        password_hasher,
        token_hasher,
        clock,
        unit_of_work,
        request_context,
    )


def make_command(
    *,
    token: str = "secure-reset-token",
    new_password: str = "NewPassword123!",
    confirm_password: str = "NewPassword123!",
) -> ResetPasswordCommand:
    return ResetPasswordCommand(
        token=token,
        new_password=new_password,
        confirm_password=confirm_password,
    )


def test_reset_password_successfully_changes_password() -> None:
    (
        use_case,
        user_repository,
        password_reset_repository,
        password_hasher,
        token_hasher,
        clock,
        unit_of_work,
        _request_context,
    ) = make_objects()

    command = make_command()

    response = asyncio.run(use_case.execute(command))

    user = user_repository.saved_user
    reset = password_reset_repository.saved_password_reset

    assert response.success is True
    assert response.message == "Password reset successfully."

    assert user is not None
    assert user.password_hash == "hashed-new-password"
    assert user.password_changed_at == clock.now()

    assert reset is not None
    assert reset.password_reset_status == PasswordResetStatus.USED
    assert reset.used_at == clock.now()

    assert token_hasher.hashed_token == "secure-reset-token"
    assert password_hasher.hashed_password == "NewPassword123!"

    assert user_repository.requested_user_id == (
        "01USER000000000000000000001"
    )
    assert password_reset_repository.requested_token_hash == (
        "hashed-reset-token"
    )

    assert unit_of_work.entered is True
    assert unit_of_work.flushed is True
    assert unit_of_work.exited is True


def test_reset_password_hashes_new_password() -> None:
    (
        use_case,
        user_repository,
        _password_reset_repository,
        password_hasher,
        _token_hasher,
        _clock,
        _unit_of_work,
        _request_context,
    ) = make_objects()

    command = make_command(
        new_password="BrandNewPassword123!",
        confirm_password="BrandNewPassword123!",
    )

    asyncio.run(use_case.execute(command))

    user = user_repository.saved_user

    assert user is not None
    assert password_hasher.hashed_password == "BrandNewPassword123!"
    assert user.password_hash == "hashed-new-password"
    assert user.password_hash != "BrandNewPassword123!"


def test_reset_password_never_persists_raw_reset_token() -> None:
    (
        use_case,
        _user_repository,
        password_reset_repository,
        _password_hasher,
        token_hasher,
        _clock,
        _unit_of_work,
        _request_context,
    ) = make_objects()

    command = make_command()

    asyncio.run(use_case.execute(command))

    reset = password_reset_repository.saved_password_reset

    assert reset is not None
    assert token_hasher.hashed_token == "secure-reset-token"
    assert reset.reset_token_hash == "hashed-reset-token"
    assert "secure-reset-token" not in reset.reset_token_hash


def test_reset_password_rejects_mismatched_passwords() -> None:
    (
        use_case,
        user_repository,
        password_reset_repository,
        password_hasher,
        token_hasher,
        _clock,
        unit_of_work,
        _request_context,
    ) = make_objects()

    command = make_command(
        new_password="NewPassword123!",
        confirm_password="DifferentPassword123!",
    )

    try:
        asyncio.run(use_case.execute(command))
        raise AssertionError("Expected ValueError")
    except ValueError as exc:
        assert str(exc) == "Passwords do not match."

    assert user_repository.saved_user is None
    assert password_reset_repository.saved_password_reset is None
    assert password_hasher.hashed_password is None
    assert token_hasher.hashed_token is None
    assert unit_of_work.entered is False


def test_reset_password_rejects_invalid_token() -> None:
    (
        use_case,
        user_repository,
        password_reset_repository,
        password_hasher,
        token_hasher,
        _clock,
        unit_of_work,
        _request_context,
    ) = make_objects(password_reset=None)

    command = make_command(token="invalid-token")

    try:
        asyncio.run(use_case.execute(command))
        raise AssertionError("Expected ValueError")
    except ValueError as exc:
        assert str(exc) == "Invalid or expired password reset token."

    assert token_hasher.hashed_token == "invalid-token"
    assert password_reset_repository.requested_token_hash == (
        "hashed-reset-token"
    )
    assert user_repository.saved_user is None
    assert password_hasher.hashed_password is None
    assert unit_of_work.entered is False


def test_reset_password_rejects_expired_token() -> None:
    (
        use_case,
        user_repository,
        password_reset_repository,
        password_hasher,
        _token_hasher,
        clock,
        unit_of_work,
        _request_context,
    ) = make_objects()

    reset = password_reset_repository.password_reset
    assert reset is not None

    reset.expires_at = clock.now() - timedelta(seconds=1)

    command = make_command()

    try:
        asyncio.run(use_case.execute(command))
        raise AssertionError("Expected ValueError")
    except ValueError as exc:
        assert str(exc) == "Invalid or expired password reset token."

    assert reset.password_reset_status == PasswordResetStatus.EXPIRED
    assert password_reset_repository.saved_password_reset is reset
    assert user_repository.saved_user is None
    assert password_hasher.hashed_password is None

    assert unit_of_work.entered is True
    assert unit_of_work.flushed is True
    assert unit_of_work.exited is True


def test_reset_password_rejects_reset_for_other_tenant() -> None:
    (
        use_case,
        user_repository,
        password_reset_repository,
        password_hasher,
        token_hasher,
        _clock,
        unit_of_work,
        _request_context,
    ) = make_objects()

    reset = password_reset_repository.password_reset
    assert reset is not None

    reset.tenant_id = "01OTHER00000000000000000001"

    command = make_command()

    try:
        asyncio.run(use_case.execute(command))
        raise AssertionError("Expected ValueError")
    except ValueError as exc:
        assert str(exc) == "Invalid or expired password reset token."

    assert token_hasher.hashed_token == "secure-reset-token"
    assert user_repository.saved_user is None
    assert password_hasher.hashed_password is None
    assert unit_of_work.entered is False


def test_reset_password_rejects_when_user_does_not_exist() -> None:
    (
        use_case,
        user_repository,
        password_reset_repository,
        password_hasher,
        _token_hasher,
        _clock,
        unit_of_work,
        _request_context,
    ) = make_objects(user=None)

    user_repository.user = None

    command = make_command()

    try:
        asyncio.run(use_case.execute(command))
        raise AssertionError("Expected ValueError")
    except ValueError as exc:
        assert str(exc) == "Invalid or expired password reset token."

    assert user_repository.requested_user_id == (
        "01USER000000000000000000001"
    )
    assert password_reset_repository.saved_password_reset is None
    assert password_hasher.hashed_password is None
    assert unit_of_work.entered is False


def test_reset_password_rejects_user_from_different_tenant() -> None:
    (
        use_case,
        user_repository,
        password_reset_repository,
        password_hasher,
        _token_hasher,
        _clock,
        unit_of_work,
        _request_context,
    ) = make_objects()

    user = user_repository.user
    assert user is not None

    user.tenant_id = "01OTHER00000000000000000001"

    command = make_command()

    try:
        asyncio.run(use_case.execute(command))
        raise AssertionError("Expected ValueError")
    except ValueError as exc:
        assert str(exc) == "Invalid or expired password reset token."

    assert user_repository.saved_user is None
    assert password_reset_repository.saved_password_reset is None
    assert password_hasher.hashed_password is None
    assert unit_of_work.entered is False


def test_reset_password_consumes_token() -> None:
    (
        use_case,
        _user_repository,
        password_reset_repository,
        _password_hasher,
        _token_hasher,
        clock,
        _unit_of_work,
        _request_context,
    ) = make_objects()

    reset = password_reset_repository.password_reset
    assert reset is not None

    asyncio.run(use_case.execute(make_command()))

    assert reset.password_reset_status == PasswordResetStatus.USED
    assert reset.used_at == clock.now()


def test_reset_password_updates_password_changed_at() -> None:
    (
        use_case,
        user_repository,
        _password_reset_repository,
        _password_hasher,
        _token_hasher,
        clock,
        _unit_of_work,
        _request_context,
    ) = make_objects()

    asyncio.run(use_case.execute(make_command()))

    user = user_repository.saved_user

    assert user is not None
    assert user.password_changed_at == clock.now()
