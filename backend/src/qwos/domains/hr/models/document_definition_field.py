"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

File:
    document_definition_field.py

Description:
    SQLAlchemy model representing a field supported by a document definition.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity
from qwos.core.database.types import ULID


class DocumentDefinitionField(TenantEntity):
    """
    Defines a structured field belonging to a document definition.
    """

    __tablename__ = "document_definition_fields"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    @classmethod
    def create(
        cls,
        *,
        id: str,
        tenant_id: str | None = None,
        document_definition_id: str,
        field_code: str,
        field_label: str,
        data_type: str,
        is_required: bool = False,
        is_extractable: bool = True,
        sort_order: int = 0,
        validation_pattern: str | None = None,
        is_active: bool = True,
        created_by: str | None = None,
    ) -> "DocumentDefinitionField":
        """
        Create a normalized document definition field.
        """

        normalized_code = field_code.strip().lower()
        normalized_label = field_label.strip()
        normalized_type = data_type.strip().lower()

        if not normalized_code:
            raise ValueError(
                "field_code is required.",
            )

        if not normalized_label:
            raise ValueError(
                "field_label is required.",
            )

        if not normalized_type:
            raise ValueError(
                "data_type is required.",
            )

        if sort_order < 0:
            raise ValueError(
                "sort_order cannot be negative.",
            )

        return cls(
            id=id,
            tenant_id=tenant_id,
            document_definition_id=document_definition_id,
            field_code=normalized_code,
            field_label=normalized_label,
            data_type=normalized_type,
            is_required=is_required,
            is_extractable=is_extractable,
            sort_order=sort_order,
            validation_pattern=(
                validation_pattern.strip()
                if validation_pattern
                else None
            ),
            is_active=is_active,
            created_by=created_by,
            updated_by=created_by,
        )

    document_definition_id: Mapped[str] = mapped_column(
        ULID,
        ForeignKey(
            "document_definitions.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    field_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    field_label: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    data_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    is_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    is_extractable: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    validation_pattern: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )