from datetime import timedelta

import pytest

from qwos.infrastructure.security.jwt_token_provider import (
    JWTTokenProvider,
)


@pytest.mark.anyio
async def test_create_access_token() -> None:
    provider = JWTTokenProvider()

    token = await provider.create_access_token(
        subject="01H00000000000000000000000",
        claims={
            "tenant_id": "01H00000000000000000000001",
            "user_type": "EMPLOYEE",
        },
        expires_in=timedelta(minutes=15),
    )

    assert token
    assert isinstance(token, str)


@pytest.mark.anyio
async def test_create_refresh_token() -> None:
    provider = JWTTokenProvider()

    token = await provider.create_refresh_token(
        subject="01H00000000000000000000000",
        expires_in=timedelta(days=30),
    )

    assert token
    assert isinstance(token, str)


@pytest.mark.anyio
async def test_validate_access_token() -> None:
    provider = JWTTokenProvider()

    token = await provider.create_access_token(
        subject="01H00000000000000000000000",
        claims={
            "tenant_id": "01H00000000000000000000001",
        },
        expires_in=timedelta(minutes=15),
    )

    payload = await provider.validate_token(token)

    assert payload["sub"] == "01H00000000000000000000000"
    assert payload["type"] == "access"
    assert payload["tenant_id"] == "01H00000000000000000000001"


@pytest.mark.anyio
async def test_validate_refresh_token() -> None:
    provider = JWTTokenProvider()

    token = await provider.create_refresh_token(
        subject="01H00000000000000000000000",
        expires_in=timedelta(days=30),
    )

    payload = await provider.validate_token(token)

    assert payload["sub"] == "01H00000000000000000000000"
    assert payload["type"] == "refresh"


@pytest.mark.anyio
async def test_invalid_token_is_rejected() -> None:
    provider = JWTTokenProvider()

    with pytest.raises(Exception):
        await provider.validate_token("not-a-valid-jwt")