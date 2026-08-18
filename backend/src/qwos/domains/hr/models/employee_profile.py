"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

File:
    employee_profile.py

Description:
    SQLAlchemy model representing the core HR profile of an employee.

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


class EmployeeProfile(TenantEntity):
    """
    Stores core personal and contact information for an employee.
    """

    __tablename__ = "employee_profiles"

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
        date_of_birth: date | None = None,
        gender: str | None = None,
        nationality: str | None = None,
        marital_status: str | None = None,
        personal_email: str | None = None,
        personal_phone: str | None = None,
        address_line_1: str | None = None,
        address_line_2: str | None = None,
        city: str | None = None,
        state_province: str | None = None,
        postal_code: str | None = None,
        country_code: str | None = None,
        emergency_contact_name: str | None = None,
        emergency_contact_relationship: str | None = None,
        emergency_contact_phone: str | None = None,
        created_by: str | None = None,
    ) -> "EmployeeProfile":
        """
        Create a new employee profile.
        """

        return cls(
            id=id,
            tenant_id=tenant_id,
            employee_id=employee_id,
            date_of_birth=date_of_birth,
            gender=(
                gender.strip().lower()
                if gender
                else None
            ),
            nationality=(
                nationality.strip().lower()
                if nationality
                else None
            ),
            marital_status=(
                marital_status.strip().lower()
                if marital_status
                else None
            ),
            personal_email=(
                personal_email.strip().lower()
                if personal_email
                else None
            ),
            personal_phone=(
                personal_phone.strip()
                if personal_phone
                else None
            ),
            address_line_1=(
                address_line_1.strip()
                if address_line_1
                else None
            ),
            address_line_2=(
                address_line_2.strip()
                if address_line_2
                else None
            ),
            city=(
                city.strip()
                if city
                else None
            ),
            state_province=(
                state_province.strip()
                if state_province
                else None
            ),
            postal_code=(
                postal_code.strip()
                if postal_code
                else None
            ),
            country_code=(
                country_code.strip().upper()
                if country_code
                else None
            ),
            emergency_contact_name=(
                emergency_contact_name.strip()
                if emergency_contact_name
                else None
            ),
            emergency_contact_relationship=(
                emergency_contact_relationship.strip().lower()
                if emergency_contact_relationship
                else None
            ),
            emergency_contact_phone=(
                emergency_contact_phone.strip()
                if emergency_contact_phone
                else None
            ),
            created_by=created_by,
            updated_by=created_by,
        )

    # -------------------------------------------------------------------------
    # Update
    # -------------------------------------------------------------------------

    def update(
        self,
        *,
        date_of_birth: date | None = None,
        gender: str | None = None,
        nationality: str | None = None,
        marital_status: str | None = None,
        personal_email: str | None = None,
        personal_phone: str | None = None,
        address_line_1: str | None = None,
        address_line_2: str | None = None,
        city: str | None = None,
        state_province: str | None = None,
        postal_code: str | None = None,
        country_code: str | None = None,
        emergency_contact_name: str | None = None,
        emergency_contact_relationship: str | None = None,
        emergency_contact_phone: str | None = None,
        updated_by: str | None = None,
    ) -> None:
        """
        Update the employee profile.
        """

        self.date_of_birth = date_of_birth
        self.gender = (
            gender.strip().lower()
            if gender
            else None
        )
        self.nationality = (
            nationality.strip().lower()
            if nationality
            else None
        )
        self.marital_status = (
            marital_status.strip().lower()
            if marital_status
            else None
        )
        self.personal_email = (
            personal_email.strip().lower()
            if personal_email
            else None
        )
        self.personal_phone = (
            personal_phone.strip()
            if personal_phone
            else None
        )
        self.address_line_1 = (
            address_line_1.strip()
            if address_line_1
            else None
        )
        self.address_line_2 = (
            address_line_2.strip()
            if address_line_2
            else None
        )
        self.city = (
            city.strip()
            if city
            else None
        )
        self.state_province = (
            state_province.strip()
            if state_province
            else None
        )
        self.postal_code = (
            postal_code.strip()
            if postal_code
            else None
        )
        self.country_code = (
            country_code.strip().upper()
            if country_code
            else None
        )
        self.emergency_contact_name = (
            emergency_contact_name.strip()
            if emergency_contact_name
            else None
        )
        self.emergency_contact_relationship = (
            emergency_contact_relationship.strip().lower()
            if emergency_contact_relationship
            else None
        )
        self.emergency_contact_phone = (
            emergency_contact_phone.strip()
            if emergency_contact_phone
            else None
        )
        self.updated_by = updated_by
        
    # -------------------------------------------------------------------------
    # Ownership
    # -------------------------------------------------------------------------

    employee_id: Mapped[str] = mapped_column(
        ULID,
        ForeignKey("employees.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )

    # -------------------------------------------------------------------------
    # Personal Information
    # -------------------------------------------------------------------------

    date_of_birth: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    gender: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    nationality: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    marital_status: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Personal Contact
    # -------------------------------------------------------------------------

    personal_email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    personal_phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Address
    # -------------------------------------------------------------------------

    address_line_1: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    address_line_2: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    state_province: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    postal_code: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    country_code: Mapped[str | None] = mapped_column(
        String(2),
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Emergency Contact
    # -------------------------------------------------------------------------

    emergency_contact_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    emergency_contact_relationship: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    emergency_contact_phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )