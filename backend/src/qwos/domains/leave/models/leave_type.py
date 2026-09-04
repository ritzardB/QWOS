"""
===============================================================================
Quantum Workforce OS (QWOS)

Domain Layer

Leave Type

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity


class LeaveType(TenantEntity):
    """
    Tenant-defined leave type master definition.

    LeaveType represents WHAT kind of leave exists.

    Entitlement, accrual, carry-forward, eligibility, and approval
    rules belong to Leave Policy and related Leave domain entities.
    """

    __tablename__ = "leave_types"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("is_paid", True)
        kwargs.setdefault("is_active", True)
        super().__init__(**kwargs)

    @classmethod
    def create(
        cls,
        *,
        id: str,
        tenant_id: str,
        leave_code: str,
        leave_name: str,
        description: str | None = None,
        is_paid: bool = True,
        is_active: bool = True,
        created_by: str | None = None,
    ) -> "LeaveType":
        """
        Create a new tenant leave type.
        """

        normalized_code = leave_code.strip().lower()
        normalized_name = leave_name.strip()

        if not normalized_code:
            raise ValueError("leave_code is required.")

        if not normalized_name:
            raise ValueError("leave_name is required.")

        normalized_description = (
            description.strip()
            if description is not None
            else None
        )

        return cls(
            id=id,
            tenant_id=tenant_id,
            leave_code=normalized_code,
            leave_name=normalized_name,
            description=normalized_description,
            is_paid=is_paid,
            is_active=is_active,
            created_by=created_by,
            updated_by=created_by,
        )

    leave_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    leave_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_paid: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )