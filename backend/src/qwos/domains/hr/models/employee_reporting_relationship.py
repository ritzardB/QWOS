"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

File:
    employee_reporting_relationship.py

Description:
    SQLAlchemy model representing employee reporting relationships.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity
from qwos.core.database.types import ULID


class EmployeeReportingRelationship(TenantEntity):
    """
    Represents a reporting relationship between two employees.
    """

    __tablename__ = "employee_reporting_relationships"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("relationship_type", "primary_manager")
        kwargs.setdefault("is_primary", False)

        super().__init__(**kwargs)

    @classmethod
    def create(
        cls,
        *,
        id: str,
        tenant_id: str,
        employee_id: str,
        manager_employee_id: str,
        relationship_type: str = "primary_manager",
        effective_from: date,
        effective_to: date | None = None,
        is_primary: bool = True,
        created_by: str | None = None,
    ) -> "EmployeeReportingRelationship":
        """
        Create a reporting relationship.
        """

        if employee_id == manager_employee_id:
            raise ValueError("An employee cannot report to themselves.")

        return cls(
            id=id,
            tenant_id=tenant_id,
            employee_id=employee_id,
            manager_employee_id=manager_employee_id,
            relationship_type=relationship_type.strip().lower(),
            effective_from=effective_from,
            effective_to=effective_to,
            is_primary=is_primary,
            created_by=created_by,
            updated_by=created_by,
        )

    employee_id: Mapped[str] = mapped_column(
        ULID,
        ForeignKey("employees.id", ondelete="RESTRICT"),
        nullable=False,
    )

    manager_employee_id: Mapped[str] = mapped_column(
        ULID,
        ForeignKey("employees.id", ondelete="RESTRICT"),
        nullable=False,
    )

    relationship_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="primary_manager",
    )

    effective_from: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    effective_to: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    is_primary: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )
