"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

ULID Generator

Description:
    Concrete implementation of the IdGenerator application port.

Responsibilities:
    - Generate globally unique ULID identifiers.
    - Keep the Application layer independent of the ULID library.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from ulid import ULID

from qwos.application.common.ports.id_generator import IdGenerator


class ULIDGenerator(IdGenerator):
    """
    Generates ULID identifiers.
    """

    def generate(self) -> str:
        """
        Generate a new ULID.

        Returns:
            A 26-character ULID string.
        """
        return str(ULID())