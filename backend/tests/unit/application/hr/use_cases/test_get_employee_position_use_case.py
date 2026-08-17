from __future__ import annotations

import asyncio
from datetime import date
from types import SimpleNamespace

import pytest

from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.hr.use_cases.get_employee_position_use_case import (
    GetEmployeePositionUseCase,
)

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
EMPLOYEE_ID = "01M03ZJQ8XMGC7424THFKH4HVD"


def make_objects(
    position: object | None = None,
):
    employee_position_repository = SimpleNamespace(
        get_current_by_employee_id=lambda **_: position,
    )

    use_case = GetEmployeePositionUseCase(
        employee_position_repository=employee_position_repository,
    )

    return use_case, employee_position_repository


def test_returns_current_position() -> None:
    position = SimpleNamespace(
        id="01M08ED3QM623NWN4N0NBQ8VF6",
        employee_id=EMPLOYEE_ID,
        job_title="CEO / Owner & Shareholder",
        organizational_level="executive",
        effective_from=date(2026, 8, 16),
        effective_to=None,
    )

    use_case, _repository = make_objects(position)

    response = asyncio.run(
        use_case.execute(
            tenant_id=TENANT_ID,
            employee_id=EMPLOYEE_ID,
        )
    )

    assert response.id == position.id
    assert response.employee_id == EMPLOYEE_ID
    assert response.job_title == "CEO / Owner & Shareholder"
    assert response.organizational_level == "executive"
    assert response.effective_from == date(2026, 8, 16)
    assert response.effective_to is None


def test_rejects_missing_position() -> None:
    use_case, _repository = make_objects()

    with pytest.raises(
        ResourceNotFoundException,
        match="EmployeePosition",
    ):
        asyncio.run(
            use_case.execute(
                tenant_id=TENANT_ID,
                employee_id=EMPLOYEE_ID,
            )
        )