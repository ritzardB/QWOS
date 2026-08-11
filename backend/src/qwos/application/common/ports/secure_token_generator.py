"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Secure Token Generator Port
===============================================================================
"""

from __future__ import annotations

from typing import Protocol


class SecureTokenGenerator(Protocol):
    """
    Contract for generating cryptographically secure tokens.
    """

    def generate(self) -> str:
        """
        Generate a cryptographically secure random token.
        """
        ...
