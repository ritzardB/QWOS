"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

HR Module

File:
    test_update_employee_profile_use_case.py

Description:
    Unit tests for UpdateEmployeeProfileUseCase.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.exceptions.forbidden_exception import (
    ForbiddenException,
)
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.hr.commands.update_employee_profile_command import (
    UpdateEmployeeProfileCommand,
)
from qwos.application.hr.use_cases.update_employee_profile_use_case import (
    UpdateEmployeeProfileUseCase,
)

TENANT_ID = "01KZYRPZANTQJBZYE7KS4DCRGW"
USER_ID = "01KZYTCWRF8S12V28R9NX6JXS5"
EMPLOYEE_ID = "01M03ZJQ8XMGC7424THFKH4HVD"
PROFILE_ID = "01PROFILE000000000001"

TEST_NOW = datetime(
    2026,
    8,
    18,
    15,
    0,
    tzinfo=timezone.utc,
)


def make_command() -> UpdateEmployeeProfileCommand:
    return UpdateEmployeeProfileCommand(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
        date_of_birth=date(1971, 1, 15),
        gender="Male",
        nationality="Philippine",
        marital_status="Married",
        personal_email="updated@example.com",
        personal_phone="+971501112233",
        address_line_1="Updated Street",
        address_line_2="Apartment 20",
        city="Abu Dhabi",
        state_province="Abu Dhabi",
        postal_code="11111",
        country_code="ae",
        emergency_contact_name="Maria",
        emergency_contact_relationship="Spouse",
        emergency_contact_phone="+971502223344",
    )


def make_employee() -> MagicMock:
    employee = MagicMock()
    employee.id = EMPLOYEE_ID
    employee.tenant_id = TENANT_ID
    return employee


def make_profile() -> MagicMock:
    profile = MagicMock()

    profile.id = PROFILE_ID
    profile.employee_id = EMPLOYEE_ID
    profile.date_of_birth = date(1971, 1, 15)
    profile.gender = "male"
    profile.nationality = "philippine"
    profile.marital_status = "married"
    profile.personal_email = "updated@example.com"
    profile.personal_phone = "+971501112233"
    profile.address_line_1 = "Updated Street"
    profile.address_line_2 = "Apartment 20"
    profile.city = "Abu Dhabi"
    profile.state_province = "Abu Dhabi"
    profile.postal_code = "11111"
    profile.country_code = "AE"
    profile.emergency_contact_name = "Maria"
    profile.emergency_contact_relationship = "spouse"
    profile.emergency_contact_phone = "+971502223344"
    profile.created_at = TEST_NOW

    return profile


def make_use_case() -> tuple[
    UpdateEmployeeProfileUseCase,
    MagicMock,
    MagicMock,
    AsyncMock,
    MagicMock,
]:
    employee_repository = MagicMock()
    employee_profile_repository = MagicMock()
    authorization_service = AsyncMock()
    unit_of_work = MagicMock()
    request_context = MagicMock(spec=RequestContext)

    request_context.tenant_id = TENANT_ID
    request_context.user_id = USER_ID

    use_case = UpdateEmployeeProfileUseCase(
        employee_repository=employee_repository,
        employee_profile_repository=employee_profile_repository,
        authorization_service=authorization_service,
        unit_of_work=unit_of_work,
        request_context=request_context,
    )

    return (
        use_case,
        employee_repository,
        employee_profile_repository,
        authorization_service,
        unit_of_work,
    )


