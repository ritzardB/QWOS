"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

File:
    document_extraction_result.py

Description:
    SQLAlchemy model representing a machine-extracted document field value.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity
from qwos.core.database.types import ULID


class DocumentExtractionResult(TenantEntity):
    """
    Stores a machine-extracted value from an employee document.

    Extraction results are evidence produced by an extraction engine.
    They are not automatically approved HR values.
    """

    __tablename__ = "document_extraction_results"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    @classmethod
    def create(
        cls,
        *,
        id: str,
        tenant_id: str,
        employee_document_id: str,
        document_definition_field_id: str,
        raw_value: str | None = None,
        normalized_value: str | None = None,
        confidence: float | None = None,
        source: str,
        extracted_at: datetime | None = None,
        created_by: str | None = None,
    ) -> "DocumentExtractionResult":
        """
        Create a normalized document extraction result.
        """

        normalized_source = source.strip().lower()

        if not normalized_source:
            raise ValueError(
                "source is required.",
            )

        if confidence is not None and not (0.0 <= confidence <= 1.0):
            raise ValueError(
                "confidence must be between 0.0 and 1.0.",
            )

        return cls(
            id=id,
            tenant_id=tenant_id,
            employee_document_id=employee_document_id,
            document_definition_field_id=(document_definition_field_id),
            raw_value=raw_value,
            normalized_value=normalized_value,
            confidence=confidence,
            source=normalized_source,
            extracted_at=(extracted_at or datetime.now(timezone.utc)),
            created_by=created_by,
            updated_by=created_by,
        )

    # -------------------------------------------------------------------------
    # Ownership
    # -------------------------------------------------------------------------

    employee_document_id: Mapped[str] = mapped_column(
        ULID,
        ForeignKey(
            "employee_documents.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    document_definition_field_id: Mapped[str] = mapped_column(
        ULID,
        ForeignKey(
            "document_definition_fields.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Extracted Values
    # -------------------------------------------------------------------------

    raw_value: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    normalized_value: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Extraction Metadata
    # -------------------------------------------------------------------------

    confidence: Mapped[float | None] = mapped_column(
        Numeric(5, 4),
        nullable=True,
    )

    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    extracted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
