"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_link_employee_to_user_use_case.py

Description:
    Unit tests for LinkEmployeeToUserUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.hr.commands.link_employee_to_user_command import (
    LinkEmployeeToUserCommand,
)
from qwos.application.hr.use_cases.link_employee_to_user_use_case import (
    LinkEmployeeToUserUseCase,
)

_UNSET = object()


class FakeEmployeeRepository:
    def __init__(
        self,
        employee: object | None,
    ) -> None:
        self.employee = employee
        self.saved_employee: object | None = None

    def get_by_id(
        self,
        employee_id: str,
    ) -> object | None:
        return self.employee

    def save(
        self,
        employee: object,
    ) -> None:
        self.saved_employee = employee


class FakeUserRepository:
    def __init__(
        self,
        user: object | None,
    ) -> None:
        self.user = user

    def get_by_id(
        self,
        user_id: str,
    ) -> object | None:
        return self.user


class FakeUserProfileRepository:
    def __init__(
        self,
        profile: object | None = None,
    ) -> None:
        self.profile = profile
        self.saved_profile: object | None = None

    def get_by_user_id(
        self,
        user_id: str,
    ) -> object | None:
        return self.profile

    def save(
        self,
        profile: object,
    ) -> None:
        self.saved_profile = profile


class FakeIdGenerator:
    def __init__(self) -> None:
        self.generated = 0

    def generate(self) -> str:
        self.generated += 1
        return "01PROFILE000000000000000001"


class FakeUnitOfWork:
    def __init__(self) -> None:
        self.entered = False
        self.committed = False
        self.rolled_back = False
        self.flushed = False

    def __enter__(self) -> "FakeUnitOfWork":
        self.entered = True
        return self

    def __exit__(
        self,
        exc_type,
        exc,
        tb,
    ) -> None:
        if exc is None:
            self.committed = True
        else:
            self.rolled_back = True

    def flush(self) -> None:
        self.flushed = True


def make_objects(
    *,
    employee: object | None = _UNSET,
    user: object | None = _UNSET,
    profile: object | None = None,
):
    tenant_id = "01KZYRPZANTQJBZYE7KS4DCRGW"

    if employee is _UNSET:
        employee = SimpleNamespace(
            id="01M03ZJQ8XMGC7424THFKH4HVD",
            tenant_id=tenant_id,
            employee_number="QW-00001",
            user_id=None,
            updated_at=datetime(
                2026,
                8,
                16,
                4,
                30,
                tzinfo=timezone.utc,
            ),
        )

    if user is _UNSET:
        user = SimpleNamespace(
            id="01KZYTCWRF8S12V28R9NX6JXS5",
            tenant_id=tenant_id,
        )

    employee_repository = FakeEmployeeRepository(employee)
    user_repository = FakeUserRepository(user)
    profile_repository = FakeUserProfileRepository(profile)
    id_generator = FakeIdGenerator()
    unit_of_work = FakeUnitOfWork()

    request_context = RequestContext(
        tenant_id=tenant_id,
        user_id=(
            user.id
            if user is not None
            else None
        ),
        correlation_id="correlation-id",
        request_id="request-id",
        locale="en-US",
        timezone="UTC",
        ip_address=None,
        user_agent="pytest",
    )

    use_case = LinkEmployeeToUserUseCase(
        employee_repository=employee_repository,
        user_repository=user_repository,
        user_profile_repository=profile_repository,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        request_context=request_context,
    )

    return (
        use_case,
        employee_repository,
        user_repository,
        profile_repository,
        id_generator,
        unit_of_work,
        tenant_id,
    )


def make_command(
    tenant_id: str,
) -> LinkEmployeeToUserCommand:
    return LinkEmployeeToUserCommand(
        tenant_id=tenant_id,
        employee_id="01M03ZJQ8XMGC7424THFKH4HVD",
        user_id="01KZYTCWRF8S12V28R9NX6JXS5",
        first_name="Richard",
        middle_name="Santisas",
        last_name="Balabarcon",
        preferred_name="Richard S. Balabarcon",
    )


