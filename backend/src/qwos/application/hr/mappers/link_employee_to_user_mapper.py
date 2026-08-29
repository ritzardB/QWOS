"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    link_employee_to_user_mapper.py

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.requests.hr.link_employee_to_user_request import (
    LinkEmployeeToUserRequest,
)
from qwos.api.contracts.responses.hr.link_employee_to_user_response import (
    LinkEmployeeToUserResponse,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.hr.commands.link_employee_to_user_command import (
    LinkEmployeeToUserCommand,
)
from qwos.application.hr.responses.link_employee_to_user_response import (
    LinkEmployeeToUserResponse as ApplicationLinkEmployeeToUserResponse,
)


class LinkEmployeeToUserMapper:
    """
    Maps Link Employee to User API contracts.
    """

    @staticmethod
    def to_command(
        *,
        employee_id: str,
        request: LinkEmployeeToUserRequest,
        request_context: RequestContext,
    ) -> LinkEmployeeToUserCommand:
        """
        Convert an API request into an application command.
        """

        return LinkEmployeeToUserCommand(
            tenant_id=request_context.tenant_id,
            employee_id=employee_id,
            user_id=request.user_id,
            first_name=request.first_name,
            middle_name=request.middle_name,
            last_name=request.last_name,
            preferred_name=request.preferred_name,
        )

    @staticmethod
    def to_response(
        response: ApplicationLinkEmployeeToUserResponse,
    ) -> LinkEmployeeToUserResponse:
        """
        Convert an application response into an API response.
        """

        return LinkEmployeeToUserResponse(
            employee_id=response.employee_id,
            employee_number=response.employee_number,
            user_id=response.user_id,
            profile_id=response.profile_id,
            display_name=response.display_name,
            preferred_name=response.preferred_name,
            updated_at=response.updated_at,
        )
