"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

File:
    document_definition_field_repository.py

Description:
    Repository contract for document definition fields.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from qwos.domains.hr.models.document_definition_field import (
    DocumentDefinitionField,
)


class DocumentDefinitionFieldRepository(Protocol):
    """
    Contract for DocumentDefinitionField persistence.
    """

    def get_by_id(
        self,
        field_id: str,
    ) -> DocumentDefinitionField | None:
        """
        Retrieve a field by ID.
        """
        ...

    def save(
        self,
        field: DocumentDefinitionField,
    ) -> None:
        """
        Persist a field.
        """
        ...

    def list_by_definition_id(
        self,
        *,
        document_definition_id: str,
        include_inactive: bool = False,
    ) -> list[DocumentDefinitionField]:
        """
        Retrieve fields belonging to a definition.
        """
        ...
