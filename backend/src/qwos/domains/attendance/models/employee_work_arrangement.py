"""
===============================================================================
Quantum Workforce OS (QWOS)

Attendance Domain

File:
    employee_work_arrangement.py

Description:
    SQLAlchemy model representing an employee's effective work arrangement.

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


class WorkArrangement(str, Enum):
    """
    Supported employee work arrangements.
    """

    OFFICE = "office"
    HYBRID = "hybrid"
    REMOTE = "remote"


class EmployeeWorkArrangement(TenantEntity):
    """
    Represents an employee's effective work arrangement.

    Work arrangements are effective-dated so that an employee's
    arrangement can change over time without destroying historical data.
    """

    __tablename__ = "employee_work_arrangements"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault(
            "work_arrangement",
            WorkArrangement.OFFICE,
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
        work_arrangement: str = "office",
        effective_from: date,
        effective_until: date | None = None,
        is_active: bool = True,
        created_by: str | None = None,
    ) -> "EmployeeWorkArrangement":
        """
        Create a normalized employee work arrangement.
        """

        normalized_arrangement = (
            work_arrangement.strip().lower()
        )

        if not normalized_arrangement:
            raise ValueError(
                "work_arrangement is required.",
            )

        if normalized_arrangement not in {
            arrangement.value
            for arrangement in WorkArrangement
        }:
            raise ValueError(
                "work_arrangement must be one of: "
                "office, hybrid, remote.",
            )

        if (
            effective_until is not None
            and effective_until < effective_from
        ):
            raise ValueError(
                "effective_until cannot be earlier than "
                "effective_from.",
            )

        return cls(
            id=id,
            tenant_id=tenant_id,
            employee_id=employee_id,
            work_arrangement=(
                normalized_arrangement
            ),
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
    # Work Arrangement
    # -------------------------------------------------------------------------

    work_arrangement: Mapped[WorkArrangement] = mapped_column(
        enum_column(WorkArrangement),
        nullable=False,
        default=WorkArrangement.OFFICE,
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
