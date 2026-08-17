"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    get_employee_profile_use_case.py

Description:
    Use case for retrieving an employee HR profile.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.hr.responses.get_employee_profile_response import (
    GetEmployeeProfileResponse,
)
from qwos.domains.hr.repositories.employee_profile_repository import (
    EmployeeProfileRepository,
)


class GetEmployeeProfileUseCase:
    """
    Retrieve an employee's HR profile within the current tenant.
    """

    def __init__(
        self,
        *,
        employee_profile_repository: EmployeeProfileRepository,
    ) -> None:
        self._employee_profile_repository = (
            employee_profile_repository
        )

    async def execute(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> GetEmployeeProfileResponse:
        """
        Retrieve the employee profile.
        """

        profile = (
            self._employee_profile_repository.get_by_employee_id(
                tenant_id=tenant_id,
                employee_id=employee_id,
            )
        )

        if profile is None:
            raise ResourceNotFoundException(
                resource="EmployeeProfile",
                identifier=employee_id,
            )

        return GetEmployeeProfileResponse(
            id=profile.id,
            employee_id=profile.employee_id,
            date_of_birth=profile.date_of_birth,
            gender=profile.gender,
            nationality=profile.nationality,
            marital_status=profile.marital_status,
            personal_email=profile.personal_email,
            personal_phone=profile.personal_phone,
            address_line_1=profile.address_line_1,
            address_line_2=profile.address_line_2,
            city=profile.city,
            state_province=profile.state_province,
            postal_code=profile.postal_code,
            country_code=profile.country_code,
            emergency_contact_name=profile.emergency_contact_name,
            emergency_contact_relationship=(
                profile.emergency_contact_relationship
            ),
            emergency_contact_phone=profile.emergency_contact_phone,
            created_at=profile.created_at,
        )