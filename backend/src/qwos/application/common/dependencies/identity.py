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
    get_secure_token_generator,
    get_token_hasher,
    get_token_provider,
    get_unit_of_work,
)
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.clock import Clock
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.application.common.ports.password_hasher import PasswordHasher
from qwos.application.common.ports.secure_token_generator import (
    SecureTokenGenerator,
)
from qwos.application.common.ports.token_hasher import TokenHasher
from qwos.application.common.ports.token_provider import TokenProvider
from qwos.application.identity.use_cases.authenticate_user_use_case import (
    AuthenticateUserUseCase,
)
from qwos.application.identity.use_cases.change_password_use_case import (
    ChangePasswordUseCase,
)
from qwos.application.identity.use_cases.create_user_use_case import (
    CreateUserUseCase,
)
from qwos.application.identity.use_cases.logout_user_use_case import (
    LogoutUserUseCase,
)
from qwos.application.identity.use_cases.refresh_access_token_use_case import (
    RefreshAccessTokenUseCase,
)
from qwos.application.identity.use_cases.request_password_reset_use_case import (
    RequestPasswordResetUseCase,
)
from qwos.application.identity.use_cases.reset_password_use_case import (
    ResetPasswordUseCase,
)
from qwos.application.identity.validators.create_user_validator import (
    CreateUserValidator,
)
from qwos.core.database.session import get_session
from qwos.domains.identity.repositories.password_reset_repository import (
    PasswordResetRepository,
)
from qwos.domains.identity.repositories.session_repository import (
    SessionRepository,
)
from qwos.domains.identity.repositories.session_token_repository import (
    SessionTokenRepository,
)
from qwos.domains.identity.repositories.user_profile_repository import (
    UserProfileRepository,
)
from qwos.domains.identity.repositories.user_repository import (
    UserRepository,
)
from qwos.infrastructure.repositories.identity import sqlalchemy_user_profile_repository as user_profile_repo
from qwos.infrastructure.repositories.identity.sqlalchemy_password_reset_repository import (
    SQLAlchemyPasswordResetRepository,
)
from qwos.infrastructure.repositories.identity.sqlalchemy_session_repository import (
    SQLAlchemySessionRepository,
)
from qwos.infrastructure.repositories.identity.sqlalchemy_session_token_repository import (
    SQLAlchemySessionTokenRepository,
)
from qwos.infrastructure.repositories.identity.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)

# -------------------------------------------------------------------------
# Repository Providers
# -------------------------------------------------------------------------

__all__ = [
    "get_logout_user_use_case",
    "get_authenticate_user_use_case",
    "get_create_user_use_case",
    "get_request_context",
    "get_request_password_reset_use_case",
    "get_reset_password_use_case",
    "get_change_password_use_case",
    
]

def get_user_repository(
    session: Session = Depends(get_session),
) -> UserRepository:
    """
    Return User repository.
    """
    return SQLAlchemyUserRepository(session)

def get_session_repository(
    session: Session = Depends(get_session),
) -> SessionRepository:
    """
    Return Session repository.
    """
    return SQLAlchemySessionRepository(session)


def get_session_token_repository(
    session: Session = Depends(get_session),
) -> SessionTokenRepository:
    """
    Return SessionToken repository.
    """
    return SQLAlchemySessionTokenRepository(session)

def get_user_profile_repository(
    session: Session = Depends(get_session),
) -> UserProfileRepository:
    """
    Return UserProfile repository.
    """
    return user_profile_repo.SQLAlchemyUserProfileRepository(session)

def get_password_reset_repository(
    session: Session = Depends(get_session),
) -> PasswordResetRepository:
    """
    Return PasswordReset repository.
    """
    return SQLAlchemyPasswordResetRepository(session)

# -------------------------------------------------------------------------
# Validator Providers
# -------------------------------------------------------------------------


def get_create_user_validator() -> CreateUserValidator:
    """
    Return CreateUserValidator.
    """
    return CreateUserValidator()

# -------------------------------------------------------------------------
# Authenticate Provider
# -------------------------------------------------------------------------

