"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

File:
    employee_immigration.py

Description:
    SQLAlchemy model representing an employee immigration record.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity
from qwos.core.database.types import ULID


class EmployeeImmigration(TenantEntity):
    """
    Stores an employee immigration or work-authorization record.

    Multiple historical records are supported for the same employee.
    """

    __tablename__ = "employee_immigration"

    def __init__(self, **kwargs: Any) -> None:
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
        immigration_type: str,
        status: str,
        document_number: str | None = None,
        sponsor_name: str | None = None,
        issuing_authority: str | None = None,
        issue_date: date | None = None,
        expiry_date: date | None = None,
        notes: str | None = None,
        created_by: str | None = None,
    ) -> "EmployeeImmigration":
        """
        Create a new employee immigration record.
        """

        return cls(
            id=id,
            tenant_id=tenant_id,
            employee_id=employee_id,
            immigration_type=immigration_type.strip().lower(),
            status=status.strip().lower(),
            document_number=(
                document_number.strip()
                if document_number
                else None
            ),
            sponsor_name=(
                sponsor_name.strip()
                if sponsor_name
                else None
            ),
            issuing_authority=(
                issuing_authority.strip()
                if issuing_authority
                else None
            ),
            issue_date=issue_date,
            expiry_date=expiry_date,
            notes=(
                notes.strip()
                if notes
                else None
            ),
            created_by=created_by,
            updated_by=created_by,
        )

    # -------------------------------------------------------------------------
    # Ownership
    # -------------------------------------------------------------------------

    employee_id: Mapped[str] = mapped_column(
        ULID,
        ForeignKey("employees.id", ondelete="RESTRICT"),
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Immigration Record
    # -------------------------------------------------------------------------

    immigration_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    document_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Sponsorship / Authority
    # -------------------------------------------------------------------------

    sponsor_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    issuing_authority: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Dates
    # -------------------------------------------------------------------------

    issue_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    expiry_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Additional Information
    # -------------------------------------------------------------------------

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )