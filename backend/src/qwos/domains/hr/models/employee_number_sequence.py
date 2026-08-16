"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

File:
    employee_number_sequence.py

Description:
    SQLAlchemy model representing tenant-specific employee number generation
    configuration.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import BigInteger, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity


class EmployeeNumberSequence(TenantEntity):
    """
    Stores employee-number generation configuration for a tenant.
    """

    __tablename__ = "employee_number_sequences"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("separator", "-")
        kwargs.setdefault("padding_length", 5)
        kwargs.setdefault("next_number", 1)
        kwargs.setdefault("is_active", True)

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
        prefix: str,
        separator: str = "-",
        padding_length: int = 5,
        next_number: int = 1,
        created_by: str | None = None,
    ) -> "EmployeeNumberSequence":
        """
        Create a new tenant employee-number sequence.
        """

        return cls(
            id=id,
            tenant_id=tenant_id,
            prefix=prefix.strip().upper(),
            separator=separator,
            padding_length=padding_length,
            next_number=next_number,
            created_by=created_by,
            updated_by=created_by,
        )

    # -------------------------------------------------------------------------
    # Configuration
    # -------------------------------------------------------------------------

    prefix: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    separator: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="-",
    )

    padding_length: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=5,
    )

    next_number: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        default=1,
    )

    # -------------------------------------------------------------------------
    # Status
    # -------------------------------------------------------------------------

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
