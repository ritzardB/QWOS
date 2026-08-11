"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Secure Token Generator
===============================================================================
"""

from __future__ import annotations

import secrets

from qwos.application.common.ports.secure_token_generator import (
    SecureTokenGenerator,
)


class SecretsTokenGenerator(SecureTokenGenerator):
    """
    Cryptographically secure token generator backed by Python secrets.
    """

    def generate(self) -> str:
        """
        Generate a high-entropy URL-safe token.
        """

        return secrets.token_urlsafe(32)
