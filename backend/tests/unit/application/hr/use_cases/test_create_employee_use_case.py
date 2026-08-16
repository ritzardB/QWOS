"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_create_employee_use_case.py

Description:
    Unit tests for CreateEmployeeUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import asyncio
from datetime import date, datetime, timezone
from types import SimpleNamespace

import pytest

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.duplicate_resource_exception import (
    DuplicateResourceException,
)
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.common.exceptions.validation_exception import (
    ValidationException,
)
from qwos.application.hr.commands.create_employee_command import (
    CreateEmployeeCommand,
)
from qwos.application.hr.use_cases.create_employee_use_case import (
    CreateEmployeeUseCase,
)
from qwos.application.hr.validators.create_employee_validator import (
    CreateEmployeeValidator,
)


class FakeEmployeeRepository:
    def __init__(
        self,
        existing_by_user: object | None = None,
        existing_by_work_email: bool = False,
    ) -> None:
        self.existing_by_user = existing_by_user
        self.existing_by_work_email = existing_by_work_email
        self.saved_employee: object | None = None

    def get_by_id(
        self,
        employee_id: str,
    ) -> object | None:
        return self.saved_employee

    def save(
        self,
        employee: object,
    ) -> None:
        self.saved_employee = employee

    def get_by_employee_number(
        self,
        *,
        tenant_id: str,
        employee_number: str,
    ) -> object | None:
        return None

    def get_by_user_id(
        self,
        *,
        tenant_id: str,
        user_id: str,
    ) -> object | None:
        return self.existing_by_user

    def exists_by_employee_number(
        self,
        *,
        tenant_id: str,
        employee_number: str,
    ) -> bool:
        return False

    def exists_by_user_id(
        self,
        *,
        tenant_id: str,
        user_id: str,
    ) -> bool:
        return self.existing_by_user is not None

    def exists_by_work_email(
        self,
        *,
        tenant_id: str,
        work_email: str,
    ) -> bool:
        return self.existing_by_work_email


class FakeUserRepository:
    def __init__(
        self,
        user: object | None = None,
    ) -> None:
        self.user = user

    def get_by_id(
        self,
        user_id: str,
    ) -> object | None:
        return self.user

    def save(
        self,
        user: object,
    ) -> None:
        pass


class FakeEmployeeNumberGenerator:
    def __init__(
        self,
        employee_number: str = "QW-00001",
    ) -> None:
        self.employee_number = employee_number
        self.tenant_ids: list[str] = []

    def generate(
        self,
        *,
        tenant_id: str,
    ) -> str:
        self.tenant_ids.append(tenant_id)
        return self.employee_number


class FakeIdGenerator:
    def __init__(self) -> None:
        self._ids = iter(
            (
                "01EMPLOYEE00000000000000001",
            )
        )

    def generate(self) -> str:
        return next(self._ids)


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
            self.commit()
        else:
            self.rollback()

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True

    def flush(self) -> None:
        self.flushed = True


class FakeClock:
    def now(self) -> datetime:
        return datetime(
            2026,
            8,
            16,
            0,
            0,
            tzinfo=timezone.utc,
        )


def make_objects(
    *,
    user: object | None = None,
    existing_by_user: object | None = None,
    existing_by_work_email: bool = False,
    employee_number: str = "QW-00001",
):
    tenant_id = "01TENANT00000000000000000001"

    user = user or SimpleNamespace(
        id="01USER000000000000000000001",
        tenant_id=tenant_id,
    )

    employee_repository = FakeEmployeeRepository(
        existing_by_user=existing_by_user,
        existing_by_work_email=existing_by_work_email,
    )

    user_repository = FakeUserRepository(
        user=user,
    )

    employee_number_generator = FakeEmployeeNumberGenerator(
        employee_number=employee_number,
    )

    id_generator = FakeIdGenerator()
    unit_of_work = FakeUnitOfWork()
    validator = CreateEmployeeValidator()

    request_context = RequestContext(
        tenant_id=tenant_id,
        user_id=user.id,
        correlation_id="correlation-id",
        request_id="request-id",
        locale="en-US",
        timezone="UTC",
        ip_address="127.0.0.1",
        user_agent="pytest",
    )

    use_case = CreateEmployeeUseCase(
        employee_repository=employee_repository,
        user_repository=user_repository,
        employee_number_generator=employee_number_generator,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        validator=validator,
        request_context=request_context,
    )

    return (
        use_case,
        employee_repository,
        user_repository,
        employee_number_generator,
        unit_of_work,
        tenant_id,
    )


