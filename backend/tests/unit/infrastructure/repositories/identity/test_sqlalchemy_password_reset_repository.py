from datetime import datetime, timezone
from types import SimpleNamespace

from qwos.domains.identity.enums.password_reset_status import (
    PasswordResetStatus,
)
from qwos.infrastructure.repositories.identity.sqlalchemy_password_reset_repository import (
    SQLAlchemyPasswordResetRepository,
)


class FakeSession:
    def __init__(self) -> None:
        self.scalar_result = None
        self.scalars_result = []

    def scalar(self, _statement):
        return self.scalar_result

    def scalars(self, _statement):
        return SimpleNamespace(
            all=lambda: self.scalars_result,
        )


def make_repository():
    session = FakeSession()

    repository = SQLAlchemyPasswordResetRepository(
        session=session,
    )

    return repository, session


def test_get_by_token_hash_returns_matching_reset() -> None:
    repository, session = make_repository()

    expected = SimpleNamespace(
        reset_token_hash="hashed-token",
    )

    session.scalar_result = expected

    result = repository.get_by_token_hash("hashed-token")

    assert result is expected


def test_get_active_by_token_hash_returns_pending_reset() -> None:
    repository, session = make_repository()

    expected = SimpleNamespace(
        reset_token_hash="hashed-token",
        password_reset_status=PasswordResetStatus.PENDING,
        revoked_at=None,
        expires_at=datetime(
            2026,
            8,
            12,
            12,
            0,
            tzinfo=timezone.utc,
        ),
    )

    session.scalar_result = expected

    result = repository.get_active_by_token_hash("hashed-token")

    assert result is expected


def test_get_active_by_token_hash_returns_none_when_not_found() -> None:
    repository, session = make_repository()

    session.scalar_result = None

    result = repository.get_active_by_token_hash("missing-token")

    assert result is None


def test_list_by_user_id_returns_resets() -> None:
    repository, session = make_repository()

    expected = [
        SimpleNamespace(id="01RESET00000000000000000001"),
        SimpleNamespace(id="01RESET00000000000000000002"),
    ]

    session.scalars_result = expected

    result = repository.list_by_user_id(
        "01USER000000000000000000001",
    )

    assert result == expected
