"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Leave Module

File:
    leave_type_mapper.py

Description:
    Maps Leave Type application responses to API contracts.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.requests.leave.create_leave_type_request import (
    CreateLeaveTypeRequest,
)
from qwos.api.contracts.responses.leave.create_leave_type_response import (
    CreateLeaveTypeResponse,
)
from qwos.application.common.context.request_context import RequestContext
from qwos.application.leave.commands.create_leave_type_command import (
    CreateLeaveTypeCommand,
)
from qwos.application.leave.responses.create_leave_type_response import (
    CreateLeaveTypeResponse as ApplicationCreateLeaveTypeResponse,
)


class LeaveTypeMapper:
    """
    Maps Leave Type application objects to API contracts.
    """

    @staticmethod
    def to_create_response(
        response: ApplicationCreateLeaveTypeResponse,
    ) -> CreateLeaveTypeResponse:
        """
        Convert a create application response into an API response.
        """

        return CreateLeaveTypeResponse(
            id=response.id,
            leave_code=response.leave_code,
            leave_name=response.leave_name,
            description=response.description,
            is_paid=response.is_paid,
            is_active=response.is_active,
            created_at=response.created_at,
        )

    @staticmethod
    def to_create_command(
        *,
        request: CreateLeaveTypeRequest,
        request_context: RequestContext,
    ) -> CreateLeaveTypeCommand:
        """
        Convert an API request into a create command.
        """

        return CreateLeaveTypeCommand(
            tenant_id=request_context.tenant_id,
            leave_code=request.leave_code,
            leave_name=request.leave_name,
            description=request.description,
            is_paid=request.is_paid,
            is_active=request.is_active,
        )