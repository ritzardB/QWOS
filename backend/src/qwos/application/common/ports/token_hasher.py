from __future__ import annotations

from typing import Protocol


class TokenHasher(Protocol):
    """
    Contract for hashing and verifying security tokens.
    """

    def hash(
        self,
        token: str,
    ) -> str:
        """
        Return a one-way hash of a token.
        """
        ...

    def verify(
        self,
        token: str,
        token_hash: str,
    ) -> bool:
        """
        Verify a raw token against its persisted hash.
        """
        ...