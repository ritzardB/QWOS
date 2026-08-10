"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Dependency Providers

Identity Module

Description:
    Dependency providers for the Identity module.

Responsibilities:
    - Provide repositories
    - Provide application services
    - Provide use cases
    - Compose object graph

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies import (
    get_clock,
    get_id_generator,
    get_password_hasher,
    get_request_context,
    get_unit_of_work,
)
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.clock import Clock
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.application.common.ports.password_hasher import PasswordHasher
from qwos.application.identity.use_cases.create_user_use_case import (
    CreateUserUseCase,
)
from qwos.application.identity.validators.create_user_validator import (
    CreateUserValidator,
)
from qwos.core.database.session import get_session
from qwos.domains.identity.repositories.user_profile_repository import (
    UserProfileRepository,
)
from qwos.domains.identity.repositories.user_repository import (
    UserRepository,
)
from qwos.infrastructure.repositories.identity import sqlalchemy_user_profile_repository as user_profile_repo
from qwos.infrastructure.repositories.identity.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)

# -------------------------------------------------------------------------
# Repository Providers
# -------------------------------------------------------------------------

__all__ = ["get_create_user_use_case", "get_request_context"]


def get_user_repository(
    session: Session = Depends(get_session),
) -> UserRepository:
    """
    Return User repository.
    """
    # FIX 2: Fixed the copy-paste bug to return UserRepository instead of profile repo
    return SQLAlchemyUserRepository(session)


def get_user_profile_repository(
    session: Session = Depends(get_session),
) -> UserProfileRepository:
    """
    Return UserProfile repository.
    """
    return user_profile_repo.SQLAlchemyUserProfileRepository(session)


# -------------------------------------------------------------------------
# Validator Providers
# -------------------------------------------------------------------------


def get_create_user_validator() -> CreateUserValidator:
    """
    Return CreateUserValidator.
    """
    return CreateUserValidator()


# -------------------------------------------------------------------------
# Use Case Providers
# -------------------------------------------------------------------------


def get_create_user_use_case(
    user_repository: UserRepository = Depends(
        get_user_repository,
    ),
    user_profile_repository: UserProfileRepository = Depends(
        get_user_profile_repository,
    ),
    validator: CreateUserValidator = Depends(
        get_create_user_validator,
    ),
    password_hasher: PasswordHasher = Depends(
        get_password_hasher,
    ),
    id_generator: IdGenerator = Depends(
        get_id_generator,
    ),
    clock: Clock = Depends(
        get_clock,
    ),
    unit_of_work: UnitOfWork = Depends(
        get_unit_of_work,
    ),
    request_context: RequestContext = Depends(
        get_request_context,
    ),
) -> CreateUserUseCase:
    """
    Return CreateUserUseCase.
    """

    return CreateUserUseCase(
        user_repository=user_repository,
        user_profile_repository=user_profile_repository,
        password_hasher=password_hasher,
        id_generator=id_generator,
        clock=clock,
        unit_of_work=unit_of_work,
        validator=validator,
        request_context=request_context,
    )
