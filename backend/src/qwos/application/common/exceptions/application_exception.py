"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Application Exception

Description:
    Base exception for all application-layer exceptions.
===============================================================================
"""

from __future__ import annotations


class ApplicationException(Exception):
    """
    Base class for all application-layer exceptions.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
