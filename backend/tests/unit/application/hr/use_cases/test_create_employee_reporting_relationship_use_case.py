"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_create_employee_reporting_relationship_use_case.py

Description:
    Unit tests for CreateEmployeeReportingRelationshipUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import asyncio
from datetime import date
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
from qwos.application.hr.commands.create_employee_reporting_relationship_command import (
    CreateEmployeeReportingRelationshipCommand,
)
from qwos.application.hr.use_cases.create_employee_reporting_relationship_use_case import (
    CreateEmployeeReportingRelationshipUseCase,
)

_UNSET = object()


class FakeEmployeeRepository:
    def __init__(self, employees: dict[str, object]) -> None:
        self.employees = employees

    def get_by_id(self, employee_id: str) -> object | None:
        return self.employees.get(employee_id)


class FakeRelationshipRepository:
    def __init__(
        self,
        existing_primary: object | None = None,
    ) -> None:
        self.existing_primary = existing_primary
        self.saved_relationship: object | None = None

    def get_active_primary_manager(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> object | None:
        return self.existing_primary

    def exists_active_primary_manager(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> bool:
        return self.existing_primary is not None

    def save(self, relationship: object) -> None:
        self.saved_relationship = relationship


class FakeIdGenerator:
    def __init__(self) -> None:
        self.generated = 0

    def generate(self) -> str:
        self.generated += 1
        return "01RELATIONSHIP00000000000001"


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
    manager: object | None = _UNSET,
    existing_primary: object | None = None,
):
    tenant_id = "01KZYRPZANTQJBZYE7KS4DCRGW"

    if employee is _UNSET:
        employee = SimpleNamespace(
            id="01M03ZJQ8XMGC7424THFKH4HVD",
            tenant_id=tenant_id,
        )

    if manager is _UNSET:
        manager = SimpleNamespace(
            id="01M03ZJQ8XMGC7424THFKH4HVE",
            tenant_id=tenant_id,
        )

    employees: dict[str, object] = {}

    if employee is not None:
        employees[employee.id] = employee

    if manager is not None:
        employees[manager.id] = manager

    employee_repository = FakeEmployeeRepository(employees)
    relationship_repository = FakeRelationshipRepository(
        existing_primary=existing_primary,
    )
    id_generator = FakeIdGenerator()
    unit_of_work = FakeUnitOfWork()

    request_context = RequestContext(
        tenant_id=tenant_id,
        user_id="01KZYTCWRF8S12V28R9NX6JXS5",
        correlation_id="correlation-id",
        request_id="request-id",
        locale="en-US",
        timezone="UTC",
        ip_address=None,
        user_agent="pytest",
    )

    use_case = CreateEmployeeReportingRelationshipUseCase(
        employee_repository=employee_repository,
        relationship_repository=relationship_repository,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        validator=(
            __import__(
                "qwos.application.hr.validators."
                "create_employee_reporting_relationship_validator",
                fromlist=[
                    "CreateEmployeeReportingRelationshipValidator",
                ],
            ).CreateEmployeeReportingRelationshipValidator()
        ),
        request_context=request_context,
    )

    return (
        use_case,
        employee_repository,
        relationship_repository,
        id_generator,
        unit_of_work,
        tenant_id,
    )


def make_command(
    tenant_id: str,
) -> CreateEmployeeReportingRelationshipCommand:
    return CreateEmployeeReportingRelationshipCommand(
        tenant_id=tenant_id,
        employee_id="01M03ZJQ8XMGC7424THFKH4HVD",
        manager_employee_id="01M03ZJQ8XMGC7424THFKH4HVE",
        relationship_type="primary_manager",
        effective_from=date(2026, 8, 16),
        is_primary=True,
    )


def test_creates_primary_manager_relationship() -> None:
    (
        use_case,
        _employee_repository,
        relationship_repository,
        id_generator,
        unit_of_work,
        tenant_id,
    ) = make_objects()

    response = asyncio.run(
        use_case.execute(
            make_command(tenant_id),
        )
    )

    assert response.id == "01RELATIONSHIP00000000000001"
    assert response.employee_id == "01M03ZJQ8XMGC7424THFKH4HVD"
    assert response.manager_employee_id == (
        "01M03ZJQ8XMGC7424THFKH4HVE"
    )
    assert response.relationship_type == "primary_manager"
    assert response.is_primary is True

    relationship = relationship_repository.saved_relationship

    assert relationship is not None
    assert relationship.employee_id == "01M03ZJQ8XMGC7424THFKH4HVD"
    assert relationship.manager_employee_id == (
        "01M03ZJQ8XMGC7424THFKH4HVE"
    )

    assert id_generator.generated == 1
    assert unit_of_work.entered is True
    assert unit_of_work.flushed is True
    assert unit_of_work.committed is True


def test_rejects_missing_employee() -> None:
    (
        use_case,
        _employee_repository,
        _relationship_repository,
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


def test_rejects_missing_manager() -> None:
    (
        use_case,
        _employee_repository,
        _relationship_repository,
        _id_generator,
        unit_of_work,
        tenant_id,
    ) = make_objects(
        manager=None,
    )

    with pytest.raises(
        ResourceNotFoundException,
        match="Employee '01M03ZJQ8XMGC7424THFKH4HVE' was not found",
    ):
        asyncio.run(
            use_case.execute(
                make_command(tenant_id),
            )
        )

    assert unit_of_work.entered is False


def test_rejects_duplicate_primary_manager() -> None:
    existing_primary = SimpleNamespace(
        id="01EXISTINGREL000000000000001",
    )

    (
        use_case,
        _employee_repository,
        _relationship_repository,
        id_generator,
        unit_of_work,
        tenant_id,
    ) = make_objects(
        existing_primary=existing_primary,
    )

    with pytest.raises(
        DuplicateResourceException,
        match="EmployeeReportingRelationship with employee_id",
    ):
        asyncio.run(
            use_case.execute(
                make_command(tenant_id),
            )
        )

    assert id_generator.generated == 0
    assert unit_of_work.entered is False


def test_rejects_self_management() -> None:
    command = CreateEmployeeReportingRelationshipCommand(
        tenant_id="01KZYRPZANTQJBZYE7KS4DCRGW",
        employee_id="01M03ZJQ8XMGC7424THFKH4HVD",
        manager_employee_id="01M03ZJQ8XMGC7424THFKH4HVD",
        relationship_type="primary_manager",
        effective_from=date(2026, 8, 16),
        is_primary=True,
    )

    (
        use_case,
        _employee_repository,
        _relationship_repository,
        _id_generator,
        unit_of_work,
        _tenant_id,
    ) = make_objects()

    with pytest.raises(
        ValidationException,
        match="Validation failed",
    ):
        asyncio.run(
            use_case.execute(command)
        )

    assert unit_of_work.entered is False