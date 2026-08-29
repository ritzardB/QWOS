from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class CreateEmployeeReportingRelationshipCommand:
    """
    Command for creating an employee reporting relationship.
    """

    tenant_id: str
    employee_id: str
    manager_employee_id: str
    effective_from: date

    relationship_type: str = "primary_manager"
    effective_to: date | None = None
    is_primary: bool = True