def get_authenticate_user_use_case(
    user_repository: UserRepository = Depends(
        get_user_repository,
    ),
    session_repository: SessionRepository = Depends(
        get_session_repository,
    ),
    session_token_repository: SessionTokenRepository = Depends(
        get_session_token_repository,
    ),
    password_hasher: PasswordHasher = Depends(
        get_password_hasher,
    ),
    token_provider: TokenProvider = Depends(
        get_token_provider,
    ),
    token_hasher: TokenHasher = Depends(
        get_token_hasher,
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
) -> AuthenticateUserUseCase:
    """
    Return AuthenticateUserUseCase.
    """

    return AuthenticateUserUseCase(
        user_repository=user_repository,
        session_repository=session_repository,
        session_token_repository=session_token_repository,
        password_hasher=password_hasher,
        token_provider=token_provider,
        token_hasher=token_hasher,
        id_generator=id_generator,
        clock=clock,
        unit_of_work=unit_of_work,
        request_context=request_context,
    )

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

def get_request_password_reset_use_case(
    user_repository: UserRepository = Depends(
        get_user_repository,
    ),
    password_reset_repository: PasswordResetRepository = Depends(
        get_password_reset_repository,
    ),
    id_generator: IdGenerator = Depends(
        get_id_generator,
    ),
    secure_token_generator: SecureTokenGenerator = Depends(
        get_secure_token_generator,
    ),
    token_hasher: TokenHasher = Depends(
        get_token_hasher,
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
) -> RequestPasswordResetUseCase:
    """
    Return RequestPasswordResetUseCase.
    """
    return RequestPasswordResetUseCase(
        user_repository=user_repository,
        password_reset_repository=password_reset_repository,
        id_generator=id_generator,
        secure_token_generator=secure_token_generator,
        token_hasher=token_hasher,
        clock=clock,
        unit_of_work=unit_of_work,
        request_context=request_context,
    )

def get_reset_password_use_case(
    user_repository: UserRepository = Depends(
        get_user_repository,
    ),
    password_reset_repository: PasswordResetRepository = Depends(
        get_password_reset_repository,
    ),
    password_hasher: PasswordHasher = Depends(
        get_password_hasher,
    ),
    token_hasher: TokenHasher = Depends(
        get_token_hasher,
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
) -> ResetPasswordUseCase:
    """
    Return ResetPasswordUseCase.
    """
    return ResetPasswordUseCase(
        user_repository=user_repository,
        password_reset_repository=password_reset_repository,
        password_hasher=password_hasher,
        token_hasher=token_hasher,
        clock=clock,
        unit_of_work=unit_of_work,
        request_context=request_context,
    )

# -------------------------------------------------------------------------
# Change Password Proividers    
# -------------------------------------------------------------------------

def get_change_password_use_case(
    user_repository: UserRepository = Depends(
        get_user_repository,
    ),
    password_hasher: PasswordHasher = Depends(
        get_password_hasher,
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
) -> ChangePasswordUseCase:
    """
    Return ChangePasswordUseCase.
    """

    return ChangePasswordUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        clock=clock,
        unit_of_work=unit_of_work,
        request_context=request_context,
    )

# -------------------------------------------------------------------------
# Logout Provider
# -------------------------------------------------------------------------

def get_logout_user_use_case(
    session_repository: SessionRepository = Depends(
        get_session_repository,
    ),
    session_token_repository: SessionTokenRepository = Depends(
        get_session_token_repository,
    ),
    token_provider: TokenProvider = Depends(
        get_token_provider,
    ),
    token_hasher: TokenHasher = Depends(
        get_token_hasher,
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
) -> LogoutUserUseCase:
    """
    Return LogoutUserUseCase.
    """

    return LogoutUserUseCase(
        session_repository=session_repository,
        session_token_repository=session_token_repository,
        token_provider=token_provider,
        token_hasher=token_hasher,
        clock=clock,
        unit_of_work=unit_of_work,
        request_context=request_context,
    )

# -------------------------------------------------------------------------
# Refresh Access Token Provider
# -------------------------------------------------------------------------

def get_refresh_access_token_use_case(
    user_repository: UserRepository = Depends(get_user_repository),
    session_repository: SessionRepository = Depends(get_session_repository),
    session_token_repository: SessionTokenRepository = Depends(
        get_session_token_repository,
    ),
    token_provider: TokenProvider = Depends(get_token_provider),
    token_hasher: TokenHasher = Depends(get_token_hasher),
    id_generator: IdGenerator = Depends(get_id_generator),
    clock: Clock = Depends(get_clock),
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    request_context: RequestContext = Depends(get_request_context),
) -> RefreshAccessTokenUseCase:
    """
    Return RefreshAccessTokenUseCase.
    """

    return RefreshAccessTokenUseCase(
        user_repository=user_repository,
        session_repository=session_repository,
        session_token_repository=session_token_repository,
        token_provider=token_provider,
        token_hasher=token_hasher,
        id_generator=id_generator,
        clock=clock,
        unit_of_work=unit_of_work,
        request_context=request_context,
    )