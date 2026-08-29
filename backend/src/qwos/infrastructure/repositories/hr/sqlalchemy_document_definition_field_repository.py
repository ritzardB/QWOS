"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

HR Module

File:
    sqlalchemy_document_definition_field_repository.py

Description:
    SQLAlchemy repository implementation for document definition fields.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from qwos.domains.hr.models.document_definition_field import (
    DocumentDefinitionField,
)
from qwos.domains.hr.repositories.document_definition_field_repository import (
    DocumentDefinitionFieldRepository,
)


class SQLAlchemyDocumentDefinitionFieldRepository(
    DocumentDefinitionFieldRepository,
):
    """
    SQLAlchemy implementation of DocumentDefinitionFieldRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id(
        self,
        field_id: str,
    ) -> DocumentDefinitionField | None:
        """
        Retrieve a field by ID.
        """

        statement = select(DocumentDefinitionField).where(
            DocumentDefinitionField.id == field_id,
            DocumentDefinitionField.deleted_at.is_(None),
        )

        return self._session.scalar(statement)

    def save(
        self,
        field: DocumentDefinitionField,
    ) -> None:
        """
        Persist a field.
        """

        self._session.add(field)

    def list_by_definition_id(
        self,
        *,
        document_definition_id: str,
        include_inactive: bool = False,
    ) -> list[DocumentDefinitionField]:
        """
        Retrieve fields belonging to a document definition.
        """

        conditions = [
            DocumentDefinitionField.document_definition_id == document_definition_id,
            DocumentDefinitionField.deleted_at.is_(None),
        ]

        if not include_inactive:
            conditions.append(
                DocumentDefinitionField.is_active.is_(True),
            )

        statement = (
            select(DocumentDefinitionField)
            .where(*conditions)
            .order_by(
                DocumentDefinitionField.sort_order.asc(),
                DocumentDefinitionField.field_code.asc(),
            )
        )

        return list(
            self._session.scalars(statement).all(),
        )
