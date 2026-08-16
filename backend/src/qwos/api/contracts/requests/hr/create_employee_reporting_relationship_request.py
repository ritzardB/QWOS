from __future__ import annotations

from datetime import date

from pydantic import Field

from qwos.api.contracts.requests.common.base_request import BaseRequest


class CreateEmployeeReportingRelationshipRequest(BaseRequest):
    manager_employee_id: str = Field(
        min_length=26,
        max_length=26,
    )

    relationship_type: str = Field(
        default="primary_manager",
        min_length=2,
        max_length=50,
    )

    effective_from: date

    effective_to: date | None = None

    is_primary: bool = True