"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

HR Module

File:
    sqlalchemy_document_definition_repository.py

Description:
    SQLAlchemy repository implementation for document definitions.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from qwos.domains.hr.models.document_definition import (
    DocumentDefinition,
)
from qwos.domains.hr.repositories.document_definition_repository import (
    DocumentDefinitionRepository,
)


class SQLAlchemyDocumentDefinitionRepository(
    DocumentDefinitionRepository,
):
    """
    SQLAlchemy implementation of DocumentDefinitionRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id(
        self,
        definition_id: str,
    ) -> DocumentDefinition | None:
        """
        Retrieve a document definition by ID.
        """

        stmt = select(DocumentDefinition).where(
            DocumentDefinition.id == definition_id,
            DocumentDefinition.deleted_at.is_(None),
        )

        return self._session.scalar(stmt)

    def save(
        self,
        definition: DocumentDefinition,
    ) -> None:
        """
        Persist a document definition.
        """

        self._session.add(definition)

    def list_active(
        self,
        *,
        country_code: str | None = None,
        document_family: str | None = None,
    ) -> list[DocumentDefinition]:
        """
        List active document definitions.
        """

        conditions = [
            DocumentDefinition.is_active.is_(True),
            DocumentDefinition.deleted_at.is_(None),
        ]

        if country_code is not None:
            conditions.append(
                DocumentDefinition.country_code == country_code.strip().upper(),
            )

        if document_family is not None:
            conditions.append(
                DocumentDefinition.document_family == document_family.strip().lower(),
            )

        stmt = (
            select(DocumentDefinition)
            .where(*conditions)
            .order_by(
                DocumentDefinition.document_family.asc(),
                DocumentDefinition.country_code.asc(),
                DocumentDefinition.display_name.asc(),
            )
        )

        return list(
            self._session.scalars(stmt).all(),
        )

    def get_by_family(
        self,
        *,
        tenant_id: str | None,
        country_code: str | None,
        document_family: str,
    ) -> DocumentDefinition | None:
        """
        Retrieve the best matching document definition.

        Tenant-specific definitions take precedence over global definitions.
        """

        normalized_family = document_family.strip().lower()

        normalized_country = country_code.strip().upper() if country_code else None

        statements = []

        if tenant_id is not None:
            statements.append(
                select(DocumentDefinition)
                .where(
                    DocumentDefinition.tenant_id == tenant_id,
                    DocumentDefinition.country_code == normalized_country,
                    DocumentDefinition.document_family == normalized_family,
                    DocumentDefinition.is_active.is_(True),
                    DocumentDefinition.deleted_at.is_(None),
                )
                .limit(1)
            )

        if normalized_country is not None:
            statements.append(
                select(DocumentDefinition)
                .where(
                    DocumentDefinition.tenant_id.is_(None),
                    DocumentDefinition.country_code == normalized_country,
                    DocumentDefinition.document_family == normalized_family,
                    DocumentDefinition.is_active.is_(True),
                    DocumentDefinition.deleted_at.is_(None),
                )
                .limit(1)
            )

        statements.append(
            select(DocumentDefinition)
            .where(
                DocumentDefinition.tenant_id.is_(None),
                DocumentDefinition.country_code.is_(None),
                DocumentDefinition.document_family == normalized_family,
                DocumentDefinition.is_active.is_(True),
                DocumentDefinition.deleted_at.is_(None),
            )
            .limit(1)
        )

        for stmt in statements:
            definition = self._session.scalar(stmt)

            if definition is not None:
                return definition

        return None
