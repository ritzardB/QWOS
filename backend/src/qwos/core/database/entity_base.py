"""
===============================================================================
Quantum Workforce OS (QWOS)

File:
    base.py

Description:
    SQLAlchemy Declarative Base and BaseEntity.

Author:
    Richard Balabarcon

===============================================================================
"""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Root SQLAlchemy declarative base.
    """

    pass


class BaseEntity(Base):
    """
    Base class for all QWOS entities.

    Provides:

    • Audit timestamps
    • Versioning
    """

    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(26),
        primary_key=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    created_by: Mapped[str | None] = mapped_column(
        String(26),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    updated_by: Mapped[str | None] = mapped_column(
        String(26),
        nullable=False,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    deleted_by: Mapped[str | None] = mapped_column(
        String(26),
        nullable=True,
    )

    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )


class TenantEntity(BaseEntity):
    """
    Base class for tenant-owned entities.
    """

    __abstract__ = True

    tenant_id: Mapped[str] = mapped_column(
        String(26),
        nullable=False,
        index=True,
    )
