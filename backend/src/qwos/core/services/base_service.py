"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Services

File:
    base_service.py

Description:
    Base class for all application services.

    Provides a common foundation for business services across all domains.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from abc import ABC


class BaseService(ABC):
    """
    Base class for all business services.

    Domain services should inherit from this class to ensure a consistent
    architecture across the application.

    This class intentionally contains very little logic. Shared capabilities
    such as logging, transactions, auditing, caching, event publishing, and
    authorization can be added here as the application evolves.
    """

    def __init__(self) -> None:
        super().__init__()