@pytest.mark.anyio
async def test_update_employee_profile_updates_profile_when_authorized() -> None:
    (
        use_case,
        employee_repository,
        employee_profile_repository,
        authorization_service,
        unit_of_work,
    ) = make_use_case()

    employee_repository.get_by_id.return_value = make_employee()

    profile = make_profile()

    employee_profile_repository.get_by_employee_id.return_value = (
        profile
    )

    authorization_service.has_permission.return_value = True

    command = make_command()

    result = await use_case.execute(command)

    authorization_service.has_permission.assert_called_once_with(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        permission_code="HR_PROFILE_UPDATE",
    )

    employee_repository.get_by_id.assert_called_once_with(
        EMPLOYEE_ID,
    )

    employee_profile_repository.get_by_employee_id.assert_called_once_with(
        tenant_id=TENANT_ID,
        employee_id=EMPLOYEE_ID,
    )

    profile.update.assert_called_once_with(
        date_of_birth=command.date_of_birth,
        gender=command.gender,
        nationality=command.nationality,
        marital_status=command.marital_status,
        personal_email=command.personal_email,
        personal_phone=command.personal_phone,
        address_line_1=command.address_line_1,
        address_line_2=command.address_line_2,
        city=command.city,
        state_province=command.state_province,
        postal_code=command.postal_code,
        country_code=command.country_code,
        emergency_contact_name=command.emergency_contact_name,
        emergency_contact_relationship=(
            command.emergency_contact_relationship
        ),
        emergency_contact_phone=command.emergency_contact_phone,
        updated_by=USER_ID,
    )

    employee_profile_repository.save.assert_called_once_with(
        profile,
    )

    unit_of_work.flush.assert_called_once()

    assert result.id == PROFILE_ID
    assert result.employee_id == EMPLOYEE_ID
    assert result.created_at == TEST_NOW


@pytest.mark.anyio
async def test_update_employee_profile_raises_forbidden_when_not_authorized() -> None:
    (
        use_case,
        employee_repository,
        employee_profile_repository,
        authorization_service,
        unit_of_work,
    ) = make_use_case()

    authorization_service.has_permission.return_value = False

    command = make_command()

    with pytest.raises(ForbiddenException):
        await use_case.execute(command)

    authorization_service.has_permission.assert_called_once_with(
        tenant_id=TENANT_ID,
        user_id=USER_ID,
        permission_code="HR_PROFILE_UPDATE",
    )

    employee_repository.get_by_id.assert_not_called()
    employee_profile_repository.get_by_employee_id.assert_not_called()
    employee_profile_repository.save.assert_not_called()
    unit_of_work.flush.assert_not_called()


@pytest.mark.anyio
async def test_update_employee_profile_rejects_unknown_employee() -> None:
    (
        use_case,
        employee_repository,
        employee_profile_repository,
        authorization_service,
        unit_of_work,
    ) = make_use_case()

    authorization_service.has_permission.return_value = True
    employee_repository.get_by_id.return_value = None

    with pytest.raises(ResourceNotFoundException):
        await use_case.execute(make_command())

    employee_profile_repository.get_by_employee_id.assert_not_called()
    employee_profile_repository.save.assert_not_called()
    unit_of_work.flush.assert_not_called()


@pytest.mark.anyio
async def test_update_employee_profile_rejects_employee_from_another_tenant() -> None:
    (
        use_case,
        employee_repository,
        employee_profile_repository,
        authorization_service,
        unit_of_work,
    ) = make_use_case()

    authorization_service.has_permission.return_value = True

    employee = make_employee()
    employee.tenant_id = "01KZYRPZANTQJBZYE7KS4DCRGX"

    employee_repository.get_by_id.return_value = employee

    with pytest.raises(ResourceNotFoundException):
        await use_case.execute(make_command())

    employee_profile_repository.get_by_employee_id.assert_not_called()
    employee_profile_repository.save.assert_not_called()
    unit_of_work.flush.assert_not_called()


@pytest.mark.anyio
async def test_update_employee_profile_rejects_missing_profile() -> None:
    (
        use_case,
        employee_repository,
        employee_profile_repository,
        authorization_service,
        unit_of_work,
    ) = make_use_case()

    authorization_service.has_permission.return_value = True
    employee_repository.get_by_id.return_value = make_employee()
    employee_profile_repository.get_by_employee_id.return_value = None

    with pytest.raises(ResourceNotFoundException):
        await use_case.execute(make_command())

    employee_profile_repository.save.assert_not_called()
    unit_of_work.flush.assert_not_called()