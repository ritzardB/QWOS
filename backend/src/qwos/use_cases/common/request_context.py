"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

File:
    request_context.py

Description:
    Represents information associated with the current request.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RequestContext:
    """
    Information about the current request.

    This object is passed to every use case.
    """

    tenant_id: str

    user_id: str | None

    correlation_id: str

    request_id: str

    locale: str = "en-US"

    timezone: str = "UTC"

    ip_address: str | None = None

    user_agent: str | None = None
