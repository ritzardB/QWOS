"""
===============================================================================
Logger Interface
===============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Logger(ABC):
    """
    Logging abstraction.
    """

    @abstractmethod
    def debug(
        self,
        message: str,
    ) -> None: ...

    @abstractmethod
    def info(
        self,
        message: str,
    ) -> None: ...

    @abstractmethod
    def warning(
        self,
        message: str,
    ) -> None: ...

    @abstractmethod
    def error(
        self,
        message: str,
    ) -> None: ...

    @abstractmethod
    def exception(
        self,
        message: str,
    ) -> None: ...
