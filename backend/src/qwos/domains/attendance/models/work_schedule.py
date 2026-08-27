from __future__ import annotations

from typing import Any

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from qwos.core.database.entity_base import TenantEntity


class WorkSchedule(TenantEntity):
    """
    Represents a reusable employee work schedule definition.
    """

    __tablename__ = "work_schedules"

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault(
            "timezone",
            "UTC",
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
        schedule_code: str,
        schedule_name: str,
        timezone: str = "UTC",
        is_active: bool = True,
        created_by: str | None = None,
    ) -> "WorkSchedule":
        """
        Create a normalized work schedule definition.
        """

        normalized_code = schedule_code.strip().lower()
        normalized_name = schedule_name.strip()
        normalized_timezone = timezone.strip()

        if not normalized_code:
            raise ValueError(
                "schedule_code is required.",
            )

        if not normalized_name:
            raise ValueError(
                "schedule_name is required.",
            )

        if not normalized_timezone:
            raise ValueError(
                "timezone is required.",
            )

        return cls(
            id=id,
            tenant_id=tenant_id,
            schedule_code=normalized_code,
            schedule_name=normalized_name,
            timezone=normalized_timezone,
            is_active=is_active,
            created_by=created_by,
            updated_by=created_by,
        )

    # -------------------------------------------------------------------------
    # Schedule Identity
    # -------------------------------------------------------------------------

    schedule_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    schedule_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Timezone
    # -------------------------------------------------------------------------

    timezone: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="UTC",
    )

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )