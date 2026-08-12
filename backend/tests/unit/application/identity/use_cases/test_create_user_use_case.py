"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_create_user_use_case.py

Description:
    Unit tests for CreateUserUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone

import pytest

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.duplicate_resource_exception import (
    DuplicateResourceException,
)
from qwos.application.common.exceptions.validation_exception import (
    ValidationException,
)
from qwos.application.common.results.validation_result import ValidationResult
from qwos.application.identity.commands.create_user_command import (
    CreateUserCommand,
)
from qwos.application.identity.use_cases.create_user_use_case import (
    CreateUserUseCase,
)
from qwos.domains.identity.enums.user_type import UserType


class FakeUserRepository:
    def __init__(
        self,
        *,
        email_exists: bool = False,
        username_exists: bool = False,
    ) -> None:
        self.email_exists = email_exists
        self.username_exists = username_exists
        self.saved_user: object | None = None

    def exists_by_email(self, email: str) -> bool:
        return self.email_exists

    def exists_by_username(self, username: str) -> bool:
        return self.username_exists

    def save(self, user: object) -> None:
        self.saved_user = user


class FakeUserProfileRepository:
    def __init__(self) -> None:
        self.saved_profile: object | None = None

    def save(self, profile: object) -> None:
        self.saved_profile = profile


class FakePasswordHasher:
    def __init__(self) -> None:
        self.hashed_password: str | None = None

    def hash(self, password: str) -> str:
        self.hashed_password = password
        return f"bcrypt:{password}"


class FakeIdGenerator:
    def __init__(self) -> None:
        self._ids = iter(
            (
                "01USER000000000000000000001",
                "01PROFILE000000000000000001",
            )
        )

    def generate(self) -> str:
        return next(self._ids)


class FakeClock:
    def __init__(self) -> None:
        self.current_time = datetime(
            2026,
            8,
            12,
            12,
            0,
            0,
            tzinfo=timezone.utc,
        )

    def now(self) -> datetime:
        return self.current_time


class FakeUnitOfWork:
    def __init__(self) -> None:
        self.entered = False
        self.committed = False
        self.rolled_back = False
        self.flushed = False

    def __enter__(self) -> "FakeUnitOfWork":
        self.entered = True
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc is None:
            self.commit()
        else:
            self.rollback()

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True

    def flush(self) -> None:
        self.flushed = True


class FakeCreateUserValidator:
    def __init__(
        self,
        validation_result: ValidationResult | None = None,
    ) -> None:
        self.validation_result = (
            validation_result
            if validation_result is not None
            else ValidationResult()
        )

    def validate(
        self,
        command: CreateUserCommand,
    ) -> ValidationResult:
        return self.validation_result


def make_command(
    *,
    tenant_id: str = "01HTENANT000000000000000001",
) -> CreateUserCommand:
    return CreateUserCommand(
        tenant_id=tenant_id,
        first_name="John",
        middle_name="Michael",
        last_name="Doe",
        preferred_name="John",
        email="john.doe@example.com",
        username="john.doe",
        password="SecurePassword123!",
        user_type=UserType.EMPLOYEE,
    )


def make_request_context(
    *,
    tenant_id: str = "01HTENANT000000000000000001",
) -> RequestContext:
    return RequestContext(
        tenant_id=tenant_id,
        user_id=None,
        correlation_id="correlation-id",
        request_id="request-id",
        locale="en-US",
        timezone="UTC",
        ip_address="127.0.0.1",
        user_agent="pytest",
    )


def make_use_case(
    *,
    email_exists: bool = False,
    username_exists: bool = False,
    validation_result: ValidationResult | None = None,
):
    user_repository = FakeUserRepository(
        email_exists=email_exists,
        username_exists=username_exists,
    )
    user_profile_repository = FakeUserProfileRepository()
    password_hasher = FakePasswordHasher()
    id_generator = FakeIdGenerator()
    clock = FakeClock()
    unit_of_work = FakeUnitOfWork()
    validator = FakeCreateUserValidator(validation_result)

    request_context = make_request_context()

    use_case = CreateUserUseCase(
        user_repository=user_repository,
        user_profile_repository=user_profile_repository,
        password_hasher=password_hasher,
        id_generator=id_generator,
        clock=clock,
        unit_of_work=unit_of_work,
        validator=validator,
        request_context=request_context,
    )

    return (
        use_case,
        user_repository,
        user_profile_repository,
        password_hasher,
        id_generator,
        clock,
        unit_of_work,
    )


def test_create_user_successfully_creates_user_and_profile() -> None:
    (
        use_case,
        user_repository,
        user_profile_repository,
        password_hasher,
        _,
        _clock,
        unit_of_work,
    ) = make_use_case()

    command = make_command()

    response = asyncio.run(use_case.execute(command))

    assert response.email == command.email
    assert response.username == command.username
    assert response.first_name == command.first_name
    assert response.last_name == command.last_name
    assert response.user_type == command.user_type
    assert response.id == "01USER000000000000000000001"

    assert password_hasher.hashed_password == command.password

    assert user_repository.saved_user is not None
    assert user_profile_repository.saved_profile is not None

    user = user_repository.saved_user
    profile = user_profile_repository.saved_profile

    assert user.id == "01USER000000000000000000001"
    assert user.tenant_id == command.tenant_id
    assert user.email == command.email
    assert user.username == command.username
    assert user.password_hash == f"bcrypt:{command.password}"
    assert user.user_type == command.user_type

    assert profile.id == "01PROFILE000000000000000001"
    assert profile.tenant_id == command.tenant_id
    assert profile.user_id == user.id
    assert profile.first_name == command.first_name
    assert profile.middle_name == command.middle_name
    assert profile.last_name == command.last_name
    assert profile.preferred_name == command.preferred_name

    assert unit_of_work.entered is True
    assert unit_of_work.flushed is True
    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


def test_create_user_rejects_invalid_command() -> None:
    from qwos.application.common.results.validation_error import (
        ValidationError,
    )

    validation_result = ValidationResult(
        errors=[
            ValidationError(
                field="email",
                message="Email format is invalid.",
            )
        ]
    )

    use_case, *_ = make_use_case(
        validation_result=validation_result,
    )

    command = make_command()

    with pytest.raises(
        ValidationException,
        match="Validation failed.",
    ) as exc_info:
        asyncio.run(use_case.execute(command))

    assert exc_info.value.validation_result is validation_result
    assert len(exc_info.value.validation_result.errors) == 1
    assert exc_info.value.validation_result.errors[0].field == "email"
    assert (
        exc_info.value.validation_result.errors[0].message
        == "Email format is invalid."
    )


def test_create_user_checks_duplicate_email() -> None:
    use_case, *_ = make_use_case(
        email_exists=True,
    )

    command = make_command()

    with pytest.raises(
        DuplicateResourceException,
        match="User with email .* already exists",
    ):
        asyncio.run(use_case.execute(command))

def test_create_user_checks_duplicate_username() -> None:
    use_case, *_ = make_use_case(
        username_exists=True,
    )

    command = make_command()

    with pytest.raises(
        DuplicateResourceException,
        match="User with username .* already exists",
    ):
        asyncio.run(use_case.execute(command))