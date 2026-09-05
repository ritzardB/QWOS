from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy import Boolean, Date, String
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity


class EmployeeLeaveAssignment(TenantEntity):
    __tablename__ = "employee_leave_assignments"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("is_active", True)
        super().__init__(**kwargs)

    @classmethod
    def create(
        cls,
        *,
        id: str,
        tenant_id: str,
        employee_id: str,
        leave_policy_id: str,
        effective_from: date,
        effective_until: date | None = None,
        is_active: bool = True,
        created_by: str | None = None,
    ) -> "EmployeeLeaveAssignment":
        if not employee_id.strip():
            raise ValueError("employee_id is required.")

        if not leave_policy_id.strip():
            raise ValueError("leave_policy_id is required.")

        if effective_until is not None and effective_until < effective_from:
            raise ValueError(
                "effective_until must be greater than or equal to effective_from."
            )

        return cls(
            id=id,
            tenant_id=tenant_id,
            employee_id=employee_id,
            leave_policy_id=leave_policy_id,
            effective_from=effective_from,
            effective_until=effective_until,
            is_active=is_active,
            created_by=created_by,
            updated_by=created_by,
        )

    employee_id: Mapped[str] = mapped_column(
        String(26),
        nullable=False,
    )

    leave_policy_id: Mapped[str] = mapped_column(
        String(26),
        nullable=False,
    )

    effective_from: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    effective_until: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )