"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_local_document_storage.py

Description:
    Unit tests for LocalDocumentStorage.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from qwos.infrastructure.storage.local_document_storage import (
    LocalDocumentStorage,
)


def test_store_writes_file_and_returns_metadata(
    tmp_path: Path,
) -> None:
    storage = LocalDocumentStorage(
        root_path=tmp_path,
    )

    content = b"QWOS document test"

    result = storage.store(
        content=content,
        storage_key=(
            "employees/QW-00002/documents/"
            "passport/QW-00002_PASSPORT_V01.pdf"
        ),
        filename="QW-00002_PASSPORT_V01.pdf",
        mime_type="application/pdf",
    )

    expected_checksum = hashlib.sha256(
        content,
    ).hexdigest()

    expected_path = (
        tmp_path
        / "employees"
        / "QW-00002"
        / "documents"
        / "passport"
        / "QW-00002_PASSPORT_V01.pdf"
    )

    assert expected_path.exists()
    assert expected_path.read_bytes() == content

    assert result.storage_provider == "local"
    assert (
        result.storage_key
        == (
            "employees/QW-00002/documents/"
            "passport/QW-00002_PASSPORT_V01.pdf"
        )
    )
    assert result.stored_filename == (
        "QW-00002_PASSPORT_V01.pdf"
    )
    assert result.file_size_bytes == len(content)
    assert result.checksum_sha256 == expected_checksum


def test_store_rejects_empty_content(
    tmp_path: Path,
) -> None:
    storage = LocalDocumentStorage(
        root_path=tmp_path,
    )

    with pytest.raises(
        ValueError,
        match="content cannot be empty",
    ):
        storage.store(
            content=b"",
            storage_key="employees/QW-00002/test.pdf",
            filename="test.pdf",
        )


def test_store_rejects_empty_storage_key(
    tmp_path: Path,
) -> None:
    storage = LocalDocumentStorage(
        root_path=tmp_path,
    )

    with pytest.raises(
        ValueError,
        match="storage_key is required",
    ):
        storage.store(
            content=b"test",
            storage_key="",
            filename="test.pdf",
        )


def test_store_rejects_path_traversal(
    tmp_path: Path,
) -> None:
    storage = LocalDocumentStorage(
        root_path=tmp_path,
    )

    with pytest.raises(
        ValueError,
        match="outside the document storage root",
    ):
        storage.store(
            content=b"test",
            storage_key="../../outside.txt",
            filename="outside.txt",
        )


def test_delete_removes_existing_document(
    tmp_path: Path,
) -> None:
    storage = LocalDocumentStorage(
        root_path=tmp_path,
    )

    storage.store(
        content=b"delete me",
        storage_key="employees/QW-00002/test.pdf",
        filename="test.pdf",
    )

    target = (
        tmp_path
        / "employees"
        / "QW-00002"
        / "test.pdf"
    )

    assert target.exists()

    storage.delete(
        storage_key="employees/QW-00002/test.pdf",
    )

    assert not target.exists()


def test_delete_is_safe_when_file_does_not_exist(
    tmp_path: Path,
) -> None:
    storage = LocalDocumentStorage(
        root_path=tmp_path,
    )

    storage.delete(
        storage_key="employees/QW-00002/missing.pdf",
    )