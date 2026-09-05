from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any

from sqlalchemy import Boolean, Date, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity


class EmployeeLeaveBalance(TenantEntity):
    __tablename__ = "employee_leave_balances"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("entitlement_days", Decimal("0"))
        kwargs.setdefault("carried_forward_days", Decimal("0"))
        kwargs.setdefault("accrued_days", Decimal("0"))
        kwargs.setdefault("used_days", Decimal("0"))
        kwargs.setdefault("adjustment_days", Decimal("0"))
        kwargs.setdefault("is_active", True)
        super().__init__(**kwargs)

    @classmethod
    def create(
        cls,
        *,
        id: str,
        tenant_id: str,
        employee_leave_assignment_id: str,
        employee_id: str,
        period_start: date,
        period_end: date,
        entitlement_days: Decimal = Decimal("0"),
        carried_forward_days: Decimal = Decimal("0"),
        accrued_days: Decimal = Decimal("0"),
        used_days: Decimal = Decimal("0"),
        adjustment_days: Decimal = Decimal("0"),
        is_active: bool = True,
        created_by: str | None = None,
    ) -> "EmployeeLeaveBalance":
        if not employee_leave_assignment_id.strip():
            raise ValueError("employee_leave_assignment_id is required.")

        if not employee_id.strip():
            raise ValueError("employee_id is required.")

        if period_end < period_start:
            raise ValueError(
                "period_end must be greater than or equal to period_start."
            )

        if entitlement_days < 0:
            raise ValueError("entitlement_days must be greater than or equal to 0.")

        if carried_forward_days < 0:
            raise ValueError(
                "carried_forward_days must be greater than or equal to 0."
            )

        if accrued_days < 0:
            raise ValueError("accrued_days must be greater than or equal to 0.")

        if used_days < 0:
            raise ValueError("used_days must be greater than or equal to 0.")

        return cls(
            id=id,
            tenant_id=tenant_id,
            employee_leave_assignment_id=employee_leave_assignment_id,
            employee_id=employee_id,
            period_start=period_start,
            period_end=period_end,
            entitlement_days=entitlement_days,
            carried_forward_days=carried_forward_days,
            accrued_days=accrued_days,
            used_days=used_days,
            adjustment_days=adjustment_days,
            is_active=is_active,
            created_by=created_by,
            updated_by=created_by,
        )

    employee_leave_assignment_id: Mapped[str] = mapped_column(
        String(26),
        nullable=False,
    )

    employee_id: Mapped[str] = mapped_column(
        String(26),
        nullable=False,
    )

    period_start: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    period_end: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    entitlement_days: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0"),
    )

    carried_forward_days: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0"),
    )

    accrued_days: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0"),
    )

    used_days: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0"),
    )

    adjustment_days: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0"),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )