"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_create_leave_policy_use_case.py

Description:
    Unit tests for CreateLeavePolicyUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

import pytest

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.duplicate_resource_exception import (
    DuplicateResourceException,
)
from qwos.application.common.exceptions.validation_exception import (
    ValidationException,
)
from qwos.application.common.results.create_leave_policy_validator import (
    CreateLeavePolicyValidator,
)
from qwos.application.leave.commands.create_leave_policy_command import (
    CreateLeavePolicyCommand,
)
from qwos.application.leave.use_cases.create_leave_policy_use_case import (
    CreateLeavePolicyUseCase,
)

TENANT_ID = "01M0TEN00000000000000000001"
OTHER_TENANT_ID = "01M0TEN00000000000000000002"
USER_ID = "01M0USR00000000000000000001"
LEAVE_POLICY_ID = "01M0LP00000000000000000001"
LEAVE_TYPE_ID = "01M0LT00000000000000000001"


class FakeRepository:
    def __init__(self) -> None:
        self.save_calls: list[object] = []
        self.exists_result = False

    def exists_by_code(
        self,
        *,
        tenant_id: str,
        policy_code: str,
    ) -> bool:
        return self.exists_result

    def save(self, entity: object) -> None:
        self.save_calls.append(entity)


class FakeIdGenerator:
    def generate(self) -> str:
        return LEAVE_POLICY_ID


class FakeUnitOfWork:
    def __init__(self) -> None:
        self.entered = False
        self.exited = False
        self.flush_called = False

    def __enter__(self):
        self.entered = True
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        self.exited = True

    def flush(self) -> None:
        self.flush_called = True


def make_request_context() -> RequestContext:
    return RequestContext(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        correlation_id="test-correlation-id",
        request_id="test-request-id",
        locale="en-US",
        timezone="UTC",
        ip_address=None,
        user_agent=None,
    )


def make_command(
    *,
    tenant_id: str = TENANT_ID,
    leave_type_id: str = LEAVE_TYPE_ID,
    policy_code: str = "annual-standard",
    policy_name: str = "Annual Standard",
    description: str | None = "Standard annual leave policy.",
    entitlement_days: Decimal = Decimal("30.00"),
    accrual_method: str = "annual",
    accrual_frequency: str = "monthly",
    carry_forward_allowed: bool = False,
    carry_forward_days: Decimal | None = None,
    minimum_service_days: int = 0,
    is_active: bool = True,
) -> CreateLeavePolicyCommand:
    return CreateLeavePolicyCommand(
        tenant_id=tenant_id,
        leave_type_id=leave_type_id,
        policy_code=policy_code,
        policy_name=policy_name,
        description=description,
        entitlement_days=entitlement_days,
        accrual_method=accrual_method,
        accrual_frequency=accrual_frequency,
        carry_forward_allowed=carry_forward_allowed,
        carry_forward_days=carry_forward_days,
        minimum_service_days=minimum_service_days,
        is_active=is_active,
    )


def make_use_case() -> tuple[
    CreateLeavePolicyUseCase,
    FakeRepository,
    FakeIdGenerator,
    FakeUnitOfWork,
]:
    repository = FakeRepository()
    id_generator = FakeIdGenerator()
    unit_of_work = FakeUnitOfWork()

    use_case = CreateLeavePolicyUseCase(
        leave_policy_repository=repository,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        validator=CreateLeavePolicyValidator(),
        request_context=make_request_context(),
    )

    return (
        use_case,
        repository,
        id_generator,
        unit_of_work,
    )


@pytest.mark.asyncio
async def test_create_leave_policy_successfully() -> None:
    (
        use_case,
        repository,
        _,
        unit_of_work,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(),
    )

    assert response.id == LEAVE_POLICY_ID
    assert response.leave_type_id == LEAVE_TYPE_ID
    assert response.policy_code == "annual-standard"
    assert response.policy_name == "Annual Standard"
    assert response.description == "Standard annual leave policy."
    assert response.entitlement_days == Decimal("30.00")
    assert response.accrual_method == "annual"
    assert response.accrual_frequency == "monthly"
    assert response.carry_forward_allowed is False
    assert response.carry_forward_days is None
    assert response.minimum_service_days == 0
    assert response.is_active is True

    assert len(repository.save_calls) == 1
    assert unit_of_work.entered is True
    assert unit_of_work.exited is True
    assert unit_of_work.flush_called is True


@pytest.mark.asyncio
async def test_create_leave_policy_normalizes_policy_code() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            policy_code="  ANNUAL-STANDARD  ",
        ),
    )

    assert response.policy_code == "annual-standard"

    saved_policy = repository.save_calls[0]

    assert saved_policy.policy_code == "annual-standard"


@pytest.mark.asyncio
async def test_create_leave_policy_normalizes_policy_name() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            policy_name="  Annual Standard  ",
        ),
    )

    assert response.policy_name == "Annual Standard"

    saved_policy = repository.save_calls[0]

    assert saved_policy.policy_name == "Annual Standard"


