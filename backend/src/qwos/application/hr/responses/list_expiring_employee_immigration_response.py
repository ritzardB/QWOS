from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class ExpiringEmployeeImmigrationItem:
    id: str
    employee_id: str
    immigration_type: str
    status: str
    document_number: str | None
    issue_date: date | None
    expiry_date: date
    days_until_expiry: int


@dataclass(frozen=True, slots=True)
class ListExpiringEmployeeImmigrationResponse:
    items: list[ExpiringEmployeeImmigrationItem]