def test_links_employee_and_creates_profile() -> None:
    (
        use_case,
        employee_repository,
        _user_repository,
        profile_repository,
        id_generator,
        unit_of_work,
        tenant_id,
    ) = make_objects()

    response = asyncio.run(
        use_case.execute(
            make_command(tenant_id),
        )
    )

    assert response.employee_id == "01M03ZJQ8XMGC7424THFKH4HVD"
    assert response.employee_number == "QW-00001"
    assert response.user_id == "01KZYTCWRF8S12V28R9NX6JXS5"
    assert response.profile_id == "01PROFILE000000000000000001"
    assert response.display_name == "Richard Balabarcon"
    assert response.preferred_name == "Richard S. Balabarcon"

    employee = employee_repository.saved_employee

    assert employee is not None
    assert employee.user_id == "01KZYTCWRF8S12V28R9NX6JXS5"

    profile = profile_repository.saved_profile

    assert profile is not None
    assert profile.first_name == "Richard"
    assert profile.middle_name == "Santisas"
    assert profile.last_name == "Balabarcon"
    assert profile.preferred_name == "Richard S. Balabarcon"

    assert unit_of_work.entered is True
    assert unit_of_work.flushed is True
    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


def test_reuses_existing_matching_profile() -> None:
    existing_profile = SimpleNamespace(
        id="01EXISTINGPROFILE000000000001",
        first_name="Richard",
        middle_name="Santisas",
        last_name="Balabarcon",
        preferred_name="Richard S. Balabarcon",
        display_name="Richard Balabarcon",
    )

    (
        use_case,
        employee_repository,
        _user_repository,
        profile_repository,
        id_generator,
        unit_of_work,
        tenant_id,
    ) = make_objects(
        profile=existing_profile,
    )

    response = asyncio.run(
        use_case.execute(
            make_command(tenant_id),
        )
    )

    assert response.employee_id == "01M03ZJQ8XMGC7424THFKH4HVD"
    assert response.employee_number == "QW-00001"
    assert response.user_id == "01KZYTCWRF8S12V28R9NX6JXS5"
    assert response.profile_id == existing_profile.id
    assert response.display_name == "Richard Balabarcon"
    assert response.preferred_name == "Richard S. Balabarcon"
    assert id_generator.generated == 0  # No new profile was created

    employee = employee_repository.saved_employee

    assert employee is not None
    assert employee.user_id == "01KZYTCWRF8S12V28R9NX6JXS5"

    assert profile_repository.saved_profile is None

    assert unit_of_work.entered is True
    assert unit_of_work.flushed is True
    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


def test_rejects_mismatching_existing_profile() -> None:
    existing_profile = SimpleNamespace(
        id="01EXISTINGPROFILE000000000001",
        first_name="Different",
        middle_name="Person",
        last_name="Example",
        preferred_name="Different Example",
    )

    (
        use_case,
        _employee_repository,
        _user_repository,
        _profile_repository,
        id_generator,
        unit_of_work,
        tenant_id,
    ) = make_objects(
        profile=existing_profile,
    )

    with pytest.raises(
        ValueError,
        match=(
            "Existing UserProfile does not match the supplied identity data"
        ),
    ):
        asyncio.run(
            use_case.execute(
                make_command(tenant_id),
            )
        )

    assert unit_of_work.entered is False


def test_rejects_missing_employee() -> None:
    (
        use_case,
        _employee_repository,
        _user_repository,
        _profile_repository,
        _id_generator,
        unit_of_work,
        tenant_id,
    ) = make_objects(
        employee=None,
    )

    with pytest.raises(
        ResourceNotFoundException,
        match="Employee '01M03ZJQ8XMGC7424THFKH4HVD' was not found",
    ):
        asyncio.run(
            use_case.execute(
                make_command(tenant_id),
            )
        )

    assert unit_of_work.entered is False


def test_rejects_missing_user() -> None:
    (
        use_case,
        _employee_repository,
        _user_repository,
        _profile_repository,
        _id_generator,
        unit_of_work,
        tenant_id,
    ) = make_objects(
        user=None,
    )

    with pytest.raises(
        ResourceNotFoundException,
        match="User '01KZYTCWRF8S12V28R9NX6JXS5' was not found",
    ):
        asyncio.run(
            use_case.execute(
                make_command(tenant_id),
            )
        )

    assert unit_of_work.entered is False