from __future__ import annotations

from decimal import Decimal
from typing import Any

from sqlalchemy import Boolean, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity


class LeavePolicy(TenantEntity):
    __tablename__ = "leave_policies"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("entitlement_days", Decimal("0"))
        kwargs.setdefault("accrual_method", "annual")
        kwargs.setdefault("accrual_frequency", "monthly")
        kwargs.setdefault("carry_forward_allowed", False)
        kwargs.setdefault("minimum_service_days", 0)
        kwargs.setdefault("is_active", True)

        super().__init__(**kwargs)

    @classmethod
    def create(
        cls,
        *,
        id: str,
        tenant_id: str,
        leave_type_id: str,
        policy_code: str,
        policy_name: str,
        description: str | None = None,
        entitlement_days: Decimal = Decimal("0"),
        accrual_method: str = "annual",
        accrual_frequency: str = "monthly",
        carry_forward_allowed: bool = False,
        carry_forward_days: Decimal | None = None,
        minimum_service_days: int = 0,
        is_active: bool = True,
        created_by: str | None = None,
    ) -> "LeavePolicy":
        normalized_code = policy_code.strip().lower()
        normalized_name = policy_name.strip()
        normalized_method = accrual_method.strip().lower()
        normalized_frequency = accrual_frequency.strip().lower()

        if not normalized_code:
            raise ValueError("policy_code is required.")

        if not normalized_name:
            raise ValueError("policy_name is required.")

        if not leave_type_id.strip():
            raise ValueError("leave_type_id is required.")

        if not normalized_method:
            raise ValueError("accrual_method is required.")

        if not normalized_frequency:
            raise ValueError("accrual_frequency is required.")

        if entitlement_days < 0:
            raise ValueError("entitlement_days must be greater than or equal to 0.")

        if carry_forward_days is not None and carry_forward_days < 0:
            raise ValueError(
                "carry_forward_days must be greater than or equal to 0."
            )

        if minimum_service_days < 0:
            raise ValueError(
                "minimum_service_days must be greater than or equal to 0."
            )

        normalized_description = (
            description.strip() if description is not None else None
        )

        return cls(
            id=id,
            tenant_id=tenant_id,
            leave_type_id=leave_type_id,
            policy_code=normalized_code,
            policy_name=normalized_name,
            description=normalized_description,
            entitlement_days=entitlement_days,
            accrual_method=normalized_method,
            accrual_frequency=normalized_frequency,
            carry_forward_allowed=carry_forward_allowed,
            carry_forward_days=carry_forward_days,
            minimum_service_days=minimum_service_days,
            is_active=is_active,
            created_by=created_by,
            updated_by=created_by,
        )

    leave_type_id: Mapped[str] = mapped_column(
        String(26),
        nullable=False,
    )

    policy_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    policy_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    entitlement_days: Mapped[Decimal] = mapped_column(
        Numeric(8, 2),
        nullable=False,
        default=Decimal("0"),
    )

    accrual_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="annual",
    )

    accrual_frequency: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="monthly",
    )

    carry_forward_allowed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    carry_forward_days: Mapped[Decimal | None] = mapped_column(
        Numeric(8, 2),
        nullable=True,
    )

    minimum_service_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )