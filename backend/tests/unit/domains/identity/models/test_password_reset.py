from datetime import datetime, timezone

from qwos.domains.identity.enums.password_reset_status import (
    PasswordResetStatus,
)
from qwos.domains.identity.models.password_reset import PasswordReset


def make_password_reset() -> PasswordReset:
    requested_at = datetime(2026, 8, 12, 10, 0, tzinfo=timezone.utc)
    expires_at = datetime(2026, 8, 12, 11, 0, tzinfo=timezone.utc)

    return PasswordReset.create(
        id="01RESET00000000000000000001",
        tenant_id="01TENANT00000000000000000001",
        user_id="01USER000000000000000000001",
        reset_token_hash="hashed-reset-token",
        requested_at=requested_at,
        expires_at=expires_at,
        request_ip_address="127.0.0.1",
        request_user_agent="pytest",
        created_by="01USER000000000000000000001",
    )


def test_password_reset_defaults_to_pending() -> None:
    reset = make_password_reset()

    assert reset.password_reset_status == PasswordResetStatus.PENDING
    assert reset.is_pending is True
    assert reset.is_used is False
    assert reset.is_expired is False
    assert reset.is_revoked is False


def test_password_reset_factory_persists_hash_not_raw_token() -> None:
    reset = make_password_reset()

    assert reset.reset_token_hash == "hashed-reset-token"
    assert reset.reset_token_hash != "raw-reset-token"


def test_password_reset_factory_sets_fields() -> None:
    reset = make_password_reset()

    assert reset.id == "01RESET00000000000000000001"
    assert reset.tenant_id == "01TENANT00000000000000000001"
    assert reset.user_id == "01USER000000000000000000001"
    assert reset.request_ip_address == "127.0.0.1"
    assert reset.request_user_agent == "pytest"


def test_password_reset_mark_used() -> None:
    reset = make_password_reset()

    used_at = datetime(2026, 8, 12, 10, 30, tzinfo=timezone.utc)

    reset.mark_used(used_at=used_at)

    assert reset.used_at == used_at
    assert reset.password_reset_status == PasswordResetStatus.USED
    assert reset.is_used is True
    assert reset.is_pending is False


def test_password_reset_mark_expired() -> None:
    reset = make_password_reset()

    reset.mark_expired()

    assert reset.password_reset_status == PasswordResetStatus.EXPIRED
    assert reset.is_expired is True
    assert reset.is_pending is False


def test_password_reset_revoke() -> None:
    reset = make_password_reset()

    revoked_at = datetime(2026, 8, 12, 10, 45, tzinfo=timezone.utc)

    reset.revoke(revoked_at=revoked_at)

    assert reset.revoked_at == revoked_at
    assert reset.password_reset_status == PasswordResetStatus.REVOKED
    assert reset.is_revoked is True
    assert reset.is_pending is False