def test_create_employee_successfully() -> None:
    (
        use_case,
        employee_repository,
        _user_repository,
        employee_number_generator,
        unit_of_work,
        tenant_id,
    ) = make_objects()

    command = CreateEmployeeCommand(
        tenant_id=tenant_id,
        hire_date=date(2026, 8, 16),
        employment_status="active",
        employment_type="full_time",
        work_email="Richard@QWOS.dev",
        work_phone=" +971 50 123 4567 ",
    )

    response = asyncio.run(use_case.execute(command))

    assert response.id == "01EMPLOYEE00000000000000001"
    assert response.employee_number == "QW-00001"
    assert response.user_id is None
    assert response.hire_date == date(2026, 8, 16)
    assert response.employment_status == "active"
    assert response.employment_type == "full_time"
    assert response.work_email == "richard@qwos.dev"
    assert response.work_phone == "+971 50 123 4567"

    employee = employee_repository.saved_employee

    assert employee is not None
    assert employee.employee_number == "QW-00001"

    assert employee_number_generator.tenant_ids == [
        tenant_id,
    ]

    assert unit_of_work.entered is True
    assert unit_of_work.flushed is True
    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


def test_create_employee_links_existing_user() -> None:
    (
        use_case,
        employee_repository,
        _user_repository,
        _employee_number_generator,
        unit_of_work,
        tenant_id,
    ) = make_objects()

    command = CreateEmployeeCommand(
        tenant_id=tenant_id,
        user_id="01USER000000000000000000001",
    )

    response = asyncio.run(use_case.execute(command))

    assert response.user_id == "01USER000000000000000000001"
    assert employee_repository.saved_employee is not None
    assert unit_of_work.committed is True


def test_create_employee_rejects_unknown_user() -> None:
    (
        use_case,
        _employee_repository,
        user_repository,
        _employee_number_generator,
        unit_of_work,
        tenant_id,
    ) = make_objects()

    user_repository.user = None

    command = CreateEmployeeCommand(
        tenant_id=tenant_id,
        user_id="01USER000000000000000000001",
    )

    with pytest.raises(
        ResourceNotFoundException,
        match="User '01USER000000000000000000001' was not found",
    ):
        asyncio.run(use_case.execute(command))

    assert unit_of_work.entered is False


def test_create_employee_rejects_duplicate_user_link() -> None:
    existing_employee = SimpleNamespace(
        id="01EXISTINGEMPLOYEE00000000001",
    )

    (
        use_case,
        _employee_repository,
        _user_repository,
        _employee_number_generator,
        unit_of_work,
        tenant_id,
    ) = make_objects(
        existing_by_user=existing_employee,
    )

    command = CreateEmployeeCommand(
        tenant_id=tenant_id,
        user_id="01USER000000000000000000001",
    )

    with pytest.raises(
        DuplicateResourceException,
        match="Employee with user_id '01USER000000000000000000001' already exists",
    ):
        asyncio.run(use_case.execute(command))

    assert unit_of_work.entered is False


def test_create_employee_rejects_invalid_command() -> None:
    (
        use_case,
        _employee_repository,
        _user_repository,
        _employee_number_generator,
        unit_of_work,
        _tenant_id,
    ) = make_objects()

    command = CreateEmployeeCommand(
        tenant_id="",
        work_email="not-an-email",
        employment_status="",
        employment_type="",
    )

    with pytest.raises(
        ValidationException,
        match="Validation failed",
    ):
        asyncio.run(use_case.execute(command))

    assert unit_of_work.entered is False


def test_create_employee_rejects_user_from_different_tenant() -> None:
    other_tenant_user = SimpleNamespace(
        id="01USER000000000000000000001",
        tenant_id="01OTHERTENANT00000000000000001",
    )

    (
        use_case,
        _employee_repository,
        _user_repository,
        _employee_number_generator,
        unit_of_work,
        tenant_id,
    ) = make_objects(
        user=other_tenant_user,
    )

    command = CreateEmployeeCommand(
        tenant_id=tenant_id,
        user_id=other_tenant_user.id,
    )

    with pytest.raises(
        ValueError,
        match="User does not belong to the requested tenant",
    ):
        asyncio.run(use_case.execute(command))

    assert unit_of_work.entered is False

def test_create_employee_rejects_duplicate_work_email() -> None:
    (
        use_case,
        _employee_repository,
        _user_repository,
        employee_number_generator,
        unit_of_work,
        tenant_id,
    ) = make_objects(
        existing_by_work_email=True,
    )

    command = CreateEmployeeCommand(
        tenant_id=tenant_id,
        work_email="richard@qwos.dev",
    )

    with pytest.raises(
        DuplicateResourceException,
        match="Employee with work_email 'richard@qwos.dev' already exists",
    ):
        asyncio.run(use_case.execute(command))

    assert employee_number_generator.tenant_ids == []
    assert unit_of_work.entered is False