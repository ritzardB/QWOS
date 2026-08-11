"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer Tests

SHA-256 Token Hasher Tests

Author:
    Richard Balabarcon
===============================================================================
"""

from qwos.infrastructure.security.sha256_token_hasher import (
    SHA256TokenHasher,
)


def test_hash_is_deterministic() -> None:
    """
    The same token should always produce the same hash.
    """

    hasher = SHA256TokenHasher()

    token = "refresh-token-example"

    first_hash = hasher.hash(token)
    second_hash = hasher.hash(token)

    assert first_hash == second_hash


def test_different_tokens_produce_different_hashes() -> None:
    """
    Different tokens should produce different hashes.
    """

    hasher = SHA256TokenHasher()

    first_hash = hasher.hash("refresh-token-one")
    second_hash = hasher.hash("refresh-token-two")

    assert first_hash != second_hash


def test_hash_is_not_the_raw_token() -> None:
    """
    The persisted hash must never equal the raw token.
    """

    hasher = SHA256TokenHasher()

    token = "refresh-token-example"
    token_hash = hasher.hash(token)

    assert token_hash != token


def test_verify_accepts_correct_token() -> None:
    """
    The original token should successfully verify against its hash.
    """

    hasher = SHA256TokenHasher()

    token = "refresh-token-example"
    token_hash = hasher.hash(token)

    assert hasher.verify(token, token_hash) is True


def test_verify_rejects_incorrect_token() -> None:
    """
    An incorrect token should fail verification.
    """

    hasher = SHA256TokenHasher()

    token = "refresh-token-example"
    token_hash = hasher.hash(token)

    assert hasher.verify(
        "different-refresh-token",
        token_hash,
    ) is False