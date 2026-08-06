"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

File:
    dependency_provider.py

Description:
    Base dependency provider.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .context.application_context import ApplicationContext
from .context.request_context import RequestContext


class DependencyProvider(ABC):
    """
    Supplies application dependencies.
    """

    @abstractmethod
    async def get_application_context(
        self,
    ) -> ApplicationContext:
        raise NotImplementedError

    @abstractmethod
    async def get_request_context(
        self,
    ) -> RequestContext:
        raise NotImplementedError
