"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Document Storage

File:
    local_document_storage.py

Description:
    Local filesystem implementation of the DocumentStorage port.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from qwos.application.common.ports.document_storage import (
    DocumentStorage,
    StoredDocument,
)


class LocalDocumentStorage(DocumentStorage):
    """
    Store employee documents on the local filesystem.
    """

    provider_name = "local"

    def __init__(
        self,
        *,
        root_path: str | Path,
    ) -> None:
        self._root_path = Path(root_path).expanduser().resolve()
        self._root_path.mkdir(
            parents=True,
            exist_ok=True,
        )

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

        if not content:
            raise ValueError(
                "Document content cannot be empty."
            )

        normalized_key = storage_key.strip().lstrip("/")

        if not normalized_key:
            raise ValueError(
                "storage_key is required."
            )

        target_path = (
            self._root_path / normalized_key
        ).resolve()

        if not self._is_within_root(target_path):
            raise ValueError(
                "storage_key resolves outside the document storage root."
            )

        target_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        target_path.write_bytes(content)

        checksum_sha256 = hashlib.sha256(
            content,
        ).hexdigest()

        return StoredDocument(
            storage_provider=self.provider_name,
            storage_key=normalized_key,
            stored_filename=filename,
            file_size_bytes=len(content),
            checksum_sha256=checksum_sha256,
        )

    def delete(
        self,
        *,
        storage_key: str,
    ) -> None:
        """
        Delete a stored document.
        """

        normalized_key = storage_key.strip().lstrip("/")

        if not normalized_key:
            raise ValueError(
                "storage_key is required."
            )

        target_path = (
            self._root_path / normalized_key
        ).resolve()

        if not self._is_within_root(target_path):
            raise ValueError(
                "storage_key resolves outside the document storage root."
            )

        if target_path.exists():
            target_path.unlink()

    def _is_within_root(
        self,
        path: Path,
    ) -> bool:
        """
        Prevent path traversal outside the configured storage root.
        """

        try:
            path.relative_to(self._root_path)
        except ValueError:
            return False

        return True