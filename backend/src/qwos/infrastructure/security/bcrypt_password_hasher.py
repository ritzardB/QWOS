"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

BCrypt Password Hasher
===============================================================================
"""

from __future__ import annotations

import bcrypt

from qwos.application.common.ports.password_hasher import PasswordHasher


class BCryptPasswordHasher(PasswordHasher):
    """
    BCrypt implementation of PasswordHasher.
    """

    def hash(
        self,
        plain_password: str,
    ) -> str:
        return bcrypt.hashpw(
            plain_password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

    def verify(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )