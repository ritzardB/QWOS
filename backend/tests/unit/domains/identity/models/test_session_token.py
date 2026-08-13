"""
Tests for the QWOS SessionToken model.
"""

from datetime import datetime, timezone

from qwos.domains.identity.models.session_token import SessionToken


def test_session_token_create() -> None:
    expires_at = datetime(
        2030,
        1,
        1,
        tzinfo=timezone.utc,
    )

    token = SessionToken.create(
        id="01JSESSIONTOKEN000000000000",
        tenant_id="01JTENANT00000000000000000",
        session_id="01JSESSION0000000000000000",
        token_hash="hashed-refresh-token",
        expires_at=expires_at,
    )

    assert token.id == "01JSESSIONTOKEN000000000000"
    assert token.tenant_id == "01JTENANT00000000000000000"
    assert token.session_id == "01JSESSION0000000000000000"
    assert token.token_hash == "hashed-refresh-token"
    assert token.token_type == "REFRESH"
    assert token.expires_at == expires_at
    assert token.revoked_at is None
    assert token.is_revoked is False


def test_session_token_mark_used() -> None:
    expires_at = datetime(
        2030,
        1,
        1,
        tzinfo=timezone.utc,
    )

    used_at = datetime(
        2029,
        1,
        1,
        tzinfo=timezone.utc,
    )

    token = SessionToken.create(
        id="01JSESSIONTOKEN000000000001",
        tenant_id="01JTENANT00000000000000000",
        session_id="01JSESSION0000000000000000",
        token_hash="hashed-refresh-token",
        expires_at=expires_at,
    )

    token.mark_used(used_at=used_at)

    assert token.last_used_at == used_at


def test_session_token_revoke() -> None:
    expires_at = datetime(
        2030,
        1,
        1,
        tzinfo=timezone.utc,
    )

    revoked_at = datetime(
        2029,
        1,
        1,
        tzinfo=timezone.utc,
    )

    token = SessionToken.create(
        id="01JSESSIONTOKEN000000000002",
        tenant_id="01JTENANT00000000000000000",
        session_id="01JSESSION0000000000000000",
        token_hash="hashed-refresh-token",
        expires_at=expires_at,
    )

    token.revoke(
        revoked_at=revoked_at,
        revoked_by="01JADMIN00000000000000000",
        reason="User logout",
    )

    assert token.revoked_at == revoked_at
    assert token.revoked_by == "01JADMIN00000000000000000"
    assert token.revocation_reason == "User logout"
    assert token.is_revoked is True
