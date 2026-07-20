"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

File:
    application_context.py

Description:
    Provides application-wide dependencies shared by use cases.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from qwos.use_cases.common.ports.cache_provider import CacheProvider
from qwos.use_cases.common.ports.clock import Clock
from qwos.use_cases.common.ports.email_sender import EmailSender
from qwos.use_cases.common.ports.event_publisher import EventPublisher
from qwos.use_cases.common.ports.logger import Logger
from qwos.use_cases.common.ports.notification_sender import (
    NotificationSender,
)
from qwos.use_cases.common.ports.password_hasher import PasswordHasher
from qwos.use_cases.common.ports.token_provider import TokenProvider


@dataclass(slots=True)
class ApplicationContext:
    """
    Shared application services.
    """

    logger: Logger

    clock: Clock

    token_provider: TokenProvider

    password_hasher: PasswordHasher

    cache_provider: CacheProvider

    email_sender: EmailSender

    notification_sender: NotificationSender

    event_publisher: EventPublisher
