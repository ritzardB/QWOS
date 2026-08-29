"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    employee_work_agreement.py

Description:
    SQLAlchemy model representing an employee's effective work agreement.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Any

from sqlalchemy import Boolean, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity
from qwos.core.database.types import ULID, enum_column


class CompensationBasis(str, Enum):
    """
    Supported compensation bases.
    """

    HOURLY = "hourly"
    DAILY = "daily"
    MONTHLY = "monthly"


class PayFrequency(str, Enum):
    """
    Supported pay frequencies.
    """

    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    SEMIMONTHLY = "semimonthly"
    MONTHLY = "monthly"


class EmployeeWorkAgreement(TenantEntity):
    """
    Represents an employee's effective work agreement.

    Work agreements are effective-dated so that an employee's
    compensation terms can change over time without destroying
    historical data.
    """

    __tablename__ = "employee_work_agreements"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault(
            "compensation_basis",
            CompensationBasis.MONTHLY,
        )
        kwargs.setdefault(
            "pay_frequency",
            PayFrequency.MONTHLY,
        )
        kwargs.setdefault(
            "is_active",
            True,
        )

        super().__init__(**kwargs)

    # -------------------------------------------------------------------------
    # Factory
    # -------------------------------------------------------------------------

    @classmethod
    def create(
        cls,
        *,
        id: str,
        tenant_id: str,
        employee_id: str,
        compensation_basis: str = "monthly",
        pay_frequency: str = "monthly",
        effective_from: date,
        effective_until: date | None = None,
        is_active: bool = True,
        created_by: str | None = None,
    ) -> "EmployeeWorkAgreement":
        """
        Create a normalized employee work agreement.
        """

        normalized_basis = compensation_basis.strip().lower()

        normalized_frequency = pay_frequency.strip().lower()

        if not normalized_basis:
            raise ValueError(
                "compensation_basis is required.",
            )

        if normalized_basis not in {basis.value for basis in CompensationBasis}:
            raise ValueError(
                "compensation_basis must be one of: hourly, daily, monthly.",
            )

        if not normalized_frequency:
            raise ValueError(
                "pay_frequency is required.",
            )

        if normalized_frequency not in {frequency.value for frequency in PayFrequency}:
            raise ValueError(
                "pay_frequency must be one of: weekly, biweekly, semimonthly, monthly.",
            )

        if effective_until is not None and effective_until < effective_from:
            raise ValueError(
                "effective_until cannot be earlier than effective_from.",
            )

        return cls(
            id=id,
            tenant_id=tenant_id,
            employee_id=employee_id,
            compensation_basis=normalized_basis,
            pay_frequency=normalized_frequency,
            effective_from=effective_from,
            effective_until=effective_until,
            is_active=is_active,
            created_by=created_by,
            updated_by=created_by,
        )

    # -------------------------------------------------------------------------
    # Employee
    # -------------------------------------------------------------------------

    employee_id: Mapped[str] = mapped_column(
        ULID,
        ForeignKey(
            "employees.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Compensation
    # -------------------------------------------------------------------------

    compensation_basis: Mapped[CompensationBasis] = mapped_column(
        enum_column(CompensationBasis),
        nullable=False,
        default=CompensationBasis.MONTHLY,
    )

    pay_frequency: Mapped[PayFrequency] = mapped_column(
        enum_column(PayFrequency),
        nullable=False,
        default=PayFrequency.MONTHLY,
    )

    # -------------------------------------------------------------------------
    # Effective Dating
    # -------------------------------------------------------------------------

    effective_from: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    effective_until: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
