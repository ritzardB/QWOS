"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

File:
    employee_document.py

Description:
    SQLAlchemy model representing an employee HR document.

    The model stores document metadata and the storage reference. Physical
    file contents are managed by the infrastructure storage layer.

    QWOS controls the standardized stored filename used for persisted files.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import re
from typing import Any

from sqlalchemy import BigInteger, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity
from qwos.core.database.types import ULID


class EmployeeDocument(TenantEntity):
    """
    Stores metadata for an employee HR document.
    """

    __tablename__ = "employee_documents"

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
        document_name: str,
        document_category: str,
        original_filename: str,
        stored_filename: str,
        mime_type: str | None = None,
        file_extension: str | None = None,
        file_size_bytes: int,
        storage_provider: str,
        storage_key: str,
        checksum_sha256: str,
        document_version: int = 1,
        uploaded_by: str | None = None,
        created_by: str | None = None,
        immigration_id: str | None = None,
    ) -> "EmployeeDocument":
        """
        Create a normalized employee document entity.
        """

        normalized_checksum = checksum_sha256.strip().lower()

        if not re.fullmatch(
            r"[0-9a-f]{64}",
            normalized_checksum,
        ):
            raise ValueError(
                "checksum_sha256 must be a valid SHA-256 hexadecimal value."
            )

        if file_size_bytes <= 0:
            raise ValueError(
                "file_size_bytes must be greater than zero."
            )

        if document_version <= 0:
            raise ValueError(
                "document_version must be greater than zero."
            )

        return cls(
            id=id,
            tenant_id=tenant_id,
            employee_id=employee_id,
            immigration_id=immigration_id,
            document_name=document_name.strip(),
            document_category=(
                document_category.strip().lower()
            ),
            original_filename=original_filename.strip(),
            stored_filename=stored_filename.strip(),
            mime_type=(
                mime_type.strip().lower()
                if mime_type
                else None
            ),
            file_extension=(
                file_extension.strip().lower().lstrip(".")
                if file_extension
                else None
            ),
            file_size_bytes=file_size_bytes,
            storage_provider=storage_provider.strip().lower(),
            storage_key=storage_key.strip(),
            checksum_sha256=normalized_checksum,
            document_version=document_version,
            uploaded_by=uploaded_by,
            created_by=created_by,
            updated_by=created_by,
        )

    # -------------------------------------------------------------------------
    # Storage / Identity
    # -------------------------------------------------------------------------

    employee_id: Mapped[str] = mapped_column(
        ULID,
        ForeignKey(
            "employees.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    immigration_id: Mapped[str | None] = mapped_column(
        ULID,
        ForeignKey(
            "employee_immigration.id",
            ondelete="RESTRICT",
        ),
        nullable=True,
    )

    document_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    document_category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    stored_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    mime_type: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    file_extension: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    file_size_bytes: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Storage Reference
    # -------------------------------------------------------------------------

    storage_provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    storage_key: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Integrity
    # -------------------------------------------------------------------------

    checksum_sha256: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Document Lifecycle
    # -------------------------------------------------------------------------

    document_version: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
    )