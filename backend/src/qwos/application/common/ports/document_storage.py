"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Port

File:
    document_storage.py

Description:
    Abstraction for storing and retrieving employee documents.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class StoredDocument:
    """
    Result returned after a document has been stored.
    """

    storage_provider: str
    storage_key: str
    stored_filename: str
    file_size_bytes: int
    checksum_sha256: str


@dataclass(frozen=True)
class RetrievedDocument:
    """
    Result returned when document content is retrieved.
    """

    content: bytes
    filename: str
    mime_type: str | None


class DocumentStorage(Protocol):
    """
    Port for document storage implementations.
    """

    def store(
        self,
        *,
        content: bytes,
        storage_key: str,
        filename: str,
        mime_type: str | None = None,
    ) -> StoredDocument:
        """
        Persist document content and return storage metadata.
        """
        ...

    def read(
        self,
        *,
        storage_key: str,
    ) -> RetrievedDocument:
        """
        Retrieve document content from storage.
        """
        ...

    def delete(
        self,
        *,
        storage_key: str,
    ) -> None:
        """
        Delete a stored document.
        """
        ...
