"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    employee_profile_mapper.py

Description:
    Maps Employee Profile API contracts to application commands and responses.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.requests.hr.create_employee_profile_request import (
    CreateEmployeeProfileRequest,
)
from qwos.api.contracts.responses.hr.create_employee_profile_response import (
    CreateEmployeeProfileResponse,
)
from qwos.api.contracts.responses.hr.get_employee_profile_response import (
    GetEmployeeProfileResponse,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.hr.commands.create_employee_profile_command import (
    CreateEmployeeProfileCommand,
)
from qwos.application.hr.responses.create_employee_profile_response import (
    CreateEmployeeProfileResponse as ApplicationCreateEmployeeProfileResponse,
)
from qwos.application.hr.responses.get_employee_profile_response import (
    GetEmployeeProfileResponse as ApplicationGetEmployeeProfileResponse,
)


class EmployeeProfileMapper:
    """
    Maps Employee Profile API contracts to application objects.
    """

    @staticmethod
    def to_create_command(
        *,
        employee_id: str,
        request: CreateEmployeeProfileRequest,
        request_context: RequestContext,
    ) -> CreateEmployeeProfileCommand:
        """
        Convert an API request into a CreateEmployeeProfileCommand.
        """

        return CreateEmployeeProfileCommand(
            tenant_id=request_context.tenant_id,
            employee_id=employee_id,
            date_of_birth=request.date_of_birth,
            gender=request.gender,
            nationality=request.nationality,
            marital_status=request.marital_status,
            personal_email=(
                str(request.personal_email)
                if request.personal_email is not None
                else None
            ),
            personal_phone=request.personal_phone,
            address_line_1=request.address_line_1,
            address_line_2=request.address_line_2,
            city=request.city,
            state_province=request.state_province,
            postal_code=request.postal_code,
            country_code=request.country_code,
            emergency_contact_name=request.emergency_contact_name,
            emergency_contact_relationship=(
                request.emergency_contact_relationship
            ),
            emergency_contact_phone=request.emergency_contact_phone,
        )

    @staticmethod
    def to_create_response(
        response: ApplicationCreateEmployeeProfileResponse,
    ) -> CreateEmployeeProfileResponse:
        """
        Convert an application response into an API response.
        """

        return CreateEmployeeProfileResponse(
            id=response.id,
            employee_id=response.employee_id,
            date_of_birth=response.date_of_birth,
            gender=response.gender,
            nationality=response.nationality,
            marital_status=response.marital_status,
            personal_email=response.personal_email,
            personal_phone=response.personal_phone,
            address_line_1=response.address_line_1,
            address_line_2=response.address_line_2,
            city=response.city,
            state_province=response.state_province,
            postal_code=response.postal_code,
            country_code=response.country_code,
            emergency_contact_name=response.emergency_contact_name,
            emergency_contact_relationship=(
                response.emergency_contact_relationship
            ),
            emergency_contact_phone=response.emergency_contact_phone,
            created_at=response.created_at,
        )

    @staticmethod
    def to_get_response(
        response: ApplicationGetEmployeeProfileResponse,
    ) -> GetEmployeeProfileResponse:
        """
        Convert an application employee profile response
        into an API response.
        """

        return GetEmployeeProfileResponse(
            id=response.id,
            employee_id=response.employee_id,
            date_of_birth=response.date_of_birth,
            gender=response.gender,
            nationality=response.nationality,
            marital_status=response.marital_status,
            personal_email=response.personal_email,
            personal_phone=response.personal_phone,
            address_line_1=response.address_line_1,
            address_line_2=response.address_line_2,
            city=response.city,
            state_province=response.state_province,
            postal_code=response.postal_code,
            country_code=response.country_code,
            emergency_contact_name=response.emergency_contact_name,
            emergency_contact_relationship=(
                response.emergency_contact_relationship
            ),
            emergency_contact_phone=response.emergency_contact_phone,
            created_at=response.created_at,
        )