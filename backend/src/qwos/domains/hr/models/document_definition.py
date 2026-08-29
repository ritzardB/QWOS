"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

File:
    document_definition.py

Description:
    SQLAlchemy model representing a generic QWOS document definition.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity


class DocumentDefinition(TenantEntity):
    """
    Defines a generic QWOS document family and its country/tenant label.

    Examples:

        national_id / AE / Emirates ID

        national_id / PH / PhilSys National ID
    """

    __tablename__ = "document_definitions"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    @classmethod
    def create(
        cls,
        *,
        id: str,
        tenant_id: str | None = None,
        country_code: str | None = None,
        document_family: str,
        display_name: str,
        is_active: bool = True,
        created_by: str | None = None,
    ) -> "DocumentDefinition":
        """
        Create a normalized document definition.
        """

        normalized_family = document_family.strip().lower()

        normalized_country = country_code.strip().upper() if country_code else None

        normalized_display_name = display_name.strip()

        if not normalized_family:
            raise ValueError(
                "document_family is required.",
            )

        if not normalized_display_name:
            raise ValueError(
                "display_name is required.",
            )

        if normalized_country is not None:
            if len(normalized_country) != 2 or not normalized_country.isalpha():
                raise ValueError(
                    "country_code must be a valid ISO 3166-1 alpha-2 code.",
                )

        return cls(
            id=id,
            tenant_id=tenant_id,
            country_code=normalized_country,
            document_family=normalized_family,
            display_name=normalized_display_name,
            is_active=is_active,
            created_by=created_by,
            updated_by=created_by,
        )

    # -------------------------------------------------------------------------
    # Definition
    # -------------------------------------------------------------------------

    document_family: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    display_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    country_code: Mapped[str | None] = mapped_column(
        String(2),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
