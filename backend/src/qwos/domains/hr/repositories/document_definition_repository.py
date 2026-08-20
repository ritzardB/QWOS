"""
===============================================================================
Quantum Workforce OS (QWOS)

HR Domain

File:
    document_definition_repository.py

Description:
    Repository contract for document definitions.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from qwos.domains.hr.models.document_definition import (
    DocumentDefinition,
)


class DocumentDefinitionRepository(Protocol):
    """
    Contract for DocumentDefinition persistence.
    """

    def get_by_id(
        self,
        definition_id: str,
    ) -> DocumentDefinition | None:
        """
        Retrieve a definition by ID.
        """
        ...

    def save(
        self,
        definition: DocumentDefinition,
    ) -> None:
        """
        Persist a document definition.
        """
        ...

    def list_active(
        self,
        *,
        country_code: str | None = None,
        document_family: str | None = None,
    ) -> list[DocumentDefinition]:
        """
        List active document definitions.
        """
        ...

    def get_by_family(
        self,
        *,
        tenant_id: str | None,
        country_code: str | None,
        document_family: str,
    ) -> DocumentDefinition | None:
        """
        Retrieve a definition by tenant/country/family.
        """
        ...