@pytest.mark.asyncio
async def test_create_leave_policy_normalizes_description() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            description="  Standard annual leave policy.  ",
        ),
    )

    assert response.description == "Standard annual leave policy."

    saved_policy = repository.save_calls[0]

    assert saved_policy.description == "Standard annual leave policy."


@pytest.mark.asyncio
async def test_create_leave_policy_normalizes_accrual_method() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            accrual_method="  ANNUAL  ",
        ),
    )

    assert response.accrual_method == "annual"

    saved_policy = repository.save_calls[0]

    assert saved_policy.accrual_method == "annual"


@pytest.mark.asyncio
async def test_create_leave_policy_normalizes_accrual_frequency() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            accrual_frequency="  MONTHLY  ",
        ),
    )

    assert response.accrual_frequency == "monthly"

    saved_policy = repository.save_calls[0]

    assert saved_policy.accrual_frequency == "monthly"


@pytest.mark.asyncio
async def test_create_leave_policy_accepts_carry_forward() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            carry_forward_allowed=True,
            carry_forward_days=Decimal("10.00"),
        ),
    )

    assert response.carry_forward_allowed is True
    assert response.carry_forward_days == Decimal("10.00")

    saved_policy = repository.save_calls[0]

    assert saved_policy.carry_forward_allowed is True
    assert saved_policy.carry_forward_days == Decimal("10.00")


@pytest.mark.asyncio
async def test_create_leave_policy_accepts_minimum_service_days() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            minimum_service_days=180,
        ),
    )

    assert response.minimum_service_days == 180

    saved_policy = repository.save_calls[0]

    assert saved_policy.minimum_service_days == 180


@pytest.mark.asyncio
async def test_create_leave_policy_accepts_zero_entitlement() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            entitlement_days=Decimal("0"),
        ),
    )

    assert response.entitlement_days == Decimal("0")

    saved_policy = repository.save_calls[0]

    assert saved_policy.entitlement_days == Decimal("0")


@pytest.mark.asyncio
async def test_create_leave_policy_allows_null_description() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            description=None,
        ),
    )

    assert response.description is None

    saved_policy = repository.save_calls[0]

    assert saved_policy.description is None


@pytest.mark.asyncio
async def test_create_leave_policy_allows_null_carry_forward_days() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            carry_forward_days=None,
        ),
    )

    assert response.carry_forward_days is None

    saved_policy = repository.save_calls[0]

    assert saved_policy.carry_forward_days is None


@pytest.mark.asyncio
async def test_create_leave_policy_accepts_inactive_policy() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(
            is_active=False,
        ),
    )

    assert response.is_active is False

    saved_policy = repository.save_calls[0]

    assert saved_policy.is_active is False


@pytest.mark.asyncio
async def test_duplicate_policy_code_raises_duplicate_resource() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    repository.exists_result = True

    with pytest.raises(DuplicateResourceException):
        await use_case.execute(
            make_command(),
        )

    assert len(repository.save_calls) == 0


@pytest.mark.asyncio
async def test_invalid_policy_raises_validation_exception() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                policy_name="   ",
            ),
        )

    assert len(repository.save_calls) == 0


@pytest.mark.asyncio
async def test_negative_entitlement_raises_validation_exception() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                entitlement_days=Decimal("-1.00"),
            ),
        )

    assert len(repository.save_calls) == 0


@pytest.mark.asyncio
async def test_negative_carry_forward_days_raises_validation_exception() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                carry_forward_days=Decimal("-1.00"),
            ),
        )

    assert len(repository.save_calls) == 0


@pytest.mark.asyncio
async def test_negative_minimum_service_days_raises_validation_exception() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    with pytest.raises(ValidationException):
        await use_case.execute(
            make_command(
                minimum_service_days=-1,
            ),
        )

    assert len(repository.save_calls) == 0


@pytest.mark.asyncio
async def test_create_leave_policy_uses_generated_id() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    response = await use_case.execute(
        make_command(),
    )

    assert response.id == LEAVE_POLICY_ID

    saved_policy = repository.save_calls[0]

    assert saved_policy.id == LEAVE_POLICY_ID


@pytest.mark.asyncio
async def test_create_leave_policy_sets_audit_user() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    await use_case.execute(
        make_command(),
    )

    saved_policy = repository.save_calls[0]

    assert saved_policy.created_by == USER_ID
    assert saved_policy.updated_by == USER_ID


@pytest.mark.asyncio
async def test_create_leave_policy_preserves_tenant_id() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    await use_case.execute(
        make_command(),
    )

    saved_policy = repository.save_calls[0]

    assert saved_policy.tenant_id == TENANT_ID


@pytest.mark.asyncio
async def test_create_leave_policy_preserves_leave_type_id() -> None:
    (
        use_case,
        repository,
        _,
        _,
    ) = make_use_case()

    await use_case.execute(
        make_command(),
    )

    saved_policy = repository.save_calls[0]

    assert saved_policy.leave_type_id == LEAVE_TYPE_ID