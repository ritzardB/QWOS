"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Common Dependency Providers

Description:
    Provides shared application dependencies used across all modules.

Responsibilities:
    - Provide Clock implementation
    - Provide IdGenerator implementation
    - Provide PasswordHasher implementation
    - Provide UnitOfWork implementation
    - Provide RequestContext

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from uuid import uuid4

from fastapi import Depends
from sqlalchemy.orm import Session

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.clock import Clock
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.application.common.ports.password_hasher import PasswordHasher
from qwos.application.common.ports.token_provider import TokenProvider
from qwos.core.database.session import get_session
from qwos.infrastructure.repositories.sqlalchemy_unit_of_work import (
    SQLAlchemyUnitOfWork,
)
from qwos.infrastructure.security.bcrypt_password_hasher import (
    BCryptPasswordHasher,
)
from qwos.infrastructure.system.system_clock import SystemClock
from qwos.infrastructure.system.ulid_generator import ULIDGenerator

# -------------------------------------------------------------------------
# Infrastructure Providers
# -------------------------------------------------------------------------


def get_clock() -> Clock:
    """
    Return the application clock.
    """
    return SystemClock()


def get_id_generator() -> IdGenerator:
    """
    Return the application's ID generator.
    """
    return ULIDGenerator()


def get_password_hasher() -> PasswordHasher:
    """
    Return the application's password hasher.
    """
    return BCryptPasswordHasher()

def get_token_provider() -> TokenProvider:
    """
    Return the application's JWT token provider.
    """
    from qwos.infrastructure.security.jwt_token_provider import (
        JWTTokenProvider,
    )

    return JWTTokenProvider()

# -------------------------------------------------------------------------
# Persistence Providers
# -------------------------------------------------------------------------


def get_unit_of_work(
    session: Session = Depends(get_session),
) -> UnitOfWork:
    """
    Return the Unit of Work.
    """
    return SQLAlchemyUnitOfWork(session)


# -------------------------------------------------------------------------
# Context Providers
# -------------------------------------------------------------------------


def get_request_context() -> RequestContext:
    """
    Return the current request context.

    TODO:
        Populate tenant_id, user_id, correlation_id and locale
        from authentication middleware.
    """
    request_id = str(uuid4())

    return RequestContext(
        tenant_id="default",
        user_id=None,
        correlation_id=request_id,
        request_id=request_id,
        locale="en-US",
        timezone="UTC",
        ip_address=None,
        user_agent=None,
    )